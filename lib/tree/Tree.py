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
import lib.globals as globals
from lib.musicdriver.MusicDriver import MusicDriver

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
                                 [], [],
                                 self._view_type,
                                 0,
                                 2)


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


        self._md = MusicDriver()

        self.HANDLE = {'CMD_MOVE_TO_PARENT' : self.move_to_parent,
                       'CMD_MOVE_TO_1ST_CHILD' : self.move_to_1st_child,
                       'CMD_SELECT' : self.select,
                       'CMD_MOVE_TO_NODE_PREV' : self.move_to_node_prev,
                       'CMD_MOVE_TO_NODE_NEXT' : self.move_to_node_next,
                       'CMD_ESC' : self.esc,
                       'CMD_STOP' : self.stop,
                       'CMD_ROGER' : self.roger
                      }





    ##
    #   @brief
    def get_md(self):
        return self._md

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
    def get_view_type(self):
        return self._view_type

    md = property(get_md,
                  doc="The Tree's MusicDriver")
    head = property(get_head,
                    doc="Read Head position (node of the Tree)")
    xnode = property(get_xnode,
                     doc="XNode is the 'explorer node' of the Tree")
    view_type = property(get_view_type,
                         doc="View type of the Tree")
    ##
    #   @brief
    def set_head(self, n):
        logging.debug("setting head at: " + n['file_name'])
        self._head = n



    ##
    #   @brief
    def set_xnode(self, n):
        logging.debug("setting xnode at: " + n['file_name'])
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

        globals.exploring = True


    ##
    #   @brief
    def move_to_next_node(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position + 1) % len(self.xnode.neighbours)
        self.set_xnode(self.xnode.neighbours[new_position])

        # Now, if we're at playing and not exploring, we have to change
        # head's position too and start playing
        if not globals.exploring:
            if len(self.xnode.children) == 0:
                self.set_head(self.xnode)
                #self.md.stop()
                #self.md.start_playing()
            else:
                globals.exploring = True


    ##
    #   @brief
    def move_to_prev_node(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position - 1) % len(self.xnode.neighbours)
        self.set_xnode(self.xnode.neighbours[new_position])

        # Now, if we're at playing and not exploring, we have to change
        # head's position too and start playing
        if not globals.exploring:
            if len(self.xnode.children) == 0:
                self.set_head(self.xnode)
                #self.md.stop()
                #self.md.start_playing()
            else:
                globals.exploring = True


    ##
    #   @brief
    def roger(self):
        if 'playing' == globals.cmus_status:
            self.md.stop()
            self.md.start_playing()


    ##
    #   @brief
    def move_to_1st_child(self):
        # There it is not useful to use the is_a_leaf() method on self.xnode
        # because we don't need to check the filesystem neither to make a
        # request in the DB. If there are children, they are already here.
        # So just check len(children)
        if globals.exploring:
            if len(self.xnode.children) >= 1:
                for n in self.xnode.children:
                    if (not n.is_a_leaf(n.full_path) and len(n.children) == 0):
                        n.add_children(1)
                self.set_xnode(self.xnode.children[0])


    ##
    #   @brief
    def select(self):
        if len(self.xnode.children) >= 1:
            self.move_to_1st_child()
        else:
            if not globals.exploring:
                self.md.toggle_pause()
                globals.exploring = True

            elif globals.cmus_status != 'playing':
                self.set_head(self.xnode)
                self.md.start_playing()
                globals.exploring = False

            elif self.xnode == self.head:
                pass
            else:
                self.set_head(self.xnode)
                self.md.start_playing()
                globals.exploring = False


    ##
    #   @brief
    def esc(self):
        if globals.cmus_status != 'playing':
            pass
        elif globals.exploring:
            self.set_xnode(self.head)
            globals.exploring = False
        else:
            self.md.toggle_pause()
            globals.exploring = True


    ##
    #   @brief
    def stop(self):
        if globals.cmus_status != 'playing':
            pass
        elif globals.exploring:
            self.md.stop()
            globals.exploring = True
            self.set_xnode(self.head)
        else:
            self.md.stop()
            globals.exploring = True


    ##
    #   @brief
    def handle(self, cmd):
        self.HANDLE[cmd]()


