# -*- coding: utf-8 -*-

"""

logging_extension

Extensions for the stdlib logging module

"""


import logging
import os
# import sys


#
# Constants
#


LOGLEVELS = dict(
    DEBUG2=9,
    DEBUG3=8,
    DEBUG4=7,
    DEBUG5=6,
    DEBUG6=5,
    DEBUG7=4,
    DEBUG8=3,
    DEBUG9=2,
    DEBUG10=1,
)

FALLBACK_LEVEL_NAME = "DEBUG3"


#
# Helper functions
#


def initialize():
    """Initialize logging"""
    for debug_level in range(2, 11):
        level_name = f"DEBUG{11 - debug_level}"
        if hasattr(logging, level_name):
            continue
        #
        logging.addLevelName(debug_level, level_name)
        setattr(logging, level_name, debug_level)
    #
    configured_level_name = os.getenv(
        "CONFIG_LOG_LEVEL_NAME", FALLBACK_LEVEL_NAME
    )
    try:
        level_number = getattr(logging, configured_level_name)
    except AttributeError:
        level_number = -1
    #
    unsupported_level = False
    if level_number < logging.NOTSET or level_number > logging.CRITICAL:
        unsupported_level = True
        level_number = getattr(logging, FALLBACK_LEVEL_NAME)
    #
    logging.basicConfig(
        level=level_number,
        format="%(levelname)-8s | %(levelno)-2d | %(message)s"
    )
    if unsupported_level:
        logging.warning(
            "Level name %r notsupported, falling bach to %r!",
            configured_level_name,
            FALLBACK_LEVEL_NAME
        )
    #


if __name__ == "__main__":
    initialize()
    logging.log(logging.DEBUG2, "Debug (level 2) message")
    logging.log(logging.DEBUG4, "Debug (level 4) message")
    logging.log(logging.DEBUG6, "Debug (level 6) message")
    logging.log(logging.DEBUG8, "Debug (level 8) message")


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
