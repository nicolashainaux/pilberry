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
from .Node import Node


##
# @class Tree
# @brief
class Tree(object):

    ##
    #   @brief
    #   @param  id : this will be the id of the root node, has to be taken
    #                from the database
    #                We could change it for just the root_path/, what
    #                will be accessible from the conf file, and let
    #                __init__() itself get the matching id from the database
    def __init__(self, id):
        # We'll first define the children until a depth of 2: e.g. the first
        # level directly under the root, and their children also (like the
        # level "Artists" + the level "Albums")
        self._nodes = Node(None, id, 0, 2)
        self._current_depth = 0
        # We set current_node as the first node found in root/,
        # otherwise we'll have to enter root to see anything
        self._neighbours_list = self._nodes.children
        self._current_node = self._nodes.children[0]



    ##
    #   @brief
    def get_current_node(self):
        return self._current_node

    ##
    #   @brief
    def get_current_depth(self):
        return self._current_depth

    current_node = property(get_current_node, doc="Current Node in the Tree")
    current_depth = property(get_current_depth, doc="Current depth in the Tree")


    ##
    #   @brief  Moves to the parent Node. Returns the new current Node.
    #   @return Node
    def move_to_parent(self):
        if self.current_node.parent != None:
            self._current_node = self.current_node.parent
            self._current_depth -= 1
            if self.current_node.parent != None:
                self._neighbours_list = self.current_node.parent.children
            else:
                self._neighbours_list = [self]

        return self.current_node



    ##
    #   @brief
    def move_to_next_node(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.current_node.position + 1) \
                                                    % len(self._neighbours_list)
        self._current_node = self._neighbours_list[new_position]
        # self._neighbours_list remains the same

        return self.current_node



    ##
    #   @brief
    def move_to_prev_node(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.current_node.position - 1) \
                                                    % len(self._neighbours_list)
        self._current_node = self._neighbours_list[new_position]
        # self._neighbours_list remains the same

        return self.current_node



    ##
    #   @brief
    def move_to_first_child(self):
        # There it is not useful to use the is_a_leaf() method because
        # we don't need to make a request in the DB. If there are children,
        # they are already here. So just check len(children)
        if len(self.current_node.children) >= 1:
            for n in self.current_node.children:
                n.add_children(1)
            self._neighbours_list = self.current_node.children
            self._current_node = self.current_node.children[0]
            self._current_depth += 1

        return self.current_node



    ##
    #   @brief
    def jump_to_1st_child_of_next_parent(self):
        self.move_to_parent()
        self.move_to_next_node()
        # To be sure we are not unfortunately on a leaf:
        # (this loop should end because we just came from a node that's not
        # a leaf, in the worst case, we come back into it)
        while len(self.current_node.children) == 0:
            self.move_to_next_node()
        return self.move_to_first_child()



    ##
    #   @brief
    def jump_to_1st_child_of_prev_parent(self):
        self.move_to_parent()
        self.move_to_prev_node()
        # To be sure we are not unfortunately on a leaf:
        # (this loop should end because we just came from a node that's not
        # a leaf, in the worst case, we come back into it)
        while len(self.current_node.children) == 0:
            self.move_to_prev_node()
        return self.move_to_first_child()


