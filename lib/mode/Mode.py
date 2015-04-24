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
import logging.config

# Pilberry packages|modules imports
from lib.tree.Node import Node
from lib.tree.NodeFileSystem import NodeFileSystem
# from lib.tree.NodeDataBase import NodeDataBase
from lib.globals import current_mode_id, MODES_CONFIG, USER_CONFIG
import lib.globals as globals
from lib.globals import LOG_DIR
from lib.musicdriver.MusicDriver import MusicDriver

import lib.mode.state.memory.default as memory_state
STATES_LIST = ['State_A', 'State_B', 'State_C']


logging.config.fileConfig(LOG_DIR + 'logging.conf')

modeLog = logging.getLogger('modeLog')


##
# @class Mode
# @brief
class Mode(object):


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
            if USER_CONFIG['VIEW'][current_mode_id] == '':
                if USER_CONFIG['VIEW']['DEFAULT'] != '':
                    if USER_CONFIG['VIEW']['DEFAULT'] != 'FILE_SYSTEM':
                        #node_class = NodeDataBase
                        self._view_type = USER_CONFIG['VIEW']['DEFAULT']
            elif USER_CONFIG['VIEW'][current_mode_id] != 'FILE_SYSTEM':
                #node_class = NodeDataBase
                self._view_type = USER_CONFIG['VIEW'][current_mode_id]

        elif USER_CONFIG['VIEW']['ALL'] != 'FILE_SYSTEM':
            #node_class = NodeDataBase
            self._view_type = USER_CONFIG['VIEW']['ALL']

        root_path = MODES_CONFIG[current_mode_id]['ROOT_PATH']
        if 'root' in options:
            root_path = options['root']


        self._tree = node_class(None,
                                root_path,
                                0,
                                [], [],
                                self._view_type,
                                0,
                                2)


        s = str(type(self._tree))
        modeLog.debug("root node's type is: "\
                     + s[s.rfind('.')+1:-2] \
                     + " its name is: " \
                     + self._tree['file_name'] \
                     + " and it has: " \
                     + str(len(self._tree.children)) \
                     + " children.")

        ##
        #   @todo   Check if there is one child at least!
        self._xnode = self._tree.children[0]
        self._head = self._tree.children[0]

        modeLog.debug("initialized xnode at: " + self._xnode['file_name'])


        self._md = MusicDriver()

        self._state = 'State_A'

        self._HANDLE = {}

        for s in STATES_LIST:
            self._HANDLE[s] = \
        {'CMD_MOVE_TO_PARENT' : getattr(memory_state, s).move_to_parent,
         'CMD_MOVE_TO_1ST_CHILD' : getattr(memory_state, s).move_to_1st_child,
         'CMD_SELECT' : getattr(memory_state, s).select,
         'CMD_MOVE_TO_NODE_PREV' : getattr(memory_state, s).move_to_node_prev,
         'CMD_MOVE_TO_NODE_NEXT' : getattr(memory_state, s).move_to_node_next,
         'CMD_ESC' : getattr(memory_state, s).esc,
         'CMD_STOP' : getattr(memory_state, s).stop,
         'playing' : getattr(memory_state, s).msg_cmus_playing,
         'stopped' : getattr(memory_state, s).msg_cmus_stopped,
         'paused' : getattr(memory_state, s).msg_cmus_paused,
         'CMD_VOL_UP' : getattr(memory_state, s).vol_up,
         'CMD_VOL_DOWN' : getattr(memory_state, s).vol_down,
         'CMD_SETTINGS' : getattr(memory_state, s).no_action,
         '' : getattr(memory_state, s).no_action,
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


    ##
    #   @brief
    def get_state(self):
        return self._state


    ##
    #   @brief
    def get_HANDLE(self):
        return self._HANDLE


    md = property(get_md,
                  doc="The Mode's MusicDriver")
    head = property(get_head,
                    doc="Read Head position (node of the tree)")
    xnode = property(get_xnode,
                     doc="XNode is the 'explorer node' of the tree")
    view_type = property(get_view_type,
                         doc="View type of the tree")
    state = property(get_state,
                     doc="The Mode's current state")
    HANDLE = property(get_HANDLE,
                     doc="The HANDLE field")


    ##
    #   @brief
    def set_head(self, n):
        modeLog.debug("setting head at: " + n['file_name'])
        self._head = n


    ##
    #   @brief
    def set_xnode(self, n):
        modeLog.debug("setting xnode at: " + n['file_name'])
        self._xnode = n


    ##
    #   @brief
    def set_state(self, s):
        ##
        #   @todo   Check that the argument s belongs to the 'authorized' states
        modeLog.debug("setting state at: \033[32m" + s + "\033[0m")
        self._state = s


    ##
    #   @brief
    def roger(self):
        if 'playing' == globals.cmus_status:
            self.md.stop()
            self.md.start_playing()


    ##
    #   @brief
    def handle(self, info, **options):
        self.HANDLE[self._state][info](self, **options)


