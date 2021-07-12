# -*- coding: utf-8 -*-

"""

translation

Text transl(iter)ation helper classes

"""


import re


#
# Classes
#


class MultiTranslator:

    """All-in-one multiple-string-substitution class
    instantiated like a dict containing (original, replacment) items,
    adapted from <https://www.oreilly.com/library/view
    /python-cookbook/0596001673/ch03s15.html>
    but optimized for re-usability.
    """

    def __init__(self, *args, **kwargs):
        """Keep an internal dict of (original, replacement) items
        and precompile a catch-all regular expression
        """
        self.__replacements = dict(*args, **kwargs)
        self.__catch_all = re.compile(
            '|'.join(re.escape(key) for key in self.__replacements))

    def __call__(self, match):
        """Handler invoked for each regex match"""
        return self.__replacements[match.group(0)]

    def translate(self, text):
        """Translate text and return the result."""
        return self.__catch_all.sub(self, text)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
