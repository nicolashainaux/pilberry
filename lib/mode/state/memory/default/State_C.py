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
import time

# Pilberry packages|modules imports
from .State_CD import State_CD
#import lib.globals as globals
from lib import globals

current_milli_time = lambda: int(round(time.time() * 1000))

##
# @class State_C
# @brief
class State_C(State_CD):


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
                self.playlist_mode_activated = False
                self.md.play_from_here()

            self.set_state('State_B')


    ##
    #   @brief
    def esc(self):
        if globals.cmus_status == 'playing':
            self.set_xnode(self.head)
            self.set_state('State_B')

        elif globals.cmus_status == 'stopped':
            self.set_state('State_A')


    ##
    #   @brief
    def msg_cmus_playing(self, **options):
        new_time = current_milli_time()

        if new_time - globals.last_playing_notification > 1000:
            if globals.cmus_playing_notifications_disabled:
                globals.cmus_playing_notifications_disabled = False
            else:
                self.md.resync_playlist()
                self.set_head(self.md.current_song)

        globals.last_playing_notification = new_time
