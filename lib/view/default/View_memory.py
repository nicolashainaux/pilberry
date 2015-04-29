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
from abc import ABCMeta, abstractmethod

# Pilberry packages|modules imports
#from lib.globals import SOCKETS_CONFIG, USER_CONFIG
from .View_infos import View_infos


##
# @class View_memory
# @brief Gathers the methods to view the xnode data
class View_memory(View_infos):


    ##
    #   @brief
    #def set_view_head(self):
    #    self.set_view('View_head')
    #    self.update()


    ##
    #   @brief
    #def set_view_xnode(self):
    #    pass


    ##
    #   @brief
    def update(self, **options):
        if self.infos_past['xnode_name'] != self.infos['xnode_name'] \
        or self.infos_past['xnode_parent'] != self.infos['xnode_parent']:
            self.lcd_message(self.infos['xnode_parent'], 0)
            self.lcd_message(self.infos['xnode_name'], 1)
