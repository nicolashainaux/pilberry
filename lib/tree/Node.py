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
import os.path
import ntpath
from abc import ABCMeta, abstractmethod

# Pilberry packages|modules imports



##
# @class Node
# @brief This matches both the inner nodes and the leaves of the tree.
#        A Node contains also all kind of information that may be available,
#        it gets it at its creation, from the file system or from the database,
#        and lets it accessible as from a dictionnary.
#        For instance, it should be possible to get, if current_node is a Node:
#        current_node['file_name'], current_node['tags'],
#        current_node['Artist'], current_node['Album'] etc.
class Node(object, metaclass=ABCMeta):

    ##
    #   @brief
    #   @param  parent : the parent Node
    #   @param  full_path : the full path of the file
    #   @param  position : the position among the neighbours' list
    #   @param  view : the view type (e.g. file system, album/artist etc.)
    #   @param  add_children : int that tells how deep we should add children
    def __init__(self, parent, full_path, position, view, add_children):
        self._parent = parent
        self._full_path = full_path  # can also be used as unique identifier
        #self._tags = ... # extract them from the database, as a dict,
                              # or from the file, if we're using the file
                              # system view
        self._position = position # this should be an int
        self._view = view

        #self._display = ... # Create it from the infos and according to
                            # the chosen view (defined in conf file)

        # Now, determine the file name from full_path
        # and add a "/" at the end if it's a dir name actually
        end_as_dirname = ""

        if os.path.isdir(full_path):
            end_as_dirname = "/"

        head, tail = ntpath.split(full_path)
        file_name = tail or ntpath.basename(head)
        file_name += end_as_dirname

        self._content = {'full_path' : full_path,
                         'file_name' : file_name
                         #'tags' : self._tags
                         }

        self._children = []

        # This was an idea to allow using move_to_parent on the root Node,
        # without detecting self._parent is None;
        # but this implies some problems in Tree.move_to_parent()
        # and in other cases... so better not do that
        #if self._parent = None:
        #    self._parent = self


    ##
    #   @brief
    def __getitem__(self, key):
        if key in self._content:
            return self._content[key]
        #elif key in self._tags:
        #    return self._content['tags'][key]



    ##
    #   @brief  Checks if current Node is actually a leaf
    @abstractmethod
    def is_a_leaf(self):
        pass


    ##
    #   @brief
    def get_parent(self):
        return self._parent


    ##
    #   @brief
    def get_children(self):
        return self._children


    ##
    #   @brief
    def get_full_path(self):
        return self._full_path



    ##
    #   @brief
    def get_position(self):
        return self._position



    parent = property(get_parent, doc="Parent Node")
    children = property(get_children, doc="Children Nodes, if any")
    full_path = property(get_full_path, doc="The full patht to the file or "\
                                            + "directory. Will also be a unique"\
                                            + " identifier.")
    position = property(get_position, doc="Position of the Node among " \
                                         + "its brothers")


    ##
    #   @brief
    @abstractmethod
    def add_children(self, depth):
        pass
