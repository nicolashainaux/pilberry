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
import logging

# Pilberry packages|modules imports
from .Node import Node
from .NodeFileSystem import NodeFileSystem
# from .NodeDataBase import NodeDataBase
from lib.globals import current_mode, MODES_CONFIG, USER_CONFIG

##
# @class Tree
# @brief
class Tree(object):

    ##
    #   @brief
    #   @todo   When the NodeDataBase will get used, remember to uncomment the
    #           matching lines
    def __init__(self, **options):
        # We'll first define the children until a depth of 2: e.g. the first
        # level directly under the root, and their children also (like the
        # level "Artists" + the level "Albums")

        node_class = NodeFileSystem
        self._view_type = 'FILE_SYSTEM'

        if USER_CONFIG['VIEW']['ALL'] == '':
            if USER_CONFIG['VIEW'][current_mode] == '':
                if USER_CONFIG['VIEW']['DEFAULT'] != '':
                    if USER_CONFIG['VIEW']['DEFAULT'] != 'FILE_SYSTEM':
                        #node_class = NodeDataBase
                        self._view_type = USER_CONFIG['VIEW']['DEFAULT']
            elif USER_CONFIG['VIEW'][current_mode] != 'FILE_SYSTEM':
                #node_class = NodeDataBase
                self._view_type = USER_CONFIG['VIEW'][current_mode]

        elif USER_CONFIG['VIEW']['ALL'] != 'FILE_SYSTEM':
            #node_class = NodeDataBase
            self._view_type = USER_CONFIG['VIEW']['ALL']

        root_path = MODES_CONFIG[current_mode]['ROOT_PATH']
        if 'root' in options:
            root_path = options['root']


        self._nodes = node_class(None,
                                 root_path,
                                 0,
                                 self._view_type,
                                 2)


        # We set read_head as the first node found in root/,
        # otherwise we'll have to enter root to see anything
        self._neighbours_list = self._nodes.children
        self._xneighbours_list = self._nodes.children

        s = str(type(self._nodes))
        logging.debug("root node's type is: "\
                     + s[s.rfind('.')+1:-2] \
                     + " its name is: " \
                     + self._nodes['file_name'] \
                     + " and it has: " \
                     + str(len(self._nodes.children)) \
                     + " children.")

        ##
        #   @todo   Check if there is one child at least!
        self._read_head = self._nodes.children[0]
        self._xnode = self._nodes.children[0]

        logging.debug("initialized read_head at: " \
                      + self._read_head['file_name'])

        ##
        #   @todo   Maybe initialize it to 1, because we did not set the
        #           view to / but to the first child of /
        self._read_head_depth = 0
        self._xdepth = 0


    ##
    #   @brief
    def get_read_head(self):
        return self._read_head

    ##
    #   @brief
    def get_xnode(self):
        return self._xnode

    ##
    #   @brief
    def get_read_head_depth(self):
        return self._read_head_depth


    ##
    #   @brief
    def get_xdepth(self):
        return self._xdepth


    ##
    #   @brief
    def get_view_type(self):
        return self._view_type


    ##
    #   @brief
    def get_rh_neighbours(self):
        return self._neighbours_list

    ##
    #   @brief
    def get_xneighbours(self):
        return self._xneighbours_list

    ##
    #   @brief Returns the list of self + all neighbours after me
    def get_rh_neighbours_after(self):
        return self._neighbours_list[\
                          self.read_head.position:len(self._neighbours_list)]



    ##
    #   @brief Returns the list of neighbours before me (but not me)
    def get_rh_neighbours_before(self):
        return self._neighbours_list[0:self.read_head.position]




    read_head = property(get_read_head,
                         doc="Read Head position (node of the Tree)")
    xnode = property(get_xnode,
                     doc="XNode is the 'explorer node' of the Tree")
    read_head_depth = property(get_read_head_depth,
                             doc="Current depth in the Tree")
    xdepth = property(get_xdepth,
                      doc="Current xdepth in the Tree")
    view_type = property(get_view_type,
                         doc="View type of the Tree")
    rh_neighbours = property(get_rh_neighbours,
                          doc="All nodes at the same floor as current")
    xneighbours = property(get_xneighbours,
                          doc="All nodes at the same floor as current x")
    rh_neighbours_after = property(get_rh_neighbours_after,
                          doc="All nodes at the same floor as current, " \
                              "after current, including current")
    rh_neighbours_before = property(get_rh_neighbours_before,
                          doc="All nodes at the same floor as current, " \
                              "before current, but not current")


    ##
    #   @brief
    def set_read_head(self, n):
        self._read_head = n

    ##
    #   @brief
    def set_xnode(self):
        return self._read_head

    ##
    #   @brief  Moves to the parent Node. Returns the new current Node.
    #   @return Node
    def move_to_parent(self):
        # self.read_head.parent should never be None because we forbid
        # to access the root directory
        # So, self.read_head.parent.parent != None
        # is equivalent to 'self.parent is not root'
        if self.read_head.parent.parent != None:
            self._read_head = self.read_head.parent
            self._read_head_depth -= 1
            self._neighbours_list = self.read_head.parent.children

        return self.read_head



    ##
    #   @brief  Moves xNode to its parent Node. Returns the new current xNode.
    #   @return Node
    def movex_to_parent(self):
        # self.xnode.parent should never be None because we forbid
        # to access the root directory
        # So, self.xnode.parent.parent != None
        # is equivalent to 'self.parent is not root'
        if self.xnode.parent.parent != None:
            self._xnode = self.xnode.parent
            self._xdepth -= 1
            self._xneighbours_list = self.xnode.parent.children

        return self.xnode



    ##
    #   @brief
    def move_to_next_node(self, nb_step=1):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.read_head.position + nb_step) \
                                                    % len(self._neighbours_list)
        self._read_head = self._neighbours_list[new_position]
        # self._neighbours_list remains the same

        return self.read_head



    ##
    #   @brief
    def movex_to_next_node(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position + 1) \
                                                    % len(self._xneighbours_list)
        self._xnode = self._xneighbours_list[new_position]
        # self._neighbours_list remains the same

        return self.read_head



    ##
    #   @brief
    def move_to_prev_node(self, nb_step=1):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.read_head.position - nb_step) \
                                                    % len(self._neighbours_list)
        self._read_head = self._neighbours_list[new_position]
        # self._neighbours_list remains the same

        return self.read_head



    ##
    #   @brief
    def movex_to_prev_node(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position - 1) \
                                                    % len(self._xneighbours_list)
        self._xnode = self._xneighbours_list[new_position]
        # self._neighbours_list remains the same

        return self.xnode



    ##
    #   @brief
    def move_to_1st_child(self):
        # There it is not useful to use the is_a_leaf() method because
        # we don't need to check the filesystem neither to make a request
        # in the DB. If there are children, they are already here.
        # So just check len(children)
        if len(self.read_head.children) >= 1:
            for n in self.read_head.children:
                if (not n.is_a_leaf(n.full_path) and len(n.children) == 0):
                    n.add_children(1)
            self._neighbours_list = self.read_head.children
            self._read_head = self.read_head.children[0]
            self._read_head_depth += 1
            self._xneighbours_list = self._neighbours_list
            self._xnode = self.read_head
            self._xdepth += 1


        return self.read_head



    ##
    #   @brief
    def jump_to_1st_child_of_next_parent(self):
        self.move_to_parent()
        self.move_to_next_node()
        # To be sure we are not unfortunately on a leaf:
        # (this loop should end because we just came from a node that's not
        # a leaf, in the worst case, we come back into it)
        while len(self.read_head.children) == 0:
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
        while len(self.read_head.children) == 0:
            self.move_to_prev_node()
        return self.move_to_first_child()


