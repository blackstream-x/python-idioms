#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

tkinter-gui-wizard.py.py

Skeleton script
(Tkinter-based GUI assistant)

"""


import argparse
import logging
import mimetypes
import os
import pathlib
import sys
import tkinter

from tkinter import filedialog
from tkinter import messagebox

# local modules

import gui_commons

#
# Constants
#


SCRIPT_NAME = '...'
HOMEPAGE = 'https://github.com/blackstream-x/PROJECT_NAME'
MAIN_WINDOW_TITLE = 'PROJECT_NAME: ...'

SCRIPT_PATH = pathlib.Path(sys.argv[0])
# Follow symlinks
if SCRIPT_PATH.is_symlink():
    SCRIPT_PATH = SCRIPT_PATH.readlink()
#

LICENSE_PATH = SCRIPT_PATH.parent / 'LICENSE'
try:
    LICENSE_TEXT = LICENSE_PATH.read_text()
except OSError as error:
    LICENSE_TEXT = '(License file is missing: %s)' % error
#

VERSION_PATH = SCRIPT_PATH.parent / 'version.txt'
try:
    VERSION = VERSION_PATH.read_text().strip()
except OSError as error:
    VERSION = '(Version file is missing: %s)' % error
#

# Phases
CHOOSE_FILE = 'choose_file'
STEP_1 = 'step_1'
STEP_2 = 'step_2'
STEP_3 = 'step_3'

PHASES = (
    CHOOSE_FILE,
    STEP_1,
    STEP_2,
    STEP_3,
)

PANEL_NAMES = {
    STEP_1: 'User interaction step 1',
    STEP_2: 'User interaction step 2',
    STEP_3: 'User interaction step 3',
}


#
# Helper Functions
#


...


#
# Classes
#


class Namespace(dict):

    # pylint: disable=too-many-instance-attributes

    """A dict subclass that exposes its items as attributes.

    Warning: Namespace instances only have direct access to the
    attributes defined in the visible_attributes tuple
    """

    visible_attributes = ('items', )

    def __repr__(self):
        """Object representation"""
        return '{0}({1})'.format(
            type(self).__name__,
            super().__repr__())

    def __dir__(self):
        """Members sequence"""
        return tuple(self)

    def __getattribute__(self, name):
        """Access a visible attribute
        or return an existing dict member
        """
        if name in type(self).visible_attributes:
            return object.__getattribute__(self, name)
        #
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(
                '{0!r} object has no attribute {1!r}'.format(
                    type(self).__name__, name)) from error
        #

    def __setattr__(self, name, value):
        """Set an attribute"""
        self[name] = value

    def __delattr__(self, name):
        """Delete an attribute"""
        del self[name]


class UserInterface():

    """GUI using tkinter"""

    with_border = dict(
        borderwidth=2,
        padx=5,
        pady=5,
        relief=tkinter.GROOVE)
    grid_fullwidth = dict(
        padx=4,
        pady=2,
        sticky=tkinter.E + tkinter.W)

    # pylint: disable=attribute-defined-outside-init

    def __init__(self, file_path):
        """Build the GUI"""
        self.main_window = tkinter.Tk()
        self.main_window.title(MAIN_WINDOW_TITLE)
        self.variables = Namespace(
            current_panel=None,
            disable_next_button=False,
            errors=[],
            file_name=tkinter.StringVar(),
            original_path=file_path,
            panel_display=tkinter.StringVar(),
            traced_vars=Namespace(
                traced_int=tkinter.IntVar(),
                traced_str=tkinter.StringVar(),
            ),
        )
        # Trace changes to some variables
        for (_, variable) in self.variables.traced_vars.items():
            variable.trace_add('write', self.apply_changes)
        #
        self.widgets = Namespace(
            action_area=None,
            buttons_area=None,
        )
        overview_frame = tkinter.Frame(self.main_window)
        file_label = tkinter.Label(
            overview_frame,
            text='Original file:')
        file_label.grid(
            padx=4, pady=2, row=0, column=0, sticky=tkinter.W)
        selected_file = tkinter.Entry(
            overview_frame,
            width=60,
            state=tkinter.DISABLED,
            textvariable=self.variables.file_name)
        selected_file.grid(
            padx=4, pady=2, row=0, column=1, sticky=tkinter.W)
        choose_button = tkinter.Button(
            overview_frame,
            text='Choose another …',
            command=self.do_choose_file)
        choose_button.grid(
            padx=4, pady=4, row=0, column=2, sticky=tkinter.W)
        panel_display = tkinter.Label(
            overview_frame,
            textvariable=self.variables.panel_display,
            justify=tkinter.LEFT)
        panel_display.grid(
            padx=4, pady=4, row=1, column=0, columnspan=3, sticky=tkinter.W)
        overview_frame.grid(**self.grid_fullwidth)
        self.do_choose_file(
            keep_existing=True,
            quit_on_empty_choice=True)
        self.main_window.mainloop()

    def do_choose_file(self,
                       keep_existing=False,
                       preset_path=None,
                       quit_on_empty_choice=False):
        """Choose an image via file dialog"""
        self.variables.current_panel = CHOOSE_FILE
        file_path = self.variables.original_path
        if preset_path:
            if not preset_path.is_dir():
                initial_dir = str(preset_path.parent)
            #
        elif file_path:
            initial_dir = str(file_path.parent)
        else:
            initial_dir = os.getcwd()
        #
        while True:
            if not keep_existing or file_path is None:
                selected_file = filedialog.askopenfilename(
                    initialdir=initial_dir)
                if not selected_file:
                    if quit_on_empty_choice:
                        self.quit()
                    #
                    return
                #
                file_path = pathlib.Path(selected_file)
            #
            # Example: check for an image mime type,
            # and show an error dialog and retry
            # if the selected file is not an image
            file_type = mimetypes.guess_type(file_path)[0] or '(unknown)'
            if not file_type.startswith('image/'):
                messagebox.showerror(
                    'Not an image',
                    f'{file_path.name!r} is a file of type {file_type},'
                    ' but an image is required.',
                    icon=messagebox.ERROR)
                initial_dir = str(file_path.parent)
                file_path = None
                continue
            #
            # Set original_path and load file data
            self.variables.original_path = file_path
            ...
            # set the displayed file name
            self.variables.file_name.set(file_path.name)
            break
        #
        self.next_panel()

    def apply_changes(self, **unused_arguments):
        """Apply changes"""
        ...

    def panel_step_1(self):
        """User interaction step 1"""
        frame = tkinter.Frame(
            self.widgets.action_area,
            **self.with_border)
        ...
        frame.grid(**self.grid_fullwidth)

    def next_action(self):
        """Execute the next action"""
        current_index = PHASES.index(self.variables.current_panel)
        next_index = current_index + 1
        try:
            next_phase = PHASES[next_index]
        except IndexError as error:
            raise ValueError(
                f'Phase number #{next_index} out of range') from error
        #
        method_display = (
            f'Action method for phase #{next_index} ({next_phase})')
        method_name = f'do_{next_phase})'
        try:
            action_method = getattr(self, method_name)
        except AttributeError:
            logging.warning('%s is undefined', method_display)
        else:
            try:
                action_method()
            except NotImplementedError as error:
                raise ValueError(
                    f'{method_display} has not been implemented yet') \
                    from error
            #
        #
        self.variables.current_phase = next_phase

    def next_panel(self):
        """Execute the next action and go to the next panel"""
        try:
            self.next_action()
        except ValueError as error:
            self.variables.errors.append(str(error))
        #
        self.__show_panel()

    def previous_panel(self):
        """Go to the next panel"""
        phase_name = self.variables.current_panel
        phase_index = PHASES.index(phase_name)
        method_display = (
            f'Rollback method for phase #{phase_index} ({phase_name})')
        method_name = f'rollback_{phase_name})'
        try:
            rollback_method = getattr(self, method_name)
        except AttributeError:
            logging.warning('%s is undefined', method_display)
        else:
            self.variables.current_phase = PHASES[phase_index - 1]
            try:
                rollback_method()
            except NotImplementedError:
                self.variables.errors.append(
                    f'{method_display} has not been implemented yet')
            #
        #
        self.__show_panel()

    def quit(self, event=None):
        """Exit the application"""
        del event
        self.main_window.destroy()

    def show_about(self):
        """Show information about the application
        in a modal dialog
        """
        gui_commons.InfoDialog(
            self.main_window,
            (SCRIPT_NAME,
             'Version: {0}\nProject homepage: {1}'.format(
                VERSION, HOMEPAGE)),
            ('License:', LICENSE_TEXT),
            title='About…')
        #

    def __show_errors(self):
        """Show errors if there are any"""
        if self.variables.errors:
            errors_frame = tkinter.Frame(
                self.widgets.action_area,
                **self.with_border)
            for message in self.variables.errors:
                error_value = tkinter.Label(
                    errors_frame,
                    text=message,
                    justify=tkinter.LEFT)
                error_value.grid(
                    padx=4,
                    sticky=tkinter.W)
            #
            self.variables.errors.clear()
            errors_frame.grid(**self.grid_fullwidth)
        #

    def __show_panel(self):
        """Show a panel.
        Add the "Previous", "Next", "Choose another relase",
        "About" and "Quit" buttons at the bottom
        """
        for area in ('action_area', 'buttons_area'):
            try:
                self.widgets[area].grid_forget()
            except AttributeError:
                pass
            #
        #
        self.widgets.action_area = tkinter.Frame(self.main_window)
        try:
            panel_method = getattr(
                self,
                'panel_%s' % self.variables.current_phase)
        except AttributeError:
            self.variables.errors.append(
                'Panel for Phase %r has not been implemented yet,'
                ' going back to phase %r.' % (
                    self.variables.current_phase,
                    self.variables.current_panel))
            self.variables.current_phase = self.variables.current_panel
            panel_method = getattr(
                self,
                'panel_%s' % self.variables.current_phase)
            self.variables.disable_next_button = False
        else:
            self.variables.current_panel = self.variables.current_phase
        #
        self.variables.panel_display.set(
            '%s (panel %s of %s)' % (
                PANEL_NAMES[self.variables.current_panel],
                PHASES.index(self.variables.current_panel),
                len(PHASES) - 1))
        self.__show_errors()
        panel_method()
        self.widgets.action_area.grid(**self.grid_fullwidth)
        #
        self.widgets.buttons_area = tkinter.Frame(
            self.main_window,
            **self.with_border)
        #
        buttons_grid = dict(padx=5, pady=5, row=0)
        if self.variables.current_phase in (STEP_2, STEP_3):
            previous_button_state = tkinter.NORMAL
        else:
            previous_button_state = tkinter.DISABLED
        #
        previous_button = tkinter.Button(
            self.widgets.buttons_area,
            text='\u25c1 Previous',
            command=self.previous_panel,
            state=previous_button_state)
        previous_button.grid(column=0, sticky=tkinter.W, **buttons_grid)
        #
        if self.variables.disable_next_button or \
                self.variables.current_phase == PHASES[-1]:
            next_button_state = tkinter.DISABLED
        else:
            next_button_state = tkinter.NORMAL
        #
        self.variables.disable_next_button = False
        next_button = tkinter.Button(
            self.widgets.buttons_area,
            text='\u25b7 Next',
            command=self.next_panel,
            state=next_button_state)
        next_button.grid(column=1, sticky=tkinter.W, **buttons_grid)
        about_button = tkinter.Button(
            self.widgets.buttons_area,
            text='About…',
            command=self.show_about)
        about_button.grid(column=3, sticky=tkinter.E, **buttons_grid)
        quit_button = tkinter.Button(
            self.widgets.buttons_area,
            text='Quit',
            command=self.quit)
        quit_button.grid(column=4, sticky=tkinter.E, **buttons_grid)
        self.widgets.buttons_area.columnconfigure(2, weight=100)
        self.widgets.buttons_area.grid(**self.grid_fullwidth)


#
# Functions
#


def __get_arguments():
    """Parse command line arguments"""
    argument_parser = argparse.ArgumentParser(
        description='Do something using a GUI wizard')
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
    argument_parser.add_argument(
        'selected_file',
        nargs='?',
        type=pathlib.Path,
        help='A file. If none is provided,'
        ' the script will ask for a file.')
    return argument_parser.parse_args()


def main(arguments):
    """Main script function"""
    logging.basicConfig(
        format='%(levelname)-8s\u2551 %(funcName)s → %(message)s',
        level=arguments.loglevel)
    selected_file = arguments.selected_file
    if selected_file and not selected_file.is_file():
        selected_file = None
    #
    UserInterface(selected_file)


if __name__ == '__main__':
    sys.exit(main(__get_arguments()))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
