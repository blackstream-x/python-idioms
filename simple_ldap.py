# -*- coding: utf-8 -*-

"""

simple_ldap

Module providing simplified LDAP helper classes

"""


class RelativeDistName:

    """Object representing an LDAP RDN"""

    def __init__(self, **kwargs):
        """Store the attribute(s)"""
        self.__data = kwargs

    @classmethod
    def from_string(cls, rdn_string):
        """Return a RelativeDN from rdn_string"""
        components = {}
        for part in rdn_string.split("+"):
            name, value = part.split("=")
            components[name.strip()] = value.strip()
        #
        return cls(**components)

    def __getattr__(self, name):
        """Return the stored attribute"""
        try:
            return self.__data[name]
        except KeyError as error:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute {name!r}"
            ) from error
        #

    def __hash__(self):
        """Return a hash value"""
        return hash(str(self))

    def __repr__(self):
        """Object representation"""
        contents = ", ".join(
            f"{key}={value!r}" for key, value in self.__data.items()
        )
        return f"{self.__class__.__name__}({contents})"

    def __str__(self):
        """String representation"""
        return "+".join(f"{key}={value}" for key, value in self.__data.items())


class DistName:

    """Object representing an LDAP DN"""

    def __init__(self, *rdns):
        """
        Allocate the inner data structure:
        a tuple of RelativeDistName objects
        """
        self.__parts = tuple(
            RelativeDistName.from_string(part) for part in rdns
        )

    @classmethod
    def from_string(cls, dn_string):
        """Return a DN from dn_string"""
        parts = dn_string.split(",")
        return cls(*parts)

    def __getitem__(self, index):
        """Return the part at index"""
        return self.__parts[index]

    def __hash__(self):
        """Return a hash value"""
        return hash(str(self))

    def __repr__(self):
        """Object representation"""
        contents = ", ".join(repr(str(part)) for part in self.__parts)
        return f"{self.__class__.__name__}({contents})"

    def __str__(self):
        """String representation"""
        return ",".join(str(part) for part in self.__parts)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
