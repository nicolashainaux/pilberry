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
# @class View_head
# @brief Gathers the methods to view the head data
class View_head(View_infos):


    ##
    #   @brief
    def set_view_head(self):
        pass


    ##
    #   @brief
    def set_view_xnode(self):
        self.set_view('View_xnode')
        self.update()


    ##
    #   @brief
    def update(self, **options):
        # Desired way of testing if the new and the old infos are the same
        # or not, instead of what we actually must do, so far:
        #if self.infos_past['head_name'] == None \
        #or self.infos['head'].full_path != self.infos_past['head'].full_path:

        if self.infos_past['head_name'] != self.infos['head_name'] \
        or self.infos_past['head_parent'] != self.infos['head_parent']:
            self.lcd.clear()
            self.lcd.message(self.infos['head_parent'][0:16]+"\n")
            self.lcd.message(self.infos['head_name'][0:16])
