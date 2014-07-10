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


from abc import ABCMeta, abstractmethod
from ..base import Clonable



class State(Clonable, metaclass=ABCMeta):

    # def handle(self, cmd):
    #    self.locals()['handle_cmd_' + cmd]()

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

    HANDLE = {'CMD_DIR_UP' : handle_cmd_dir_up,
              'CMD_DIR_DOWN' : handle_cmd_dir_down,
              'CMD_PLAY' : handle_cmd_play,
              'CMD_PREV' : handle_cmd_prev,
              'CMD_NEXT' : handle_cmd_next,
              'CMD_ESC' : handle_cmd_esc,
              'CMD_STOP' : handle_cmd_stop,
              'CMD_CHMOD' : handle_cmd_chmod
             }

    def handle(self, cmd):
        HANDLE[cmd]()
