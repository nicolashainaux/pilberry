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
import socket
import configparser
import pickle

# Pilberry packages|modules imports
from lib.globals import SOCKETS_CONF


class Carrier(object):

    def __init__(self):
        self._sockets_available = configparser.ConfigParser()
        self._sockets_available.read(SOCKETS_CONF)
        self._sockets_enabled = {}


    def send(self, dest, data):
        if not dest in self._sockets_enabled.keys():
            self._sockets_enabled[dest] = socket.socket(socket.AF_INET,
                                                        socket.SOCK_STREAM)

            ##
            # @todo Check if the connection works
            #       and handle the possible exception

            self._sockets_enabled[dest].connect((\
                                    str(self._sockets_available[dest]['IP']),
                                    int(self._sockets_available[dest]['PORT'])))


        self._sockets_enabled[dest].send(pickle.dumps(data))


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        for dest in self._sockets_enabled:
            self._sockets_enabled[dest].close()
