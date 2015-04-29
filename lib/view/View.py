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
                        'xnode_parent' : None,
                        'head_name' : None,
                        'head_parent' : None
                      }

        self._infos_past = { 'xnode_name' : None,
                             'xnode_parent' : None,
                             'head_name' : None,
                             'head_parent' : None
                           }

        self._HANDLE = {}

        for v in VIEWS_LIST:
            self._HANDLE[v] = \
        {'UPDATE' : getattr(display_view, v).update
        #,
         #'SET_VIEW_XNODE' : getattr(display_view, v).set_view_xnode,
         #'SET_VIEW_HEAD' : getattr(display_view, v).set_view_head
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
    #def get_lcd(self):
    #    return self._lcd


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
    #lcd = property(get_lcd,
    #                doc="The LCD object")
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
    #def set_infos_head(self, new_infos):
    #    self._infos_past['head_name'] = self._infos['head_name']
    #    self._infos['head_name'] = new_infos['head_name']

    #    self._infos_past['head_parent'] = self._infos['head_parent']
    #    self._infos['head_parent'] = new_infos['head_parent']


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

        self._lcd.message((msg + "                ")[0:16] + carriage_return)



