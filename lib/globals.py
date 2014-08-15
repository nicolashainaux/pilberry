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

# Global variables initialization

# Python packages|modules imports
import sys, os
import configparser

#YES = ['Y', 'YES', 'Yes', 'True', 'TRUE', 1, "ON", "On", "on"]
#NO = ['N', 'NO', 'No', 'False', 'FALSE', 0, "OFF", "Off", "off"]
PILBERRY_ROOT = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
BIN_DIR = PILBERRY_ROOT + 'bin/'
CONF_DIR = PILBERRY_ROOT + 'etc/'
LOCKS_DIR = PILBERRY_ROOT + 'locks/'
LOG_DIR = PILBERRY_ROOT + 'log/'
VAR_RUN = PILBERRY_ROOT + 'var/run/'

SOCKETS_CONF_FILE = CONF_DIR + 'sockets.conf'
MODES_CONF_FILE = CONF_DIR + 'modes.conf'
CMD_CONF_FILE = CONF_DIR + 'cmd.conf'
USER_CONF_FILE = CONF_DIR + 'user.conf'

CORE_SCRIPT = PILBERRY_ROOT + 'pilberry_core'
DISPLAY_SCRIPT = PILBERRY_ROOT + 'pilberry_display'
VOLUME_SCRIPT = PILBERRY_ROOT + 'pilberry_volume'
AUDIO_FEEDBACK_SCRIPT = BIN_DIR + 'audio_feedback'
AUDIO_FEEDBACK_LOCK_FILE = LOCKS_DIR + 'audio_feedback'

PID_FILE = VAR_RUN + 'pid'


# Read the modes' list from appropriate conf file
MODES_CONFIG = configparser.ConfigParser()
MODES_CONFIG.read(MODES_CONF_FILE)
modes_list = []
for s in MODES_CONFIG.sections():
    if MODES_CONFIG[s].getboolean('ENABLED'):
        modes_list.append(s)

##
#   @todo   At startup, define the current_mode as last used mode
current_mode_id = modes_list[0]
current_state = {}
##
#   @todo   At startup, get the tree matching the current mode and state
current_mode = None

# Read the modes' list from appropriate conf file
CMD_CONFIG = configparser.ConfigParser()
CMD_CONFIG.optionxform = lambda option: option
CMD_CONFIG.read(CMD_CONF_FILE)
cmd_match_list = dict(CMD_CONFIG[MODES_CONFIG[current_mode_id]['TYPE']])

# Get the port from sockets' conf file
SOCKETS_CONFIG = configparser.ConfigParser()
SOCKETS_CONFIG.read(SOCKETS_CONF_FILE)

# Read the modes' list from appropriate conf file
USER_CONFIG = configparser.ConfigParser()
USER_CONFIG.optionxform = lambda option: option
USER_CONFIG.read(USER_CONF_FILE)

MUSIC_FILE_EXTENSIONS = ['.ogg', '.mp3', '.flac', '.wma', '.m4a',
                         '.mpc', '.mpp', '.wav', '.wv', '.ape',
                         '.aac', '.mp4', '.mod', '.s3m']

CMUS_NOTIFICATIONS = ['stopped',
                      'playing',
                      'paused']

cmus_status = 'stopped'
