import os
import time
import sys
import io
import logging
import asyncio
import warnings
import numpy as np
from abc import ABC, abstractmethod, abstractproperty
from concurrent.futures import ThreadPoolExecutor
from itertools import count
from dataclasses import dataclass, field
from pyspimosim.base_model import BaseModel, NoMoreDataException, ModelBackendSettings as BaseModelBackendSettings

class CSVPipeReaderEOF(Exception):
    pass


def to_numbers(obj):
    if type(obj) is list:
        return [to_numbers(o) for o in obj]

    if type(obj) is dict:
        return {key: to_numbers(value) for key, value in obj.items()}

    if type(obj) is float or type(obj) is int:
        return obj

    try:
        return int(obj)
    except Exception as e:
        try:
            return float(obj)
        except Exception as e:
            logging.warning("Warning! Not a float: " + str(e))
            return 0

async def async_loadtxt(file, max_rows=None, ndmin=None, comments=None, executor = ThreadPoolExecutor()):
    loop = asyncio.get_event_loop()
    def loadtxt():
        try:
            return np.loadtxt(file, max_rows=max_rows, ndmin=2, comments=None)
        except ValueError:
            return np.zeros((0, 0))
    return await loop.run_in_executor(executor, loadtxt)

class NoEOFReader(io.BufferedReader):
    encoding = "UTF-8"
    __buf = b""

    def read(self, size=-1):
        buf = super().read(size=size)
        while len(buf) < size:
            buf += super().read(size=size - len(buf))
        return buf

    def read1(self, size=-1):
        buf = super().read1(size=size)
        while len(buf) < size:
            buf += super().read1(size=size - len(buf))
        return buf

    def readline(self):
        self.__buf += super().readline()
        if self.__buf[-1:] == b"\n":
            buf = self.__buf
            self.__buf = b""
            return buf
        return b""

    def __iter__(self):
        return self

    def __next__(self):
        b = self.readline()
        if not b:
            raise StopIteration()
        return b.decode("UTF-8")


class CSVPipeReader:
    sleep_time = 0.01
    read_tries_until_done = 3

    def __init__(self, path, data_file_fields, block_size=1, skip_lines=0, data_is_final=False, new_fifo=True):
        self.path = path

        if new_fifo:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

        if not os.path.exists(path):
            os.system(f"mkfifo {path}")

        self.data_file_fields = data_file_fields
        if any(callable(func_or_factor) for key, func_or_factor in data_file_fields):
            self._convert_using_function = True
            self._functions = []
            for i, (key, func_or_factor) in enumerate(data_file_fields):
                if callable(func_or_factor):
                    self._functions.append(np.vectorize(func_or_factor))
                else:
                    self._functions.append(lambda x: func_or_factor * x)
        else:
            self._factors = np.array(
                [factor for key, factor in data_file_fields])
            self._convert_using_function = False

        self._skip_lines = skip_lines
        self.data_is_final = data_is_final

        self.file = None
        self.block_size = block_size
        self.buf = [{key: 0 for key, _ in self.data_file_fields}
                    ] * self.block_size

    async def open_file(self):
        while not os.path.exists(self.path):
            await asyncio.sleep(self.sleep_time)

        # open without buffering
        f = open(self.path, "rb", buffering=0)
        os.set_blocking(f.fileno(), False)
        self.file = NoEOFReader(f)

    async def prepare_file(self):
        if self.file is None:
            await self.open_file()

        while self._skip_lines > 0:
            self.file.readline()
            self._skip_lines -= 1

    def close(self):
        if not self.file is None:
            self.file.close()
        self.file = None


    def get_file_stat(self):
        if self.file is None:
            return 0, 0
        try:
            position = self.file.tell()
        except io.UnsupportedOperation:
            position = 0
        try:
            size = os.stat(self.path).st_size
        except FileNotFoundError:
            size = 0
        return position, size


    async def fill_buffer(self, max_rows=None):
        if max_rows is None:
            max_rows = self.block_size

        await self.prepare_file()

        if self.data_is_final:
            max_tries = self.read_tries_until_done
        else:
            max_tries = -1

        if max_rows:
            max_rows = min(max_rows, self.get_reasonable_max_chunk_size())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw = None
            for i in count():
                if self.file is None:
                    raise CSVPipeReaderEOF()
                raw = await async_loadtxt(self.file, max_rows=max_rows, ndmin=2, comments=None)
                if max_rows >= 2**13:
                    await asyncio.sleep(0.1)
                if raw.shape[0] != 0:
                    break
                if i == max_tries:
                    raise CSVPipeReaderEOF()
                await asyncio.sleep(self.sleep_time)

            self.buf = raw

    def get_reasonable_max_chunk_size(self):
        # Limit amount of data to reasonable amount.
        estimated_bytes_per_row = 10 * len(self.data_file_fields)
        default_limit = 2 ** 20 / estimated_bytes_per_row
        limit = default_limit
        position, full_size = self.get_file_stat()
        if position != 0:
            # Use smaller chunks at beginning of file
            if full_size != 0:
                limit *= (position / full_size) ** 0.5
            else:
                # fallback: replace full_size with 100 * default_limit
                limit *= (position / (100 * default_limit)) ** 0.5
        if full_size != 0:
            # Use larger chunks for large files
            limit *= (full_size / default_limit) ** 0.5

        max_limit = 100 * default_limit
        limit = round(max(min(max_limit, limit), default_limit))
        return limit


class CSVPipeWriter(ABC):
    def __init__(self, path, new_fifo=False):
        self.path = path

        if new_fifo:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

        if not os.path.exists(path):
            os.system(f"mkfifo {path}")

        self.file = None

    def open_file(self):
        # open with line buffering
        self.file = os.fdopen(os.open(self.path, os.O_RDWR | os.O_NONBLOCK), "wb")

    def close(self):
        if not self.file is None:
            self.file.close()
        self.file = None

    def write_fields(self, fields):
        self.writeline(" ".join(str(field) for field in fields))

    def writeline(self, line):
        self.write(line + os.linesep)

    def write(self, s):
        self.file.write(s.encode())
        self.file.flush()


class CSVPipeModel(BaseModel):
    multi_step = True
    save_state_after_init = False

    def __init__(self, backend, model_backend_settings, user_model_settings):
        super().__init__(backend, model_backend_settings, user_model_settings)
        self.csv_pipe_writer = None
        self.init_workdir()
        self.init_pipe_reader()
        self.state = self.csv_pipe_reader.buf[-1]
        self.init_pipe_writer(model_backend_settings)
        self.change_settings(user_model_settings, True)

    def init_workdir(self):
        self.work_dir = self.model_backend_settings.workbasedir + "/" + \
            self.model_backend_settings.instance_id.get(self.backend) + "/"
        try:
            os.makedirs(self.work_dir)
        except FileExistsError:
            pass

    def init_pipe_reader(self):
        self.csv_pipe_reader = CSVPipeReader(
            path=self.work_dir + self.model_backend_settings.data_file,
            data_file_fields=self.data_file_fields,
            skip_lines=self.model_backend_settings.data_file_skiplines,
            data_is_final=self.model_backend_settings.data_is_final,
            new_fifo=not self.model_backend_settings.no_new_run
        )

    def change_settings(self, user_model_settings, restart=False):
        if self.csv_pipe_writer is None:
            return
        parameters_as_numbers = to_numbers(user_model_settings['parameters'])
        parameters = [factor * parameters_as_numbers[key] for key, factor in self.settings_fields]
        self.csv_pipe_writer.write_fields(parameters)

    async def steps(self, vars_config, t, t_max, protocol, save_interval, next_send_time):
        try:
            await self.csv_pipe_reader.fill_buffer(max_rows=t_max - t + 1)
        except CSVPipeReaderEOF as e:
            raise NoMoreDataException() from e

        for i, (name, _) in enumerate(self.data_file_fields):
            protocol.vars[name].set_all(
                t, np.array(self.csv_pipe_reader.buf[:, i], dtype=protocol.vars[name].dtype))

        t_max = t + len(self.csv_pipe_reader.buf) - 1
        protocol.t_max = t_max
        return t_max

    async def step(self, vars_config, t, restart=False):
        try:
            await self.csv_pipe_reader.fill_buffer(max_rows=1)
        except CSVPipeReaderEOF as e:
            raise NoMoreDataException() from e

        self.state = {
            name: field for (name, _), field in zip(self.data_file_fields, self.csv_pipe_reader.buf[-1])
        }

    def stop(self):
        if not self.csv_pipe_writer is None:
            self.csv_pipe_writer.close()
        self.csv_pipe_reader.close()

    @abstractmethod
    def init_pipe_writer(self, model_backend_settings):
        pass

    @abstractproperty
    def data_file_fields(self):
        pass

    @abstractproperty
    def settings_fields(self):
        pass


class InstanceId(str):
    def __new__(cls, s, use_handler_id=False):
        if type(s) == InstanceId:
            return s
        new = super(InstanceId, cls).__new__(cls, s)
        new.use_handler_id = use_handler_id
        return new

    def get(self, backend):
        if self.use_handler_id:
            return str(backend.handler.id)
        return str(self)


@dataclass
class ModelBackendSettings(BaseModelBackendSettings):
    workbasedir: str = field(default=".", metadata={
                             "help": "The working directory will be <workbasedir>/<instance_id>"})
    instance_id: InstanceId = field(default=InstanceId("<random number>", use_handler_id=True), metadata={
                                    "help": "The working directory will be <workbasedir>/<instance_id>"})
    setting_file: str = field(default="settings.csv", metadata={
                              "help": "File name (inside working directory) for the *.csv file or pipe for settings (and more)"})
    data_file: str = field(default="data.csv", metadata={
                           "help": "File name (inside working directory) for the *.csv file or pipe for generated data"})
    data_file_skiplines: int = field(default=0, metadata={
                                     "help": "Size of the ignored header of the file specified by --output"})
    no_new_run: bool = field(default=False, metadata={
                             "help": "Do not generate new data but read existing data from a previous run"})
    data_is_final: bool = field(default=False, metadata={
                                "help": "Stop reading after reaching end of file instead of waiting for new data"})
