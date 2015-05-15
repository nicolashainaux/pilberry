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
#import logging

# Adafruit packages|modules imports
from lib.hardware_drivers.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Pilberry packages|modules imports
#from lib.globals import current_mode_id, MODES_CONFIG, USER_CONFIG
import lib.globals as globals

import lib.view.default as display_view
VIEWS_LIST = ['View_memory']


##
# @class View
# @brief
class View(object):


    ##
    #   @brief
    def __init__(self, **options):
        #self._view_type = 'FILE_SYSTEM'

        self._lcd = Adafruit_CharLCDPlate()

        # The default view could be chosen from the config file
        self._view = 'View_memory'

        # The two fields will be Node objects
        self._infos = { 'xnode_name' : None,
                        'xnode_parent' : None
                      }

        self._infos_past = { 'xnode_name' : None,
                             'xnode_parent' : None
                           }

        self._HANDLE = {}

        ##
        #   @todo   Check the names there below, ensure the States names match
        #           Mode.STATES_LIST
        for v in VIEWS_LIST:
            self._HANDLE[v] = \
        {'UPDATE' : getattr(display_view, v).update,
         'State_A' : getattr(display_view, v).State_A,
         'State_B' : getattr(display_view, v).State_B,
         'State_C' : getattr(display_view, v).State_C,
         'State_D' : getattr(display_view, v).State_D
        }


    ##
    #   @brief
    #def get_view_type(self):
    #    return self._view_type


    ##
    #   @brief
    def get_infos(self):
        return self._infos


    ##
    #   @brief
    def get_infos_past(self):
        return self._infos_past


    ##
    #   @brief
    def get_view(self):
        return self._view


    ##
    #   @brief
    def get_HANDLE(self):
        return self._HANDLE


    #view_type = property(get_view_type,
    #                     doc="...")
    view = property(get_view,
                    doc="The current View")
    HANDLE = property(get_HANDLE,
                     doc="The HANDLE field")
    infos = property(get_infos,
                     doc="Current infos about xnode and head")
    infos_past = property(get_infos_past,
                     doc ="Previous infos about xnode and head")



    ##
    #   @brief
    #def set_view(self, v):
        ##
        #   @todo   Check that the argument v belongs to the 'authorized' views
    #    logging.debug("setting view at: " + v)
    #    self._view = v


    ##
    #   @brief
    def set_infos_memory(self, new_infos):
        self._infos_past['xnode_name'] = self._infos['xnode_name']
        self._infos['xnode_name'] = new_infos['xnode_name']

        self._infos_past['xnode_parent'] = self._infos['xnode_parent']
        self._infos['xnode_parent'] = new_infos['xnode_parent']


    ##
    #   @brief
    def handle(self, info, **options):
        self.HANDLE[self._view][info](self, **options)


    ##
    #   @brief
    def lcd_clear(self):
        self._lcd.clear()


    ##
    #   @brief  This method is used to send a message "safely" to the LCD. Some
    #           encoding errors did not trigger any error in pilberry, but they
    #           did later in the LCD driver.
    #   @todo   Check if line == 0 or line == 1
    def lcd_message(self, msg, line):
        bmsg = msg.encode('utf-8', 'replace')

        if b'\xef\xbf\xbd' in bmsg:
                bmsg = msg.encode('ascii', 'replace')

        msg = bmsg.decode()

        self._lcd.setCursor(0,line)

        carriage_return = "\n" if line == 0 else ""

        # We send the 16 first chars of (the msg added to 16 spaces), to display
        # either the 16 first chars of a msg that would be longer than 16 chars,
        # or all the msg plus the right number of spaces to delete the possibly
        # remaining chars of the string previously displayed
        self._lcd.message((msg + "                ")[0:16] + carriage_return)



    ##
    #   @brief
    def lcd_set_play_indicator(self):
        self._lcd.setCursor(15, 1)
        self._lcd.noCursor()
        self._lcd.blink()


    ##
    #   @brief
    def lcd_set_pause_indicator(self):
        pass

    ##
    #   @brief
    def lcd_set_explore_indicator(self):
        self._lcd.setCursor(15, 1)
        self._lcd.noBlink()
        self._lcd.cursor()

    ##
    #   @brief
    def lcd_set_no_indicator(self):
        self._lcd.setCursor(15, 1)
        self._lcd.noBlink()
        self._lcd.noCursor()

