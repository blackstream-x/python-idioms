# -*- coding: utf-8 -*-

"""

immutable_dict

immutable dict class

"""


from collections import abc


#
# Classes
#


class ImmutableDict(abc.Mapping, abc.Hashable):

    """Immutable dict-like class

    TODO: add .items() method
    """

    def __init__(self, *args, **kwargs):
        """Allocate the inner data structure"""
        data = dict(*args, **kwargs)
        keylist = []
        valuelist = []
        self.__key_lookup = {}
        for (index, (key, value)) in enumerate(data.items()):
            if not isinstance(value, abc.Hashable):
                raise ValueError("All values must be hashable!")
            #
            keylist.append(key)
            valuelist.append(value)
            self.__key_lookup[key] = index
        #
        self.__keys = tuple(keylist)
        self.__values = tuple(valuelist)

    def __getitem__(self, name):
        """Return the value for key 'name'"""
        index = self.__key_lookup[name]
        return self.__values[index]

    def __len__(self):
        """Return the number of items"""
        return len(self.__keys)

    def __iter__(self):
        """Return an iterator over the keys"""
        return iter(self.__keys)

    def __hash__(self):
        """Return the hash of the str representation"""
        return hash(str(self))

    def __str__(self):
        """String representation"""
        contents = ", ".join(
            f"{key!r}: {self.__values[index]!r}"
            for (index, key) in enumerate(self.__keys)
        )
        return f"{self.__class__.__name__}({contents})"


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
