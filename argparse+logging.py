#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

Script file name

Description, Copyright, License etc.

"""


import argparse
import logging
import sys


#
# Constants
#

MESSAGE_FORMAT_PURE = '%(message)s'
MESSAGE_FORMAT_WITH_LEVELNAME = '%(levelname)-8s\u2551 %(message)s'

RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


#
# Classes
#


...


#
# Functions
#


...


def __get_arguments():
    """Parse command line arguments"""
    argument_parser = argparse.ArgumentParser(
        description='Description')
    argument_parser.set_defaults(loglevel=logging.INFO)
    argument_parser.add_argument(
        '-v', '--verbose',
        action='store_const',
        const=logging.DEBUG,
        dest='loglevel',
        help='Output all messages including debug level')
    argument_parser.add_argument(
        '-q', '--quiet',
        action='store_const',
        const=logging.WARNING,
        dest='loglevel',
        help='Limit message output to warnings and errors')

    ...

    return argument_parser.parse_args()


def main(arguments):
    """Main routine, calling functions from above as required.
    Returns a returncode which is used as the script's exit code.
    """
    logging.basicConfig(format=MESSAGE_FORMAT_WITH_LEVELNAME,
                        level=arguments.loglevel)

    ...

    # Debug messages will NOT be displayed
    # unless the script is called with the
    # -v / --verbose option.
    logging.debug('Debugging information: %s * %s = %s', 2, 3, 2 * 3)

    # Information messages will be displayed
    # unless the script is called with the
    # -q / --quiet option
    logging.info('Normal information message')

    # Warning, error and critical messages will always be displayed
    logging.warning('Warning message')
    logging.error('Error message')
    logging.critical('Critical error message')

    ...

    return RETURNCODE_OK


if __name__ == '__main__':
    # Call main() with the provided command line arguments
    # and exit with its returncode
    sys.exit(main(__get_arguments()))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
