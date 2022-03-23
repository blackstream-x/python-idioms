# -*- coding: utf-8 -*-

"""

freezer

Module providing the FrozenDict class
(an immutable and hashable mapping behaving like a readonly dict)
and functions to deepfreeze (i.e. make immutable and hashable) collections,
or to make objects serializable via JSON or YAML.

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


def deepfreeze(obj):
    """Return a frozen (i.e. immutable and hashable)
    pendant of obj. For collections, this implies
    that all members are frozen too (recursively)
    """
    if obj in (True, False, None, Ellipsis) or isinstance(
        obj, (str, int, float, frozenset, FrozenDict)
    ):
        return obj
    #
    if isinstance(obj, set):
        return frozenset(obj)
    #
    if isinstance(obj, (list, tuple)):
        return tuple(deepfreeze(item) for item in obj)
    #
    if isinstance(obj, dict):
        return FrozenDict(
            (key, deepfreeze(value)) for (key, value) in obj.items()
        )
    #
    # Try hashing obj. Implicitly raises a TypeError on non-hashable types.
    hash(obj)
    #
    # Is obj an iterable?
    # If not -> assume it is frozen.
    # This is not 100 % safe...
    try:
        None in obj
    except TypeError:
        return obj
    #
    # TODO: intelligent conversions checking if obj is a collection,
    #       mutable etc.
    raise NotImplementedError


def serializable(obj, keep_hashable=False):
    """Return a (JSON or YAML) serializable pendant of obj"""
    if obj in (True, False, None) or isinstance(obj, (str, int, float)):
        return obj
    #
    if isinstance(obj, (list, set)):
        if keep_hashable:
            raise TypeError(
                f"{obj.__class__.__name__} {obj!r}"
                " is not hashable by definition."
            )
        #
        return [serializable(item) for item in obj]
    #
    if isinstance(obj, (tuple, frozenset)):
        return tuple(
            serializable(item, keep_hashable=keep_hashable) for item in obj
        )
    #
    if isinstance(obj, dict):
        if keep_hashable:
            raise TypeError(
                f"{obj.__class__.__name__} {obj!r}"
                " is not hashable by definition."
            )
        #
        return dict(
            (serializable(key, keep_hashable=True), serializable(value))
            for (key, value) in obj.items()
        )
    #
    if isinstance(obj, FrozenDict):
        if keep_hashable:
            return serializable(tuple(obj.items()), keep_hashable=True)
        #
        return serializable(dict(obj))
    #
    raise TypeError(f"Cannot serialize {obj.__class__.__name__} {obj!r}")


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
