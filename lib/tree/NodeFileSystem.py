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


# Pilberry packages|modules imports
from . import Node


##
# @class NodeFileSystem
# @brief These nodes will be built from file system informations
class NodeFileSystem(Node):

    ##
    #   @brief
    #   @param  parent : the parent Node
    #   @param  full_path : the full path of the file
    #   @param  position : the position among the neighbours' list
    #   @param  view : the view type (e.g. file system, album/artist etc.)
    #   @param  add_children : int that tells how deep we should add children
    def __init__(self, parent, full_path, position, view, add_children):
        Node.__init__(self, parent, full_path, position, view, add_children)



    ##
    #   @brief  Checks if current Node is actually a leaf
    def is_a_leaf(self):
        # /!\ Take care, this should not only be:
        #return len(self._children) == 0
        # This should actually check, in the database, if self has really
        # children or not, according to the current view

        # /!\ MAYBE this would be better a (class?) method, because
        # it is useful in many situations, including in __init__()




    parent = property(get_parent, doc="Parent Node")
    children = property(get_children, doc="Children Nodes, if any")
    full_path = property(get_full_path, doc="The full patht to the file or "\
                                            + "directory. Will also be a unique"\
                                            + " identifier.")
    position = property(get_position, doc="Position of the Node among " \
                                         + "its brothers")


    ##
    #   @brief
    def add_children(self, depth):
        if not self.is_a_leaf():
            # define all what children would be, according to the chosen view
            # and add them to self._children
            # should be same algorithm as in __init__()
            # depth is an int. if depth == 0, do nothing, if depth > 0,
            # then call recursively add_children on each child, with depth - 1
