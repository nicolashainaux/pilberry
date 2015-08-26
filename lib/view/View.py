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
from lib.utils import current_milli_time

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

        self._short_message = ""

        self._volume_info = ""

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

        self._core_state = 'State_A'

        self._volume_display_elapsed_time = current_milli_time()


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
    def get_volume_display_elapsed_time(self):
        return self._volume_display_elapsed_time


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
    volume_display_elapsed_time = property(get_volume_display_elapsed_time,
                                           doc = "Over this time, volume info"\
                                                 + " shouldn't be displayed" \
                                                 + " any longer.")



    ##
    #   @brief
    #def set_view(self, v):
        ##
        #   @todo   Check that the argument v belongs to the 'authorized' views
    #    logging.debug("setting view at: " + v)
    #    self._view = v


    ##
    #   @brief
    def reset_volume_display_elapsed_time(self):
        self._volume_display_elapsed_time = current_milli_time() + 100


    ##
    #   @brief
    def set_infos_memory(self, new_infos):
        self._infos_past['xnode_name'] = self._infos['xnode_name']
        self._infos['xnode_name'] = new_infos['xnode_name']

        self._infos_past['xnode_parent'] = self._infos['xnode_parent']
        self._infos['xnode_parent'] = new_infos['xnode_parent']


    ##
    #   @brief
    def set_short_message(self, new_infos):
        self._short_message = new_infos


    ##
    #   @brief
    def reset_short_message(self):
        self._short_message = ""


    ##
    #   @brief
    def set_volume_info(self, new_infos):
        self._volume_info = new_infos


    ##
    #   @brief
    def reset_volume_info(self):
        self._volume_info = ""


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
    def lcd_message(self, msg, line, **options):
        cursor_position = 0
        if 'last_chars' in options \
            and type(options['last_chars']) == int:
        #___
            cursor_position = 16 - options['last_chars']

        bmsg = msg.encode('utf-8', 'replace')

        if b'\xef\xbf\xbd' in bmsg:
                bmsg = msg.encode('ascii', 'replace')

        msg = bmsg.decode()

        self._lcd.setCursor(cursor_position, line)

        carriage_return = "\n" if line == 0 else ""

        # We send the 16 first chars of (the msg added to 16 spaces), to display
        # either the 16 first chars of a msg that would be longer than 16 chars,
        # or all the msg plus the right number of spaces to delete the possibly
        # remaining chars of the string previously displayed
        if cursor_position == 0:
            self._lcd.message((msg + "                ")[0:16] + carriage_return)
        else:
            self._lcd.message(msg[len(msg) - options['last_chars']:] \
                                                               + carriage_return)



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

    ##
    #   @brief
    def lcd_set_indicator(self):
          self.handle(self._core_state)


    ##
    #   @brief
    #   @todo   The list of the states' names should be a constant somewhere.
    #           It is also used in __init__()
    def store_core_state(self, info):
        if info in ['State_A', 'State_B', 'State_C', 'State_D']:
            self._core_state = info

