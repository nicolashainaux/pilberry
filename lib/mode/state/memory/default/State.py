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
import subprocess
from abc import ABCMeta, abstractmethod

# Pilberry packages|modules imports
from lib.globals import SOCKETS_CONFIG, USER_CONFIG
import lib.globals as globals
from lib.carrier.Carrier import Carrier


##
# @class State
# @brief Mother class of (memory) States
#   @todo   More code factorization between the different State_* classes?
class State(object, metaclass=ABCMeta):


    ##
    #   @brief  Moves to the parent Node. Returns the new current Node.
    @abstractmethod
    def move_to_parent(self):
        pass


    ##
    #   @brief
    @abstractmethod
    def move_to_node_next(self):
        pass


    ##
    #   @brief
    @abstractmethod
    def move_to_node_prev(self):
        pass


    ##
    #   @brief
    @abstractmethod
    def move_to_1st_child(self):
        pass


    ##
    #   @brief
    @abstractmethod
    def select(self):
        pass

    ##
    #   @brief
    @abstractmethod
    def esc(self):
        pass


    ##
    #   @brief
    @abstractmethod
    def stop(self):
        pass


    ##
    #   @brief
    def append_song(self):
        self.activate_playlist_mode()

        with Carrier() as C:
            if len(self.xnode.children) >= 1:
                C.send('CORE_STATE_TO_DISPLAY', "Queuing songs...")
                for elt in self.xnode.children:
                    if len(elt.children) == 0:
                        self.md.append_song(elt)
                C.send('CORE_STATE_TO_DISPLAY', "Queued all songs")
            else:
                self.md.append_song(self.xnode)
                C.send('CORE_STATE_TO_DISPLAY', "Queued a song")


    ##
    #   @brief
    def prepend_song(self):
        self.activate_playlist_mode()

        with Carrier() as C:
            if len(self.xnode.children) >= 1:
                C.send('CORE_STATE_TO_DISPLAY', "Queuing songs...")
                for elt in self.xnode.children:
                    if len(elt.children) == 0:
                        self.md.prepend_song(elt)
                C.send('CORE_STATE_TO_DISPLAY', "Queued all songs")
            else:
                self.md.prepend_song(self.xnode)
                C.send('CORE_STATE_TO_DISPLAY', "Queued a song")


    ##
    #   @brief
    def clear_playlist(self):
        self.unactivate_playlist_mode()
        self.md.clear_playlist()


    ##
    #   @brief
    def msg_cmus_playing(self, **options):
        pass


    ##
    #   @brief
    def msg_cmus_stopped(self, **options):
        pass


    ##
    #   @brief
    def msg_cmus_paused(self, **options):
        pass


    ##
    #   @brief
    def vol_up(self, **options):
        subprocess.Popen(['cmus-remote',
                          '--server',
                          SOCKETS_CONFIG['TO_CMUS']['FILE'],
                          '-C',
                          'vol +' + USER_CONFIG['GENERAL']['VOL_STEP'] + '%'])


    ##
    #   @brief
    def vol_down(self, **options):
        subprocess.Popen(['cmus-remote',
                          '--server',
                          SOCKETS_CONFIG['TO_CMUS']['FILE'],
                          '-C',
                          'vol -' + USER_CONFIG['GENERAL']['VOL_STEP'] + '%'])

    ##
    #   @brief
    def no_action(self, **options):
        pass
