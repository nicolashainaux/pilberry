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
from abc import ABCMeta, abstractmethod


##
# @class State
# @brief Abstract class that provides the handle() method for
#        all State_* subclasses
class State(object, metaclass=ABCMeta):

    # def handle(self, cmd):
    #    self.locals()['handle_cmd_' + cmd]()

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def handle_cmd_dir_up(self):
        pass

    @abstractmethod
    def handle_cmd_dir_down(self):
        pass

    @abstractmethod
    def handle_cmd_play(self):
        pass

    @abstractmethod
    def handle_cmd_prev(self):
        pass

    @abstractmethod
    def handle_cmd_next(self):
        pass

    @abstractmethod
    def handle_cmd_esc(self):
        pass

    @abstractmethod
    def handle_cmd_stop(self):
        pass

    @abstractmethod
    def handle_cmd_chmod(self):
        pass

    HANDLE = {'CMD_DIR_UP' : 'handle_cmd_dir_up',
              'CMD_DIR_DOWN' : 'handle_cmd_dir_down',
              'CMD_PLAY' : 'handle_cmd_play',
              'CMD_PREV' : 'handle_cmd_prev',
              'CMD_NEXT' : 'handle_cmd_next',
              'CMD_ESC' : 'handle_cmd_esc',
              'CMD_STOP' : 'handle_cmd_stop',
              'CMD_CHMOD' : 'handle_cmd_chmod'
             }

    def handle(self, cmd):
        getattr(self, self.HANDLE[cmd])()
