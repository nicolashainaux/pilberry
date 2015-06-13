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

logging.config.fileConfig(LOG_DIR + 'logging.conf')

stateBLog = logging.getLogger('stateBLog')

current_milli_time = lambda: int(round(time.time() * 1000))

globals.last_playing_notification = current_milli_time()


##
# @class State_B
# @brief
class State_B(State):


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
        if self.queue_mode_activated:
            if not self.md.queue_is_empty():
                self.md.skip_to_next_song()
                self.set_xnode(self.md.current_song)
                self.set_head(self.xnode)
            else:
                pass
                # So far, we do not loop over the queue...

        else:
            # We compute the new position with a modulo to go to first position
            # if we were at end and vice-versa
            new_position = (self.xnode.position + 1) % len(self.xnode.neighbours)
            self.set_xnode(self.xnode.neighbours[new_position])

            if len(self.xnode.children) == 0:
                self.set_head(self.xnode)

                # If we've just "cycled", e.g. we've landed on the first song
                # again, then we can repopulate the queue
                if self.head.position == 0:
                    self.md.clear_queue()
                    for n in [self.head] + self.head.neighbours_after:
                        self.md.queue_song(n)

                self.md.skip_to_next_song()

            else:
                self.md.stop()
                self.set_state('State_A')


    ##
    #   @brief
    def move_to_node_prev(self):
        if self.queue_mode_activated:
            if not self.md.queue_past_is_empty():
                self.md.skip_to_prev_song_in_queue()
                self.set_xnode(self.md.current_song)
                self.set_head(self.xnode)
            else:
                pass
                # So far, we do not loop over the queue...

        else:
            # We compute the new position with a modulo to go to first position
            # if we were at end and vice-versa
            self.md.queue_song_first(self.head)

            stateBLog.debug("self.xnode.position - 1 = " \
                            + str(self.xnode.position - 1))
            stateBLog.debug("len(self.xnode.neighbours) = " \
                            + str(len(self.xnode.neighbours)))
            new_position = (self.xnode.position - 1) % len(self.xnode.neighbours)
            stateBLog.debug("new_position = " + str(new_position))
            self.set_xnode(self.xnode.neighbours[new_position])

            if len(self.xnode.children) == 0:
                self.set_head(self.xnode)

                # If we've just "cycled", e.g. we've landed on the last song,
                # then we can clear the queue
                if self.head.position == len(self.xnode.neighbours) - 1:
                    self.md.clear_queue()

                self.md.queue_song_first(self.head)
                self.md.skip_to_next_song()


            else:
                self.md.stop()
                self.set_state('State_A')


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
                self.md.unqueue_song_first()
                self.set_xnode(self.md.current_song)
                self.set_head(self.md.current_song)

        globals.last_playing_notification = new_time


    ##
    #   @brief
    def msg_cmus_stopped(self, **options):
        self.set_state('State_A')
