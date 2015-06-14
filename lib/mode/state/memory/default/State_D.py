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
from .State_CD import State_CD
import lib.globals as globals

##
# @class State_D
# @brief
class State_D(State_CD):


    ##
    #   @brief
    def select(self):
        # xnode is an inode
        if len(self.xnode.children) >= 1:
            self.handle('CMD_MOVE_TO_1ST_CHILD')

        # xnode is a leaf
        else:
            if self.xnode != self.head:
                self.set_head(self.xnode)
                ##
                #   @todo   Check if this stop is still necessary once the
                #           delayed play is implemented
                self.md.stop()
                self.playlist_mode_activated = False
                self.md.play_from_here()
            else:
                globals.cmus_playing_notifications_disabled = True
                self.md.toggle_pause()

            self.set_state('State_B')


    ##
    #   @brief
    def esc(self):
        self.set_xnode(self.head)
        self.md.toggle_pause()
        self.set_state('State_B')

