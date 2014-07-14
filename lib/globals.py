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

# Global variables

# Pilberry packages|modules imports
import sys, os

#YES = ['Y', 'YES', 'Yes', 'True', 'TRUE', 1, "ON", "On", "on"]
#NO = ['N', 'NO', 'No', 'False', 'FALSE', 0, "OFF", "Off", "off"]
PILBERRY_ROOT = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
CONF_DIR = PILBERRY_ROOT + 'etc/'
SOCKETS_CONF = CONF_DIR + 'sockets.conf'
MODES_CONF = CONF_DIR + 'modes.conf'
CMD_CONF = CONF_DIR + 'cmd.conf'
