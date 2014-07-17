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



##
# @class Node
# @brief This matches both the inner nodes and leaves of the tree.
#        A Node contains also all kind of information that may be available,
#        it gets it at its creation, from the database using the unique id,
#        and lets it accessible as from a dictionnary.
#        For instance, it should be possible to get, if current_node is a Node:
#        current_node['file_name'], current_node['id3_tags'],
#        current_node['Artist'], current_node['Album'] etc.
class Node(object):

    ##
    #   @brief
    #   @param  parent : the parent Node
    #   @param  id : the id of the file, to get infos from the database
    #   @param  add_children : boolean to tell if we want to create children
    #                          at once
    def __init__(self, parent, id, add_children):
        self._parent = parent
        self._id = id         # unique identifier for the file, in the database?
        #self._id3_tags = ... # extract them from the database, as a dict

        self._display = ... # Create it from the infos and according to
                            # the chosen view (defined in conf file)

        self._content = {'file_name' : ...,  # get it from database
                         'display' : self._display
                         #'id3_tags' : self._id3_tags
                         }

        self._children = [] # and if the current node does have children in
                            # this view, AND if we want to dive one step more
                            # into the tree (add_children is True),
                            # then create them according to conf file (which
                            # kind of view...). Take all info
                            # from database and create each new i-th Node in
                            # this list with Node(self, id[i], False).
                            # Maybe use the method add_children() for that?
                            # It should be all the same...


    ##
    #   @brief
    def __getitem__(self, key):
        if key in self._content:
            return self._content[key]
        #elif key in self._id3_tags:
        #    return self._content['id3_tags'][key]



    ##
    #   @brief  Checks if current Node is actually a leaf
    def is_a_leaf(self):
        # /!\ Take care, this should not only be:
        #return len(self._children) == 0
        # This should actually check, in the database, if self has really
        # children or not, according to the current view


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
    def get_id(self):
        return self._id



    parent = property(get_parent, doc="Parent Node")
    children = property(get_children, doc="Children Nodes, if any")
    id = property(get_id, doc="The id is a unique identifier in the database")


    ##
    #   @brief
    def add_children(self):
        if not self.is_a_leaf():
            # define all what children would be, according to the chosen view
            # and add them to self._children
            # should be same algorithm as in __init__()



##
# @class Tree
# @brief
class Tree(object):

    ##
    #   @brief
    #   @param  id : this will be the id of the root node, has to be taken
    #                from the database
    def __init__(self, id):
        self._nodes = Node(None, id, True)
        self._current_node = self._nodes


    ##
    #   @brief
    def move_to_first_child(self):
        if not self.current_node.is_a_leaf():
            self.set_current_node(self.current_node.child[0])


    ##
    #   @brief
    def move_to_next_node(self):
        self.set_current_node = self.current_node.parent.
