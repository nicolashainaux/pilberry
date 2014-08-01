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
import logging

# Pilberry packages|modules imports
import lib.globals as globals
from lib.globals import SOCKETS_CONFIG


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
    #def play_songs(self, full_paths_list):
    #    for s in full_paths_list:
    #        self._send(['-q', s])
    #
    #    self._send(['-p'])

    ##
    #   @brief
    def add_playlist(self, full_path):
        self._send(['-C', 'add -q ' + full_path])


    ##
    #   @brief
    def clear_queue(self):
        self._send(['-c', '-q'])

    ##
    #   @brief
    def skip_to_next_song(self):
        self._send(['-C', 'player-next'])


    ##
    #   @brief
    def start_playing(self):
        self.clear_queue()
        for n in globals.current_tree.current_neighbours_after:
            self.add_playlist(n.full_path)

        self.skip_to_next_song()
        self._send(['-p'])


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
                          SOCKETS_CONFIG['CMUS']['FILE']
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

