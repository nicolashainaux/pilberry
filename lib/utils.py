# -*- coding: utf-8 -*-

# Pilberry runs a car radio based on Raspberry Pi
# Copyright 2014 Olivier Cecillon <ocecillon@users.sourceforge.net>
# and Nicolas Hainaux <nico_h@users.sourceforge.net>

# This file is part of Pilberry.

# Pilberry is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Pilberry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Pilberry; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Python packages|modules imports
import re
import time
import subprocess

# Pilberry packages|modules imports
from lib.globals import SOCKETS_CONFIG

current_milli_time = lambda: int(round(time.time() * 1000))

##
#   @brief  Natural sort of a list; e.g. ['file2', 'file1', 'file10'] becomes
#           ['file1', 'file2', 'file10'] and NOT ['file1', 'file10', 'file2']
def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


##
#   @brief
def get_cmus_volume():
    cmus_status = subprocess.Popen(['cmus-remote',
                                    '--server',
                                    SOCKETS_CONFIG['TO_CMUS']['FILE'],
                                    '-C',
                                    'status'],
                                    stdout=subprocess.PIPE)

    grep_cmd = subprocess.Popen(['grep', 'vol_left'],
                                stdin=cmus_status.stdout,
                                stdout=subprocess.PIPE)

    raw_info = grep_cmd.communicate()[0].decode()

    print("vol: " + raw_info)

    return raw_info[12:len(raw_info)-1]
