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

import datetime


def _process_msg(format_: str, log_level: str, msg: str) -> str:
    tt = datetime.date.today().timetuple()

    new_str = format_
    new_str.replace("{level}", log_level)
    new_str.replace("%y", tt.tm_year)
    new_str.replace("%M", tt.tm_mon)
    new_str.replace("%d", tt.tm_mday)
    new_str.replace("%h", tt.tm_hour)
    new_str.replace("%M", tt.tm_min)
    new_str.replace("%s", tt.tm_sec)
    new_str.replace("{msg}", msg)

    return new_str
