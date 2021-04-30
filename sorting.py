# -*- coding: utf-8 -*-

"""

sorting

Sort helper classes

"""


#
# Classes
#


class SortableMixin:

    """Minimalist mixin to make a class sortable
    by attribute sort_key
    """

    def __eq__(self, other):
        """Rich comparison: equals"""
        return self.sort_key == other.sort_key

    def __gt__(self, other):
        """Rich comparison: greater than"""
        return self.sort_key > other.sort_key


class SortKey:

    """Provide a function suitable as value for the key= keyword
    in the builtin sorted() function.
    It is primarily intended for string comparisons,
    hence convert_non_to defaults to ''.
    """

    msg_required_keywords = 'Please specify either attr or item!'

    def __init__(self,
                 attr=None,
                 item=None,
                 case_sensitive=True,
                 convert_none_to=''):
        """Store the key attribute name or item hashable.
        Raise a TypeError if the provided attr is not a string,
        or the provided item is not hashable.
        Raise a ValueError if not exactly one of
        attr and item was provided.
        """
        if attr is not None:
            if item is not None:
                raise ValueError(self.msg_required_keywords)
            #
            # Test if attr is a string
            try:
                getattr(self, attr)
            except AttributeError:
                pass
            #
            self.__key = attr
            self.__value_getter = getattr
        elif item is not None:
            # Test if item is hashable
            hash(item)
            self.__key = item
            self.__value_getter = self.getitem
        else:
            raise ValueError(self.msg_required_keywords)
        #
        self.__case_sensitive = case_sensitive
        # Convert None to a comparable type
        self.__convert_none_to = convert_none_to

    @staticmethod
    def getitem(obj, name):
        """Item access"""
        return obj[name]

    def __call__(self, sort_item):
        """Return a sortable value for sort_item"""
        value = self.__value_getter(sort_item, self.__key)
        if value is None:
            value = self.__convert_none_to
        #
        if self.__case_sensitive:
            return value
        #
        return value.lower()


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
