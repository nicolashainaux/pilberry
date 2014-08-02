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


        # We set head as the first node found in root/,
        # otherwise we'll have to enter root to see anything
        self._xneighbours = self._nodes.children
        self._hneighbours = self._nodes.children

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
        self._xnode = self._nodes.children[0]
        self._head = self._nodes.children[0]

        logging.debug("initialized xnode at: " + self._xnode['file_name'])


        ##
        #   @todo   Maybe initialize it to 1, because we did not set the
        #           view to / but to the first child of /
        self._xdepth = 0
        self._hdepth = 0


    ##
    #   @brief
    def get_head(self):
        return self._head

    ##
    #   @brief
    def get_xnode(self):
        return self._xnode

    ##
    #   @brief
    def get_hdepth(self):
        return self._hdepth

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
    def get_hneighbours(self):
        return self._hneighbours

    ##
    #   @brief
    def get_xneighbours(self):
        return self._xneighbours

    ##
    #   @brief Returns a list of all neighbours after head, including head
    def get_hneighbours_after(self):
        return self.hneighbours[self.head.position:len(self.hneighbours)]

    ##
    #   @brief Returns the list of neighbours before head (but not head)
    def get_hneighbours_before(self):
        return self.hneighbours[0:self.head.position]




    head = property(get_head,
                    doc="Read Head position (node of the Tree)")
    xnode = property(get_xnode,
                     doc="XNode is the 'explorer node' of the Tree")
    hdepth = property(get_hdepth,
                      doc="Current depth in the Tree")
    xdepth = property(get_xdepth,
                      doc="Current xdepth in the Tree")
    view_type = property(get_view_type,
                         doc="View type of the Tree")
    hneighbours = property(get_hneighbours,
                           doc="All nodes at the same floor as current")
    xneighbours = property(get_xneighbours,
                           doc="All nodes at the same floor as current x")
    hneighbours_after = property(get_hneighbours_after,
                          doc="All nodes at the same floor as current, " \
                              "after current, including current")
    hneighbours_before = property(get_hneighbours_before,
                          doc="All nodes at the same floor as current, " \
                              "before current, but not current")


    ##
    #   @brief
    def set_head(self, n):
        self._head = n

    ##
    #   @brief
    def set_xnode(self, n):
        self._xnode = n

    ##
    #   @brief  Moves to the parent Node. Returns the new current Node.
    #   @return Node
    def move_to_parent(self):
        # self.xnode.parent should never be None because we forbid
        # to access the root directory
        # So, self.xnode.parent.parent != None
        # is equivalent to 'self.xnode.parent is not root'
        if self.xnode.parent.parent != None:
            self.set_xnode(self.xnode.parent)
            self._xdepth -= 1
            self._xneighbours = self.xnode.parent.children



    ##
    #   @brief
    def move_to_next_node(self, nb_step=1):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position + nb_step) % len(self.xneighbours)
        self.set_xnode(self.xneighbours[new_position])
        # self._xneighbours remains the same


    ##
    #   @brief
    def move_to_prev_node(self, nb_step=1):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xndoe.position - nb_step) % len(self.xneighbours)
        self.set_xnode(self.xneighbours[new_position])
        # self._xneighbours remains the same



    ##
    #   @brief
    def move_to_1st_child(self):
        # There it is not useful to use the is_a_leaf() method because
        # we don't need to check the filesystem neither to make a request
        # in the DB. If there are children, they are already here.
        # So just check len(children)
        if len(self.xnode.children) >= 1:
            for n in self.xnode.children:
                if (not n.is_a_leaf(n.full_path) and len(n.children) == 0):
                    n.add_children(1)
            self._xneighbours = self.xnode.children
            self.set_xnode(self.xnode.children[0])
            self._xdepth += 1



