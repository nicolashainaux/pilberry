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


##
# @class View_infos
# @brief Mother class of View_xnode and View_head,
#        possibly later of View_settings and View_radio too
class View_infos(object, metaclass=ABCMeta):

    ##
    #   @brief
    def State_A(self):
        pass


    ##
    #   @brief
    def State_B(self):
        pass


    ##
    #   @brief
    def State_C(self):
        pass


    ##
    #   @brief
    @abstractmethod
    def update(self, **options):
        pass


    ##
    #   @brief
    def no_action(self, **options):
        pass
