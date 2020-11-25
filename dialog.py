# -*- coding: utf-8 -*-

"""

dialog

User interaction functions

"""


import collections
import datetime
import logging
import sys
import textwrap



#
# Constants
#


DATE_ORDERS = {
    # Assume ISO date format (yyyy-mm-dd etc)
    '-': 'ymd',
    # Assume German date format (d.m., d.m.yy, d.m.yyyy)
    '.': 'dmy',
    # Assume US-american date format (m/d, m/d/yy, m/d/yyyy)
    '/': 'mdy'}

DEFAULT_OUTPUT_WIDTH = 70

FS_DATE_DE = '%d.%m.%Y'
FS_DATE_ISO = '%Y-%m-%d'

FS_MESSAGE = '%(levelname)-8s| %(message)s'


#
# Helper functions
#


def date_from_components(date_components, order='dmy', default=None):
    """Determine a date from the given components and the order"""
    if not isinstance(default, datetime.date):
        default = datetime.date.today()
    #
    try:
        day_index = order.index('d')
        month_index = order.index('m')
        year_index = order.index('y')
    except ValueError as value_error:
        raise ValueError(
            'Invalid order {0!r}!'.format(order)) from value_error
    #
    if len(order) != 3:
        raise ValueError('Invalid order {0!r}!'.format(order))
    #
    try:
        day = int(date_components[day_index])
    except (IndexError, ValueError):
        day = default.day
    #
    try:
        month = int(date_components[month_index])
    except (IndexError, ValueError):
        month = default.month
    #
    try:
        year = int(date_components[year_index])
    except (IndexError, ValueError):
        year = default.year
    #
    if year < 100:
        year = year + 2000
    #
    return datetime.date(year, month, day)


def date_from_string(date_string, default=None):
    """Try to determine a date from the given date_string
    Fill missing parts from default if a default date object was provided,
    else from today's date.
    Return a date object or rase a ValueError
    """
    if not isinstance(default, datetime.date):
        default = datetime.date.today()
    #

    for separator, date_order in DATE_ORDERS.items():
        if separator in date_string:
            return date_from_components(
                date_string.split(separator),
                order=date_order,
                default=default)
        #
    #
    raise ValueError(
        'Could not determine a date from {0!r}!'.format(date_string))


#
# Classes
#


class WrappedTextLogger:

    """Log wrapped text"""

    def __init__(self,
                 width=DEFAULT_OUTPUT_WIDTH):
        """Initialize an internal textwrapper"""
        self.textwrapper = textwrap.TextWrapper(width=width)
        #self.width = width

    def wrap_preserving_linebreaks(self, source_text):
        """Generator function yieling lines wrapped to maximum <self.width>
        columns, but preserving pre-existing line breaks
        """
        for source_line in source_text.splitlines():
            if source_line:
                for output_line in self.textwrapper.wrap(source_line):
                    yield output_line
                #
            else:
                yield source_line
            #
        #

    def _log(self, level, msg, args):
        """Mix the logging functions with self.wrap_preserving_linebreaks().
        Adapted from
        <https://github.com/python/cpython/blob/3.6/Lib/logging/__init__.py>
        (lines 277-279)
        """
        if args:
            if (len(args) == 1 and isinstance(args[0], collections.Mapping)
                    and args[0]):
                args = args[0]
            #
            msg = msg % args
        #
        for line in self.wrap_preserving_linebreaks(msg):
            logging.log(level, line)
        #

    def log(self, level, msg, *args):
        """logging.log() mixed with self.wrap_preserving_linebreaks()"""
        self._log(level, msg, args)

    def debug(self, msg, *args):
        """logging.debug() mixed with self.wrap_preserving_linebreaks()"""
        self._log(logging.DEBUG, msg, args)

    def info(self, msg, *args):
        """logging.info() mixed with self.wrap_preserving_linebreaks()"""
        self._log(logging.INFO, msg, args)

    def warning(self, msg, *args):
        """logging.warning() mixed with self.wrap_preserving_linebreaks()"""
        self._log(logging.WARNING, msg, args)

    def error(self, msg, *args):
        """logging.error() mixed with self.wrap_preserving_linebreaks()"""
        self._log(logging.ERROR, msg, args)

    def critical(self, msg, *args):
        """logging.critical() mixed with self.wrap_preserving_linebreaks()"""
        self._log(logging.CRITICAL, msg, args)

    fatal = critical


class Interrogator:

    """Object for user interaction"""

    # Todo: english version that can be subclassed by a german one

    answers = {True: 'ja', False: 'nein'}
    pseudo_loglevel = '(INPUT)'

    def __init__(self,
                 message_format=FS_MESSAGE,
                 default_prompt='-> ',
                 width=DEFAULT_OUTPUT_WIDTH,
                 logger=None):
        """Set internal message format"""
        self.default_prompt = default_prompt
        self.message_format = message_format
        if isinstance(logger, WrappedTextLogger):
            self.logger = logger
        else:
            self.logger = WrappedTextLogger(width=width)
        #

    def get_input(self, question_text, *args, **kwargs):
        """Return user input"""
        if question_text:
            self.logger.info(question_text, *args)
        #
        input_prompt = self.message_format % collections.defaultdict(
            str,
            levelname=self.pseudo_loglevel,
            message=kwargs.get('prompt') or self.default_prompt)
        return input(input_prompt).strip()

    def get_input_with_preset(self, question_text, *args, **kwargs):
        """Ask a question with a preset answer.
        Return user input if provided, else return the preset answer
        """
        preset_answer = kwargs.pop('preset_answer', None)
        args = list(args)
        if (len(args) == 1 and isinstance(args[0], collections.Mapping)):
            args[0]['preset_answer'] = preset_answer
            placeholder = '%(preset_answer)r'
        else:
            args.append(preset_answer)
            placeholder = '%r'
        #
        answer = self.get_input(
            '{0}\n(Standardwert ist {1})'.format(
                question_text,
                placeholder),
            *args,
            **kwargs)
        if answer:
            return answer
        #
        return preset_answer

    def ask_polar_question(self, question_text, *args, **kwargs):
        """Ask for user input, set preset_answer if no input was provided.
        Return True or False
        """
        preset_value = kwargs.pop('preset_value', False)
        kwargs['preset_answer'] = self.answers[preset_value]
        answer = self.get_input_with_preset(question_text, *args, **kwargs)
        for (answer_value, answer_text) in self.answers.items():
            if answer_text.startswith(answer.lower()):
                return answer_value
            #
        #
        self.logger.info('Ich interpretiere das als %r.', self.answers[False])
        return False

    def confirm(self, question_text, *args, **kwargs):
        """Ask for confirmation"""
        kwargs['preset_value'] = False
        return self.ask_polar_question(question_text, *args, **kwargs)

    def ask_date(self, question_text, *args, **kwargs):
        """Ask for a date.
        Return a date object, or raise a ValueError
        """
        not_after = kwargs.pop('not_after', None)
        not_before = kwargs.pop('not_before', None)
        default = kwargs.pop('default', None)
        answer = self.get_input(question_text, *args, **kwargs)
        if answer:
            for date_format in (FS_DATE_DE, FS_DATE_ISO):
                try:
                    answer_datetime = datetime.datetime.strptime(
                        answer,
                        date_format)
                except ValueError:
                    continue
                else:
                    answer_date = answer_datetime.date()
                    break
                #
            else:
                answer_date = date_from_string(answer, default=default)
            #
            if isinstance(not_after,
                          datetime.date) and answer_date > not_after:
                raise ValueError(
                    'Das Datum darf nicht nach dem {0} liegen!'.format(
                        not_after.strftime(FS_DATE_DE)))
            #
            if isinstance(not_before,
                          datetime.date) and answer_date < not_before:
                raise ValueError(
                    'Das Datum darf nicht vor dem {0} liegen!'.format(
                        not_before.strftime(FS_DATE_DE)))
            #
            return answer_date
        elif isinstance(default, datetime.date):
            return default
        #
        raise ValueError('Kein Datum angegeben und kein Standardwert!')


#
# Functions
#


def exit_error(message, *args, logger=None, returncode=1):
    """Print an error message and exit"""
    if not isinstance(logger, WrappedTextLogger):
        logger = logging
    #
    logging.error(message, *args)
    sys.exit(returncode)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
