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
import time
import logging
import logging.config
from collections import deque

# Pilberry packages|modules imports
from lib import globals
#import lib.globals as globals
from lib.globals import SOCKETS_CONFIG
from lib.globals import LOG_DIR

logging.config.fileConfig(LOG_DIR + 'logging.conf')

mdLog = logging.getLogger('mdLog')

##
# @class MusicDriver
# @brief The MusicDriver will drive the music player
class MusicDriver(object):


    ##
    #   @brief
    def __init__(self):
        self._past_songs = deque()
        self._next_songs = deque()


    ##
    #   @brief
    def get_current_song(self):
        if len(self._past_songs) >= 1:
            return self._past_songs[len(self._past_songs) - 1]
        else:
            return {'file_name' : "(No song)"}


    current_song = property(get_current_song,
                            doc="The Mode's MusicDriver")


    ##
    #   @brief
    def get_past_songs(self):
        return self._past_songs


    past_songs = property(get_past_songs,
                          doc="The past songs' deque")


    ##
    #   @brief
    def get_next_songs(self):
        return self._next_songs


    next_songs = property(get_next_songs,
                          doc="The next songs' deque")


    next_songs = property(get_next_songs,
                          doc="The next songs' deque")


    ##
    #   @brief
    def next_songs_queue_is_empty(self):
        return len(self._next_songs) == 0


    ##
    #   @brief
    def past_songs_queue_is_empty(self):
        return len(self._past_songs) == 1


    ##
    #   @brief
    def append_song(self, n):
        mdLog.debug('appending song: ' + n['file_name'])

        if len(self._past_songs) == 0:
            self._past_songs.append(n)
        else:
            self._next_songs.append(n)
        self._send(['-C', 'add -q ' + n.full_path])

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def prepend_song(self, n):
        mdLog.debug('prepending song: ' + n['file_name'])

        if len(self._past_songs) == 0:
            self._past_songs.append(n)
        else:
            self._next_songs.appendleft(self._past_songs.pop())
            self._past_songs.append(n)

        self._send(['-C', 'add -Q ' + n.full_path])

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def reinsert_current_song(self):
        mdLog.debug('re-inserting current song')
        self._send(['-C', 'add -Q ' + self.current_song.full_path])


    ##
    #   @brief
    def shift_playlist_to_left(self, **options):
        loop = True
        if 'dont_loop' in options and options['dont_loop'] == True:
            loop = False

        if len(self._next_songs) >= 1:
            self._past_songs.append(self._next_songs.popleft())

        # In this case we've reached the end of the next songs.
        # As a default behaviour, we will loop over the playlist.
        elif len(self._next_songs) == 0 and loop:
            self._next_songs, self._past_songs = \
                                            self._past_songs, self._next_songs
            self._send(['-c', '-q'])
            for n in self._next_songs:
                self._send(['-C', 'add -q ' + n.full_path])
            self._past_songs.append(self._next_songs.popleft())

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def shift_playlist_to_right(self, **options):
        loop = True
        if 'dont_loop' in options and options['dont_loop'] == True:
            loop = False

        requeue = True
        if 'dont_requeue' in options and options['dont_requeue'] == True:
            requeue = False

        if len(self._past_songs) >= 1:
            self._send(['-C', 'add -Q ' + self.current_song.full_path])
            self._next_songs.appendleft(self._past_songs.pop())

        # In this case we've reached the end of the past songs.
        # As a default behaviour, we will loop over the playlist.
        if len(self._past_songs) == 0 and loop:
            self._next_songs, self._past_songs = \
                                            self._past_songs, self._next_songs
            self._send(['-c', '-q'])

        if requeue:
            self._send(['-C', 'add -Q ' + self.current_song.full_path])

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def clear_playlist(self):
        mdLog.debug('playlist is being cleared')
        self._next_songs.clear()
        self._past_songs.clear()
        self._send(['-c', '-q'])

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def jump_to_next_song(self, **options):
        mdLog.debug('jump to next song')

        self.shift_playlist_to_left(**options)
        self._send(['-C', 'player-next'])
        globals.cmus_playing_notifications_disabled = True

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def jump_to_prev_song(self, **options):
        mdLog.debug('jump to prev song')

        self.shift_playlist_to_right(**options)
        self._send(['-C', 'player-next'])
        globals.cmus_playing_notifications_disabled = True

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def play_from_here(self):
        self.clear_playlist()

        for n in reversed([globals.current_mode.head] \
            + globals.current_mode.head.neighbours_after):
        #___
            self.prepend_song(n)

        self._next_songs.appendleft(self._past_songs.pop())

        for n in globals.current_mode.head.neighbours_before:
            self._past_songs.append(n)

        self.jump_to_next_song()
        self.play()


    ##
    #   @brief
    def unqueue_next(self):
        self._send(['-C', 'player-next'])


    ##
    #   @brief
    def remove_current_song(self):
        self._past_songs.pop()


    ##
    #   @brief
    def play_playlist(self):
        self._send(['-C', 'player-next'])
        self.play()


    ##
    #   @brief
    def play(self):
        mdLog.debug("sending order to PLAY!")

        globals.cmus_playing_notifications_disabled = True
        self._send(['-p'])


    ##
    #   @brief
    def stop(self):
        mdLog.debug("sending STOP")

        self._send(['-s'])

        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._next_songs]))


    ##
    #   @brief
    def toggle_pause(self):
        mdLog.debug("sending PAUSE")
        self._send(['-u'])


    ##
    #   @brief  Sends the given command to cmus, via cmus-remote
    #   @param  cmd_list a list of chains
    def _send(self, cmd_list):
        mdLog.debug('sending ' + str(cmd_list) + ' via cmus-remote')
        subprocess.Popen(['cmus-remote',
                          '--server',
                          SOCKETS_CONFIG['TO_CMUS']['FILE']
                         ]
                         + cmd_list)


    ##
    #   @brief To be sure to quit cmus safely, whatever happens. An __enter__()
    #          and an __exit__() methods are required to be able to use the
    #          object in a with statement.
    def __enter__(self):
        return self


    ##
    #   @brief To be sure to quit cmus safely, whatever happens. An __enter__()
    #          and an __exit__() methods are required to be able to use the
    #          object in a with statement.
    def __exit__(self, type, value, traceback):
        ##
        #   @todo   Send the quit signal to cmus
        pass

