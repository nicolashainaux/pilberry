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
from .State import State


##
# @class State_A
# @brief
class State_A(State):


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


    ##
    #   @brief
    def move_to_node_next(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position + 1) % len(self.xnode.neighbours)
        self.set_xnode(self.xnode.neighbours[new_position])


    ##
    #   @brief
    def move_to_node_prev(self):
        # We compute the new position with a modulo to go to first position if
        # we were at end and vice-versa
        new_position = (self.xnode.position - 1) % len(self.xnode.neighbours)
        self.set_xnode(self.xnode.neighbours[new_position])


    ##
    #   @brief
    def move_to_1st_child(self):
        # There it is not useful to use the is_a_leaf() method on self.xnode
        # because we don't need to check the filesystem neither to make a
        # request in the DB. If there are children, they are already here.
        # So just check len(children)
        if len(self.xnode.children) >= 1:
            for n in self.xnode.children:
                if (not n.is_a_leaf(n.full_path) and len(n.children) == 0):
                    n.add_children(1)
            self.set_xnode(self.xnode.children[0])
        else:
            pass


    ##
    #   @brief
    def select(self):
        if len(self.xnode.children) >= 1:
            self.handle('CMD_MOVE_TO_1ST_CHILD')
        else:
            if self.queue_mode_activated:
                self.md.start_playing_queue()
                self.set_xnode(self.md.current_song)
                self.set_head(self.xnode)
            else:
                self.set_head(self.xnode)
                self.md.start_playing()
            self.set_state('State_B')


    ##
    #   @brief
    def esc(self):
        pass


    ##
    #   @brief
    def stop(self):
        pass


