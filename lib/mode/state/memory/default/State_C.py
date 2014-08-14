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
import subprocess

# Pilberry packages|modules imports
import lib.globals as globals
from lib.globals import SOCKETS_CONFIG, USER_CONFIG

##
# @class State_C
# @brief
class State_C(object):


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
        # xnode is an inode
        if len(self.xnode.children) >= 1:
            for n in self.xnode.children:
                if (not n.is_a_leaf(n.full_path) and len(n.children) == 0):
                    n.add_children(1)
            self.set_xnode(self.xnode.children[0])

        # xnode is a leaf
        elif self.head != self.xnode:
            self.set_head(self.xnode)
            ##
            #   @todo   Check if this stop is still necessary once the delayed
            #           play is implemented
            self.md.stop()
            self.md.start_playing()
            self.set_state('State_B')

        # xnode is head
        else:
            if globals.cmus_status == 'paused':
                self.md.toggle_pause()
                self.set_state('State_B')
            elif globals.cmus_status == 'playing':
                self.set_state('State_B')


    ##
    #   @brief
    def select(self):
        self.handle('CMD_MOVE_TO_1ST_CHILD')


    ##
    #   @brief
    def esc(self):

        if globals.cmus_status == 'playing':
            self.set_xnode(self.head)
            self.set_state('State_B')

        elif globals.cmus_status == 'stopped':
            self.set_state('State_A')

        elif globals.cmus_status == 'paused':
            self.set_xnode(self.head)
            self.md.toggle_pause()
            self.set_state('State_B')



    ##
    #   @brief
    def stop(self):
        self.md.stop()
        self.set_xnode(self.head)
        self.set_state('State_A')

    ##
    #   @brief
    def msg_cmus_playing(self, **options):
        if self.head['full_path'] != options['full_path']:
            logging.debug("noticed that head doesn't match current song")
            # Current song doesn't match head node
            # Let's try to find the node matching current song
            # First, check if it's one of the song of the same 'directory'
            found = False
            for n in self.head.neighbours:
                if n['full_path'] == options['full_path']:
                    self.set_head(n)
                    found = True
            if found:
                logging.debug("found the node matching current song")
                logging.debug("Updated head Node, waiting for next command...\n")

            ##
            #   @todo   If the right node is not among the neighbours, it has
            #           to be found elsewhere. In the best case, a data-
            #           base is available and we can find it thanks to its
            #           full path. If no database is available, then a
            #           search algorithm has to be found...

    ##
    #   @brief
    def msg_cmus_stopped(self, **options):
        pass


    ##
    #   @brief
    def msg_cmus_paused(self, **options):
        pass


    ##
    #   @brief
    def vol_up(self, **options):
        subprocess.Popen(['cmus-remote',
                          '--server',
                          SOCKETS_CONFIG['TO_CMUS']['FILE'],
                          '-C',
                          'vol +' + USER_CONFIG['GENERAL']['VOL_STEP'] + '%'])


    ##
    #   @brief
    def vol_down(self, **options):
        subprocess.Popen(['cmus-remote',
                          '--server',
                          SOCKETS_CONFIG['TO_CMUS']['FILE'],
                          '-C',
                          'vol -' + USER_CONFIG['GENERAL']['VOL_STEP'] + '%'])


    ##
    #   @brief
    def no_action(self, **options):
        pass
