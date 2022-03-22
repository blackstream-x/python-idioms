# -*- coding: utf-8 -*-

"""

frozen_dict

An immutable and hashable dict-like class

"""


from collections import abc


class FrozenDict(abc.Mapping, abc.Hashable):

    """Immutable and hashable object mimicking dict behavior

    JSON or YAML serialization is not supported directly,
    but can be done by creating a dict from the instance
    (eg. using the .unfreeze() method).
    """

    def __init__(self, *args, **kwargs):
        """Allocate the inner data structure"""
        self.__data = tuple(dict(*args, **kwargs).items())
        self.__cached_hash = hash((self.__class__, self.__data))

    def unfrozen(self):
        """Return a normal dict from self"""
        return dict(self)

    def items(self):
        """Return an iterator over (key, value) pairs"""
        for key, value in self.__data:
            yield key, value
        #

    def __getitem__(self, name):
        """Return the value for key 'name'"""
        for key, value in self.__data:
            if key == name:
                return value
            #
        #
        raise KeyError(name)

    def get(self, key, default=None):
        """Return the value for key 'name' or default"""
        try:
            return self[key]
        except KeyError:
            return default
        #

    def __hash__(self):
        """Return a hash value"""
        return self.__cached_hash

    def __iter__(self):
        """Return an iterator over the keys"""
        for key, _ in self.__data:
            yield key
        #

    def __len__(self):
        """Return the number of items"""
        return len(self.__data)

    def __repr__(self):
        """String representation"""
        contents = ", ".join(
            f"{key!r}: {value!r}" for key, value in self.items()
        )
        return f"{self.__class__.__name__}({{{contents}}})"


def deepfreeze(item):
    """Return a frozen (i.e. immutable and hashable)
    pendant of item. For collections, this implies
    that all members are frozen too.
    """
    if item in (True, False, None, Ellipsis) or isinstance(
        item, (str, int, float, frozenset, FrozenDict)
    ):
        return item
    #
    if isinstance(item, set):
        return frozenset(item)
    #
    if isinstance(item, (list, tuple)):
        return tuple(deepfreeze(member) for member in item)
    #
    if isinstance(item, dict):
        return FrozenDict(
            (key, deepfreeze(value)) for (key, value) in item.items()
        )
    #
    # Try hashing the item
    hash(item)
    #
    # Is the item an iterable?
    # If not -> assume it is frozen.
    # This is not 100 % safe...
    try:
        None in item
    except TypeError:
        return item
    #
    # TODO: check if item is a collection, mutable etc.
    raise NotImplementedError


def serializable(item, keep_hashable=False):
    """Return a serializable pendan to item"""
    if item in (True, False, None) or isinstance(item, (str, int, float)):
        return item
    #
    if isinstance(item, (list, set)):
        return [serializable(member) for member in item]
    #
    if isinstance(item, (tuple, frozenset)):
        return [
            serializable(member, keep_hashable=keep_hashable)
            for member in item
        ]
    #
    # TODO: dict, FrozenDict
    ...
    #
    #
    raise TypeError(f"Cannot serialize {item.__class__.__name__} {item!r}")


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
