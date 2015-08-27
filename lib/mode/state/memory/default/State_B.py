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
import logging.config
import subprocess
import time

# Pilberry packages|modules imports
from .State import State
from lib.globals import AUDIO_FEEDBACK_LOCK_FILE
from lib.globals import LOG_DIR
from lib import globals
from lib.utils import current_milli_time
from lib.carrier.Carrier import Carrier

logging.config.fileConfig(LOG_DIR + 'logging.conf')

stateBLog = logging.getLogger('stateBLog')

globals.last_playing_notification = current_milli_time()


##
# @class State_B
# @brief
class State_B(State):


    ##
    #   @brief
    def clear_playlist(self):
        if self.playlist_mode_activated:
            self.md.remove_current_song()
            self.md.jump_to_next_song()
            self.set_xnode(self.md.current_song)
            self.set_head(self.xnode)
            with Carrier() as C:
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Removed a song",
                                                 'timeout' : 1})
        else:
            with Carrier() as C:
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Can't remove",
                                                 'timeout' : 1})


    ##
    #   @brief  Moves to the parent Node. Returns the new current Node.
    #   @return Node
    def move_to_parent(self):
        # self.xnode.parent should never be None because we forbid
        # to access the root directory
        # So, self.xnode.parent.parent != None
        # is equivalent to 'self.xnode.parent is not root'
        if self.xnode.parent.parent != None:
            self.set_xnode(self.xnode.parent)

        self.set_state('State_C')


    ##
    #   @brief
    def move_to_node_next(self):
        self.md.jump_to_next_song()
        self.set_xnode(self.md.current_song)
        self.set_head(self.xnode)


    ##
    #   @brief
    def move_to_node_prev(self):
        self.md.jump_to_prev_song()
        self.set_xnode(self.md.current_song)
        self.set_head(self.xnode)


    ##
    #   @brief
    def jump_to_album_next(self):
        if self.playlist_mode_activated:
            self.md.stop()
            current_parent = self.md.current_song.parent

            while not self.md.next_songs_queue_is_empty() \
                and self.md.current_song.parent == current_parent:
            #___
                self.md.shift_playlist_to_left(dont_loop=True)
                self.md.unqueue_next()

            self.md.shift_playlist_to_right(dont_loop=True,
                                            dont_requeue=True)
            self.md.play_playlist()
            self.md.shift_playlist_to_left(dont_loop=True)
            self.set_xnode(self.md.current_song)
            self.set_head(self.xnode)


    ##
    #   @brief
    def jump_to_album_prev(self):
        if self.playlist_mode_activated:
            self.md.stop()
            current_parent = self.md.current_song.parent

            while not self.md.past_songs_queue_is_empty() \
                and self.md.current_song.parent == current_parent:
            #___
                self.md.shift_playlist_to_right(dont_loop=True,
                                                dont_requeue=True)

            current_parent = self.md.current_song.parent

            while not self.md.past_songs_queue_is_empty() \
                and self.md.current_song.parent == current_parent:
            #___
                self.md.shift_playlist_to_right(dont_loop=True,
                                                dont_requeue=True)

            if len(self.md.past_songs) > 1:
                self.md.shift_playlist_to_left(dont_loop=True)
            else:
                self.md.reinsert_current_song()

            self.md.play_playlist()
            self.set_xnode(self.md.current_song)
            self.set_head(self.xnode)


    ##
    #   @brief
    def move_to_1st_child(self):
        pass


    ##
    #   @brief
    def select(self):
        self.md.toggle_pause()
        self.set_state('State_D')


    ##
    #   @brief
    def esc(self):
        self.md.toggle_pause()
        self.set_state('State_D')


    ##
    #   @brief
    def stop(self):
        self.md.stop()
        self.set_state('State_A')
        if self.playlist_mode_activated:
            self.md.reinsert_current_song()
        else:
            self.md.clear_playlist()


    ##
    #   @brief
    def msg_cmus_playing(self, **options):
        new_time = current_milli_time()

        stateBLog.debug("playing notification received...")
        stateBLog.debug(str(new_time) \
                        + " - " \
                        + str(globals.last_playing_notification) \
                        + " = " \
                        + str(new_time - globals.last_playing_notification))

        if new_time - globals.last_playing_notification > 1000:
            if globals.cmus_playing_notifications_disabled:
                stateBLog.debug("Turning globals." \
                                + "cmus_playing_notifications_disabled" \
                                + " to False...")
                globals.cmus_playing_notifications_disabled = False
            else:
                self.md.shift_playlist_to_left()
                self.set_xnode(self.md.current_song)
                self.set_head(self.md.current_song)

        globals.last_playing_notification = new_time


    ##
    #   @brief
    def msg_cmus_stopped(self, **options):
        self.set_state('State_A')
        if not self.playlist_mode_activated:
            self.md.clear_playlist()
