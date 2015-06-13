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
        self._songs_queue = deque()
        self._past_songs = deque()
        #self._current_song = []


    ##
    #   @brief
    def get_current_song(self):
        #return self._current_song[0]
        if len(self._past_songs) >= 1:
            return self._past_songs[len(self._past_songs) - 1]
        else:
            return {'file_name' : "(No song)"}


    current_song = property(get_current_song,
                            doc="The Mode's MusicDriver")


    ##
    #   @brief
    def set_current_song(self, n):
        self._past_songs.append(n)


    ##
    #   @brief
    def queue_song(self, n):
        mdLog.debug('queuing song: ' + n['file_name'])
        self._songs_queue.append(n)
        self._send(['-C', 'add -q ' + n.full_path])
        mdLog.debug('current song: ' \
                    + self.current_song['file_name'])
        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._songs_queue]))


    ##
    #   @brief
    def queue_song_first(self, n):
        mdLog.debug('queuing song first: ' + n['file_name'])
        self._songs_queue.appendleft(n)
        self._send(['-C', 'add -Q ' + n.full_path])
        mdLog.debug('current song: ' \
                    + self.current_song['file_name'])
        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._songs_queue]))


    ##
    #   @brief
    def requeue_current_song_first(self):
        mdLog.debug('requeuing current song first')
        self._send(['-C', 'add -Q ' + self.current_song.full_path])


    ##
    #   @brief  This is only used to synchronize pilberry's queue with cmus'.
    #           cmus has already unqueued the song, so this method only deals
    #           with pilberry's queue.
    def unqueue_song_first(self):
        mdLog.debug('unqueuing first song: ')
        if not self.queue_is_empty():
            self.set_current_song(self._songs_queue.popleft())
        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._songs_queue]))


    ##
    #   @brief
    def queue_is_empty(self):
        if len(self._songs_queue) == 0:
            return True
        else:
            return False



    ##
    #   @brief
    def queue_past_is_empty(self):
        # Remember the song at the right of past_songs is actually current_song
        # so we check if there are other songs before it.
        if len(self._past_songs) <= 1:
            return True
        else:
            return False



    ##
    #   @brief
    def clear_queue(self):
        mdLog.debug('queue is being cleared')
        self._songs_queue.clear()
        self._past_songs.clear()
        self._send(['-c', '-q'])
        mdLog.debug('current song: ' \
                    + self.current_song['file_name'])
        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._songs_queue]))


    ##
    #   @brief
    def skip_to_next_song(self):
        mdLog.debug('skip to next song')
        self._past_songs.append(self._songs_queue.popleft())
        self._send(['-C', 'player-next'])
        mdLog.debug('current song: ' \
                    + self.current_song['file_name'])
        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._songs_queue]))
        globals.cmus_playing_notifications_disabled = True


    ##
    #   @brief
    def skip_to_prev_song_in_queue(self):
        mdLog.debug('skip to prev song in queue')
        if len(self._past_songs) >= 2:
            self.queue_song_first(self._past_songs.pop())
            self.requeue_current_song_first()
            self._send(['-C', 'player-next'])
            mdLog.debug('current song: ' \
                        + self.current_song['file_name'])
            mdLog.debug('past songs: ' \
                        + str([n['file_name'] for n in self._past_songs]))
            mdLog.debug('future songs: ' \
                        + str([n['file_name'] for n in self._songs_queue]))
            globals.cmus_playing_notifications_disabled = True


    ##
    #   @brief
    def start_playing(self):
        self.clear_queue()
        for n in reversed([globals.current_mode.head] \
            + globals.current_mode.head.neighbours_after):
        #___
            self.queue_song_first(n)

        for n in globals.current_mode.head.neighbours_before:
            self._past_songs.append(n)

        self.play()


    ##
    #   @brief
    def start_playing_queue(self):
        if len(self._past_songs) >= 1:
            self._past_songs.reverse()
            self._songs_queue.extendleft(self._past_songs)
            self._past_songs.clear()

        # Clearing and repopulating cmus' queue
        self._send(['-c', '-q'])
        for n in self._songs_queue:
            self._send(['-C', 'add -q ' + n.full_path])

        self.play()


    ##
    #   @brief
    def play(self):
        self.skip_to_next_song()
        mdLog.debug("sending order to PLAY!")

        globals.cmus_playing_notifications_disabled = True

        self._send(['-p'])


    ##
    #   @brief
    #def start_playing_after_delay(self):

        #self.stop()

    #    q = []
    #    for n in [globals.current_mode.head] \
    #        + globals.current_mode.head.neighbours_after:
        #___
    #        q += [n.full_path]

        #try:
        #    killall = subprocess.Popen(['killall', 'roger_roger'])
        #except:
        #    logging.debug('no roger_roger was here')
        #else:
        #    logging.debug('killed roger_roger')

    #    r = subprocess.Popen([ROGER_ROGER_SCRIPT] + q)

     #   logging.debug('after having sent a new roger_roger')


    ##
    #   @brief
    def stop(self):
        mdLog.debug("sending STOP")
        #self._songs_queue.popleft()
        #self._current_song = []
        self._send(['-s'])
        mdLog.debug('current song: ' \
                    + self.current_song['file_name'])
        mdLog.debug('past songs: ' \
                    + str([n['file_name'] for n in self._past_songs]))
        mdLog.debug('future songs: ' \
                    + str([n['file_name'] for n in self._songs_queue]))


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

