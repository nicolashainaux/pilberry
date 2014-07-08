# -*- coding: utf-8 -*-

##
# @class Clonable
# @brief All objects that are used must be able to be copied deeply
# Any Clonable are provided the clone() method, no need to reimplement it
class Clonable(object):





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a deep copy of the object
    def clone(self):
        result = object.__new__(type(self))
        result.__init__(self)
        return result
