# Copyright (C) 2018 Nikita S., Koni Dev Team, All Rights Reserved
# https://github.com/Nekit10/pyloges
#
# This file is part of Pyloges.
#
# Pyloges is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyloges is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyloges.  If not, see <https://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch

import timeout_decorator

from pyloges.handlers.std import StdHandler
from pyloges.handlers.file import FileHandler
from pyloges.logger import Logger
from pyloges.asynclogger import AsyncLogger
from pyloges.classes.config import Config

stdout = ""


def print_new(*args, sep=' ', end='\n', file=None):
    global stdout
    for i in args:
        stdout += str(i)
        if args.index(i) != len(args) - 1:
            stdout += sep


stderr = ""


def stderr_print_new(msg):
    global stderr
    stderr += msg


files_ = {}


class PatchedStream:

    mode = ''
    closed = False
    file = ''

    def __init__(self, filename, mode):
        self.mode = mode
        self.file = filename

    def read(self):
        try:
            if self.closed:
                raise PermissionError('Reading from closed file')
            return files_[self.file]
        except KeyError:
            raise FileNotFoundError('[Errno 2] No such file or directory')

    def write(self, file):
        global files_
        if self.closed:
            raise PermissionError('Writing to closed file')
        if self.mode != 'w' and self.mode != 'a':
            raise PermissionError('Writing to read-only file')
        files_[self.file] = file

    def close(self):
        self.closed = True


def open_patched(filename, mode, buffering=None, encoding=None, errors=None, newline=None, closefd=True):
    return PatchedStream(filename, mode)


class HandlersTest(unittest.TestCase):
    @patch("builtins.print", print_new)
    @patch("sys.stderr.write", stderr_print_new)
    def test_std(self):
        global stdout, stderr
        stdout = ""
        stderr = ""
        msg = "dwowew weufhw euf hwiuehaus aufh qufhq uefiqefugn j126312037r12837r0827etfbo"
        handler = StdHandler()
        handler.print_log(msg)
        self.assertEqual("", stdout)
        self.assertEqual(msg+"\n", stderr)

    @patch("builtins.open", open_patched)
    def test_file(self):
        global files_
        msg = "dwowew weufhw euf hwiuehaus aufh qufhq uefiqefugn j126312037r12837r0827etfbo"
        filename = "latest.log"
        files_[filename] = ""
        handler = FileHandler(filename)
        handler.print_log(msg)
        handler.save()
        self.assertEqual(msg+'\n', files_[filename])


class LoggerTest(unittest.TestCase):
    @patch("builtins.print", print_new)
    @patch("sys.stderr.write", stderr_print_new)
    def test_std(self):
        global stdout, stderr
        stdout = ""
        stderr = ""
        logger = Logger(Config(log_message_format="{msg}"))
        msg = "dwowew weufhw euf hwiuehaus aufh qufhq uefiqefugn j126312037r12837r0827etfbo"
        logger.t("trace" + msg)
        logger.d("debug" + msg)
        logger.i("info" + msg)
        logger.f("fatal" + msg)
        self.assertEqual("debug" + msg + "\n" + "info" + msg + "\n" + "fatal" + msg + "\n", stderr)
        self.assertEqual("", stdout)

    @patch("builtins.open", open_patched)
    def test_file(self):
        global files_
        filename = "latest.log"
        files_[filename] = ""
        logger = Logger(Config(log_message_format="{msg}", print_to_std=False))
        msg = "dwowew weufhw euf hwiuehaus aufh qufhq uefiqefugn j126312037r12837r0827etfbo"
        logger.config.add_writing_to_file(filename)
        logger.t("trace" + msg)
        logger.d("debug" + msg)
        logger.i("info" + msg)
        logger.f("fatal" + msg)
        self.assertEqual("debug" + msg + "\n" + "info" + msg + "\n" + "fatal" + msg + "\n", files_[filename])


class AsyncLoggerTest(unittest.TestCase):
    @patch("builtins.print", print_new)
    @patch("sys.stderr.write", stderr_print_new)
    @unittest.skip
    def test_std(self):
        global stdout, stderr
        stdout = ""
        stderr = ""
        logger = AsyncLogger(Config(log_message_format="{msg}"))
        msg = "dwowew weufhw euf hwiuehaus aufh qufhq uefiqefugn j126312037r12837r0827etfbo"
        logger.t("trace" + msg)
        logger.d("debug" + msg)
        logger.i("info" + msg)
        logger.f("fatal" + msg)
        logger.wait()
        self.assertEqual("debug" + msg + "\n" + "info" + msg + "\n" + "fatal" + msg + "\n", stderr)
        self.assertEqual("", stdout)

    @patch("builtins.open", open_patched)
    @unittest.skip
    def test_file(self):
        global files_
        filename = "latest.log"
        files_[filename] = ""
        logger = AsyncLogger(Config(log_message_format="{msg}", print_to_std=False))
        msg = "dwowew weufhw euf hwiuehaus aufh qufhq uefiqefugn j126312037r12837r0827etfbo"
        logger.config.add_writing_to_file(filename)
        logger.t("trace" + msg)
        logger.d("debug" + msg)
        logger.i("info" + msg)
        logger.f("fatal" + msg)
        logger.wait()
        self.assertEqual("debug" + msg + "\n" + "info" + msg + "\n" + "fatal" + msg + "\n", files_[filename])


if __name__ == '__main__':
    unittest.main()
