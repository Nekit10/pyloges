import unittest
import time
from unittest.mock import patch

from pyloges.logger import _process_msg
from pyloges.handlers.file import _process_filename


class datetimefix:
    @classmethod
    def now(cls):
        return datetimefix()

    def timetuple(self):
        return time.struct_time((2000, 8, 9, 9, 0, 0, 0, 0, 0))


class FormatMethodsTest(unittest.TestCase):
    @patch("datetime.datetime", datetimefix)
    def test_msg_format(self):
        self.assertEqual("INFO 09.08.2000 9:00:00 - MSG", _process_msg("{level} %d.%M.%y %h:%m:%s - {msg}", "INFO", "MSG"))

    @patch("datetime.datetime", datetimefix)
    def test_filename_format(self):
        self.assertEqual("09.08.2000 9:00:00", _process_filename("%d.%M.%y %h:%m:%s"))


if __name__ == '__main__':
    unittest.main()
