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
import pickle
from abc import ABCMeta, abstractmethod
from collections import deque

# Pilberry packages|modules imports
from lib.globals import SOCKETS_CONFIG, USER_CONFIG
import lib.globals as globals
from lib.carrier.Carrier import Carrier
from lib.utils import current_milli_time


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
    #@abstractmethod
    def jump_to_album_next(self):
        pass


    ##
    #   @brief
    #@abstractmethod
    def jump_to_album_prev(self):
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
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Queuing songs..."})
                for elt in self.xnode.children:
                    if len(elt.children) == 0:
                        self.md.append_song(elt)
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Queued all songs",
                                                 'timeout' : 1})
            else:
                self.md.append_song(self.xnode)
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Queued a song",
                                                 'timeout' : 1})


    ##
    #   @brief
    def prepend_song(self):
        self.activate_playlist_mode()

        with Carrier() as C:
            if len(self.xnode.children) >= 1:
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Queuing songs..."})
                for elt in reversed(self.xnode.children):
                    if len(elt.children) == 0:
                        self.md.prepend_song(elt)
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Queued all songs",
                                                 'timeout' : 1})
            else:
                self.md.prepend_song(self.xnode)
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Queued a song",
                                                 'timeout' : 1})


    ##
    #   @brief
    def clear_playlist(self):
        if self.playlist_mode_activated:
            self.unactivate_playlist_mode()
            self.md.clear_playlist()
            with Carrier() as C:
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Playlist cleared",
                                                 'timeout' : 1})
        else:
            with Carrier() as C:
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Can't clear",
                                                 'timeout' : 1})


    ##
    #   @brief
    def save_playlist(self):
        if self.playlist_mode_activated:
            with Carrier() as C:
                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Saving playlist"})

                playlist = deque()

                playlist.extend(self.md.past_songs)
                playlist.extend(self.md.next_songs)

                with open(r"/data/music/05 - Playlists/current.pil", 'wb') \
                    as outfile:
                #___
                    pickle.dump([self._tree, playlist], outfile)

                C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Playlist saved",
                                                 'timeout' : 1})


    ##
    #   @brief
    def load_playlist(self, **options):
        with Carrier() as C:
            C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Loading..."})

            data = None

            with open(options['file'].full_path, "rb") as f:
                data = pickle.load(f)

            self._tree = data[0]
            self.md.clear_playlist()

            last_time = current_milli_time()
            how_many = len(data[1])
            i = 1

            for n in data[1]:
                self.md.append_song(n)
                i += 1
                if current_milli_time() - last_time > 500:
                    last_time = current_milli_time()
                    number = str(int(100*i/how_many))
                    progress_raw = "    " + number + " %"
                    progress = progress_raw[len(progress_raw) - 5:]
                    C.send('CORE_STATE_TO_DISPLAY',
                           {'msg' : "Loading..." + progress,
                            'last_chars' : 5})

            self.activate_playlist_mode()

            C.send('CORE_STATE_TO_DISPLAY', {'msg' : "Playlist loaded",
                                             'timeout' : 1})


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
