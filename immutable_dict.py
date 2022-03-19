# -*- coding: utf-8 -*-

"""

immutable_dict

An immutable and hashable dict-like class

"""


from collections import abc


class ImmutableDict(abc.Mapping, abc.Hashable):

    """Immutable and hashable dict-like class

    JSON or YAML serialization is not supported directly,
    but can be done by creating a dict from the instance
    (eg. using the .as_mutable_dict() method).
    """

    def __init__(self, *args, **kwargs):
        """Allocate the inner data structure"""
        data = dict(*args, **kwargs)
        for value in data.values():
            try:
                hash(value)
            except TypeError as error:
                raise ValueError(
                    f"Cannot create the {self.__class__.__name__} instance:"
                    f" value {value!r} is not hashable!"
                ) from error
            #
        #
        self.__keys = tuple(data.keys())
        self.__values = tuple(data.values())

    def as_mutable_dict(self):
        """Return a standard dict from self"""
        return dict(self)

    def items(self):
        """Return an iterator over (key, value) pairs"""
        for index, key in enumerate(self.__keys):
            yield key, self.__values[index]
        #

    def __getitem__(self, name):
        """Return the value for key 'name'"""
        try:
            return self.__values[self.__keys.index(name)]
        except ValueError as error:
            raise KeyError(name) from error
        #

    def __hash__(self):
        """Return the hash of the str representation"""
        return hash(repr(self))

    def __iter__(self):
        """Return an iterator over the keys"""
        return iter(self.__keys)

    def __len__(self):
        """Return the number of items"""
        return len(self.__keys)

    def __repr__(self):
        """String representation"""
        contents = ", ".join(
            f"{key!r}: {value!r}" for key, value in self.items()
        )
        return f"{self.__class__.__name__}({{{contents}}})"


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
