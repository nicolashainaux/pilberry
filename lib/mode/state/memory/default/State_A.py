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
import logging

# Pilberry packages|modules imports
from .State_ACD import State_ACD
from lib.globals import PLAYLIST_FILE_EXTENSIONS


##
# @class State_A
# @brief
class State_A(State_ACD):


    ##
    #   @brief
    def select(self):
        if len(self.xnode.children) >= 1:
            self.handle('CMD_MOVE_TO_1ST_CHILD')
        else:
            if self.playlist_mode_activated:
                self.md.play_playlist()
                self.set_xnode(self.md.current_song)
                self.set_head(self.xnode)
            else:
                if self.xnode.extension in PLAYLIST_FILE_EXTENSIONS:
                    self.handle("CMD_LOAD_PLAYLIST", file=self.xnode)
                    self.set_xnode(self.md.current_song)
                    self.set_head(self.xnode)
                    self.md.play_playlist()

                else:
                    self.set_head(self.xnode)
                    self.md.play_from_here()

            self.set_state('State_B')


    ##
    #   @brief
    def esc(self):
        pass


    ##
    #   @brief
    def stop(self):
        pass


