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
import logging

# Pilberry packages|modules imports
from lib.globals import MUSIC_FILE_EXTENSIONS


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
    #   @brief  Checks if current Node is actually a leaf
    @staticmethod
    @abstractmethod
    def is_a_leaf(self):
        # /!\ Take care, this should not only be:
        # return len(self._children) == 0
        # Because this should actually check, in the database or filesystem,
        # if self has really children or not, according to the current view.
        # This is a static method because it doesn't need the fields of an
        # object, just determine from the path if it's a leaf indeed or not.
        # Moreover it has to be used in __init__()
        pass



    ##
    #   @brief  Gets the children list of a Node, as filenames or directory names.
    #           Returns [] if the node has no children. Should be called only
    #           on non-leaves nodes.
    #   @return List
    #   @param  full_path   The full path of directory to test
    #   @todo   Maybe check full_path is a path to a directory.
    @staticmethod
    @abstractmethod
    def get_children_list(self, full_path):
        pass
        #getattr(self, self.get_children_list(full_path))()



    ##
    #   @brief
    def add_children(self, deeper):
        logging.debug("Node: " \
                      + self['file_name'] \
                      + " checks if it can add children. Given deeper is: " \
                      + str(deeper))
        if deeper > 0 \
            and not self.is_a_leaf(self.full_path) \
            and len(self._children) == 0:
        #___
            logging.debug("Node: " \
                          + self['file_name'] \
                          + " will add children")

            for i, name in enumerate(self.get_children_list(self.full_path)):
                n = object.__new__(type(self))
                n.__init__(self,
                           self.full_path + name,
                           i,
                           self._children[0:i],
                           [],
                           self._view,
                           self.depth + 1,
                           deeper - 1)

                if not self.is_a_leaf(self.full_path + name):
                    if deeper > 1:
                        n.add_children(deeper - 1)

                self._children.append(n)
                logging.debug("Node: " + self['file_name'] + \
                              " has now " \
                              + str(len(self._children)) \
                              + " children. ")

            # Now, add the neighbours after!
            for i in range(len(self._children)):
                self._children[i]._neighbours_after = \
                                        self._children[i+1:len(self._children)]


        elif deeper > 1 \
            and not self.is_a_leaf(self.full_path):
        #___
            for n in self._children:
                n.add_children(deeper - 1)



    ##
    #   @brief
    #   @param  parent : the parent Node
    #   @param  full_path : the full path of the file
    #   @param  position : the position among the neighbours' list
    #   @param  view : the view type (e.g. file system, album/artist etc.)
    #   @param  deeper : int that tells how deep we should further add children
    def __init__(self, parent, full_path, position,
                       neighbours_before, neighbours_after,
                       view, depth, deeper):

        self._parent = parent

        end_as_dirname = ""

        if os.path.isdir(full_path):
            end_as_dirname = "/"
            if full_path[-1:] != "/":
                full_path += end_as_dirname


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
        head, tail = ntpath.split(full_path)
        file_name = tail or ntpath.basename(head)
        file_name += end_as_dirname

        temp = "None"
        if self.parent != None:
            temp = self.parent['file_name']

        s = str(type(self))
        logging.debug("creating a new " + s[s.rfind('.')+1:-2] \
                      + "; its parent is: " +  temp \
                      + "; its name: " + file_name)

        # The content should be initialized here, without any problem a priori
        self._content = {'full_path' : full_path,
                         'file_name' : file_name
                         #'tags' : self._tags
                         }

        # The children and neighbours
        self._children = []
        self._neighbours_before = neighbours_before
        self._neighbours_after = neighbours_after

        self._depth = depth

        if deeper > 0:
            self.add_children(deeper)



    ##
    #   @brief
    def __getitem__(self, key):
        if key in self._content:
            return self._content[key]
        #elif key in self._tags:
        #    return self._content['tags'][key]



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
    def get_neighbours_before(self):
        return self._neighbours_before


    ##
    #   @brief
    def get_neighbours_after(self):
        return self._neighbours_after


    ##
    #   @brief
    def get_neighbours(self):
        return self._neighbours_before + [self] + self._neighbours_after


    ##
    #   @brief
    def get_full_path(self):
        return self._full_path


    ##
    #   @brief
    def get_position(self):
        return self._position


    ##
    #   @brief
    def get_depth(self):
        return self._depth


    parent = property(get_parent, doc="Parent Node")
    children = property(get_children, doc="Children Nodes, if any")
    neighbours_before = property(get_neighbours_before,
                                 doc="Neighbours of the Node, before it")
    neighbours_after = property(get_neighbours_after,
                                doc="Neighbours of the Node, after it")
    neighbours = property(get_neighbours,
                          doc="Neighbours of the Node, including it")

    full_path = property(get_full_path, doc="The full patht to the file or "\
                                            + "directory. Will also be a unique"\
                                            + " identifier.")
    position = property(get_position, doc="Position of the Node among " \
                                         + "its brothers")
    depth = property(get_depth, doc="Depth of the Node")


    ##
    #   @brief
    def set_depth(self, val):
        self._depth = val



