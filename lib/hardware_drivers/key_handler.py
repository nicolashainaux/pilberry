#!/usr/bin/env python3
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

# This file describes the KeyHandler class

# Python packages|modules imports
import time
import logging

# Pilberry packages|modules imports
from lib.globals import GENERAL_CONFIG
from lib.carrier.Carrier import Carrier

LONG_CLICK_DELAY = float(GENERAL_CONFIG['CLICK_DELAYS']['LONG'])
DOUBLE_CLICK_DELAY = float(GENERAL_CONFIG['CLICK_DELAYS']['DOUBLE'])
BUTTON = GENERAL_CONFIG['BUTTON_IDS']
SHORT_CLICK_ID = GENERAL_CONFIG['CLICK_IDS']['SINGLE_SHORT']
LONG_CLICK_ID = GENERAL_CONFIG['CLICK_IDS']['SINGLE_LONG']
DOUBLE_CLICK_ID = GENERAL_CONFIG['CLICK_IDS']['DOUBLE']

keypadLog = logging.getLogger('keypadLog')

##
# @class KeyHandler
# @brief
class KeyHandler(object):


    with Carrier() as C:
        ##
        #   @brief
        def __init__(self, key_id):
            self._key_id = key_id
            self._cmd = 'CMD_' + BUTTON[key_id]
            self._state = self.state_initial
            self._time = time.time()



        ##
        #   @brief
        def get_key_id(self):
            return self._key_id


        ##
        #   @brief
        def get_time(self):
            return self._time


        ##
        #   @brief
        def get_cmd(self):
            return self._cmd


        key_id = property(get_key_id,
                          doc="The key's id, like SELECT, LEFT, UP, etc.")
        time = property(get_time,
                        doc="Time the current state was set.")

        cmd = property(get_cmd,
                       doc="Begining of the CMD_ command associated to button.")


        ##
        #   @brief
        def set_state(self, new_state):
            self._time = time.time()
            self._state = new_state
            keypadLog.debug("state set to: " + self._state.__name__)


        ##
        #   @brief
        def handle(self, is_pressed):
            self._state(is_pressed)


        ##
        #   @brief
        def state_initial(self, is_pressed):
            if is_pressed:
                self.set_state(self.state_single_click)


        ##
        #   @brief
        def state_single_click(self, is_pressed):
            if not is_pressed:
                if time.time() - self.time > LONG_CLICK_DELAY:
                    #C.send('KEYPAD_TO_CORE',
                           #self.cmd + LONG_CLICK_ID)
                    keypadLog.debug("sending \033[32mLONG CLICK\033[0m")
                    self.set_state(self.state_initial)

                else:
                    self.set_state(self.state_provisional)


        ##
        #   @brief
        def state_provisional(self, is_pressed):
            if not is_pressed:
                if time.time() - self.time \
                    > DOUBLE_CLICK_DELAY:
                #___
                    #C.send('KEYPAD_TO_CORE',
                    #       self.cmd + SHORT_CLICK_ID)
                    keypadLog.debug("sending \033[34mSHORT CLICK\033[0m")
                    self.set_state(self.state_initial)
            else:
                #C.send('KEYPAD_TO_CORE',
                #       self.cmd + DOUBLE_CLICK_ID)
                keypadLog.debug("sending \033[31mDOUBLE CLICK\033[0m")
                self.set_state(self.state_double_click)


        ##
        #   @brief
        def state_double_click(self, is_pressed):
            if not is_pressed:
                self.set_state(self.state_initial)

