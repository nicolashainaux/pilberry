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

# Pilberry packages|modules imports
import lib.globals as globals
from lib.globals import SOCKETS_CONFIG, AUDIO_FEEDBACK_LOCK_FILE


##
# @class MusicDriver
# @brief The MusicDriver will drive the music player
class MusicDriver(object):


    ##
    #   @brief
    def __init__(self):
        self._songs_queue = ['']


    ##
    #   @brief
    def queue(self, full_path):
        logging.debug('queuing: ' + full_path)
        self._send(['-C', 'add -q ' + full_path])


    ##
    #   @brief
    def queue_first(self, full_path):
        logging.debug('queuing: ' + full_path)
        self._send(['-C', 'add -Q ' + full_path])


    ##
    #   @brief
    def clear_queue(self):
        logging.debug('queue is being cleared')
        self._send(['-c', '-q'])

    ##
    #   @brief
    def skip_to_next_song(self):
        self._send(['-C', 'player-next'])


    ##
    #   @brief
    def start_playing(self):
        self.clear_queue()
        for n in [globals.current_mode.head] \
            + globals.current_mode.head.neighbours_after:
        #___
            self.queue(n.full_path)

        self.skip_to_next_song()
        logging.debug("sending order to PLAY!")

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
        self._send(['-s'])



    ##
    #   @brief
    def toggle_pause(self):
        self._send(['-u'])



    ##
    #   @brief  Sends the given command to cmus, via cmus-remote
    #   @param  cmd_list a list of chains
    def _send(self, cmd_list):
        logging.debug('sending ' + str(cmd_list) + ' via cmus-remote')
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

