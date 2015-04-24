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
import os
import socket
import configparser
import pickle

# Pilberry packages|modules imports
from lib.globals import SOCKETS_CONFIG

##
# @class Carrier
# @brief Carrier objects are dedicated to 'pack' and transmit data
#        to a given address
class Carrier(object):

    ##
    #   @brief This initializer creates the dictionnary of available sockets.
    #          This dictionnary will be filled only if necessary, by send().
    def __init__(self):
        self._sockets_enabled = {}

    ##
    #   @brief Connects to the destination socket if it is not connected yet,
    #          then 'packs' and sends the data.
    def send(self, dest, data):
        if not dest in self._sockets_enabled.keys():
            if SOCKETS_CONFIG[dest]['TYPE'] == 'TCP_IP':
                self._sockets_enabled[dest] = socket.socket(socket.AF_INET,
                                                            socket.SOCK_STREAM)

                ##
                # @todo Check if the connection works
                #       and handle the possible exception
                self._sockets_enabled[dest].connect((\
                                            str(SOCKETS_CONFIG[dest]['IP']),
                                            int(SOCKETS_CONFIG[dest]['PORT'])))


            ##
            # @todo Maybe check if the type is 'UNIX' and not anything else (
            #       would be wrong)
            else:
                self._sockets_enabled[dest] = socket.socket(socket.AF_UNIX,
                                                            socket.SOCK_DGRAM)

                ##
                # @todo Check if the connection works
                #       and handle the possible exception
                self._sockets_enabled[dest].connect(\
                                            str(SOCKETS_CONFIG[dest]['FILE']))


        self._sockets_enabled[dest].send(pickle.dumps(data))

    ##
    #   @brief To be sure to close the connections, whatever happens, we must
    #          define an __enter__() and an __exit__() methods in order to be
    #          able to use the object in a with statement.
    def __enter__(self):
        return self

    ##
    #   @brief To be sure to close the connections, whatever happens, we must
    #          define an __enter__() and an __exit__() methods in order to be
    #          able to use the object in a with statement.
    def __exit__(self, type, value, traceback):
        for dest in self._sockets_enabled:
            self._sockets_enabled[dest].shutdown(socket.SHUT_RDWR)
            self._sockets_enabled[dest].close()
            if SOCKETS_CONFIG[dest]['TYPE'] == 'UNIX':
                os.remove(str(SOCKETS_CONFIG[dest]['FILE']))

