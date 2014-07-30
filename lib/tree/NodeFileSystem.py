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

# Pilberry packages|modules imports
from .Node import Node
from lib.utils import natural_sort
from lib.globals import USER_CONFIG


##
# @class NodeFileSystem
# @brief These nodes will be built from file system informations
class NodeFileSystem(Node):


    ##
    #   @brief  Checks if current Node is really a leaf, according to the
    #           chosen view.
    #   @return Boolean
    #   @param  full_path   The full path of the file or directory to test
    #   @todo   Maybe find a way to treat an empty directory not as a leaf
    #           but in order to do that, a special Node (emptyNode?) has to be
    #           created and the rest of the code has to be adapted to be able
    #           to deal with it.
    @staticmethod
    def is_a_leaf(full_path):
        # /!\ Check the comment in Node.is_a_leaf() before changing this
        # A non-empty directory will be treated as an inode (False)
        # all other cases are leaves (True)
        if os.path.isdir(full_path) and len(os.listdir(full_path)) != 0:
            return False
        else:
            return True



    ##
    #   @brief  Gets the children list of a Node, as filenames or directory names.
    #           Returns [] if the node has no children. Should be called only
    #           on non-leaves nodes.
    #   @return List
    #   @param  full_path   The full path of directory to test
    #   @todo   Maybe check full_path is a path to a directory.
    @staticmethod
    def get_children_list(full_path):
        if USER_CONFIG['GENERAL'].getboolean('SHOW_FILES_FIRST'):
            return natural_sort(next(os.walk(full_path))[2]) \
                   + natural_sort(next(os.walk(full_path))[1])
        else:
            return natural_sort(next(os.walk(full_path))[1]) \
                   + natural_sort(next(os.walk(full_path))[2])






