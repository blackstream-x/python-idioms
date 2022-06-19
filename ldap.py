# -*- coding: utf-8 -*-

"""

ldap

Module providing LDAP helper classes and functions

"""


class DistiguishedName:

    """Object representing an LDAP DN
    """

    # pylint: disable=invalid-name  # LDAP DN attributes

    def __init__(self, cn=None, ou=None, dc=None):
        """Allocate the inner data structure"""
        if not isinstance(cn, str):
            raise ValueError("At least, a cn must be provided")
        #
        self.__cn = cn
        ous_list = []
        if isinstance(ou, str):
            ous_list.append(ou)
        else:
            try:
                ous_list.extend(ou)
            except TypeError:
                pass
            #
        #
        self.__ou = tuple(ous_list)
        dcs_list = []
        if isinstance(dc, str):
            dcs_list.append(dc)
        else:
            try:
                dcs_list.extend(dc)
            except TypeError as error:
                raise ValueError(
                    "At least, a dc must be provided"
                ) from error
            #
        #
        self.__dc = tuple(dcs_list)

    def __hash__(self):
        """Return a hash value"""
        return hash(str(self))

    def __repr__(self):
        """String representation"""
        contents = ", ".join(
            f"{key}={value!r}"
            for key, value in (
                ("cn", self.__cn),
                ("ou", self.__ou),
                ("dc", self.__dc),
            )
        )
        return f"{self.__class__.__name__}({{{contents}}})"



# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
