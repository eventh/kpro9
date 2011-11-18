# -*- coding: utf-8 -*-
# Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
# Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
# Sigurd Wien and Jaroslav Fibichr.
#
# This file is part of CSjark.
#
# CSjark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSjark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CSjark.  If not, see <http://www.gnu.org/licenses/>.
"""
Module for performing the C preprocessor step on C header files.

The parse_file() function calls the external C preprocessor program,
while post_cpp() function removes output from the preprocessor which
pycparser does not support.
"""
import sys
import os
from subprocess import Popen, PIPE

from config import Options


def parse_file(filename, platform=None, folders=None, includes=None):
    """Run a C header or code file through C preprocessor program.

    'filename' is the file to feed CPP.
    'platform' is the platform to simulate.
    'folders' is directories to -Include.
    'includes' is a set of filename to #include.
    """
    # Just read the content of the file if we don't want to use cpp
    if not Options.use_cpp:
        with open(filename, 'r') as f:
            return f.read()

    if folders is None:
        folders = set()
    if includes is None:
        includes = []

    config = Options.match_file(filename)
    path_list = _get_cpp()

    # Add fake includes and includes from configuration
    path_list.append(r'-I../utils/fake_libc_include')

    # Add as include the folder the files are located in
    if os.path.dirname(filename):
        folders.add(os.path.dirname(filename))

    # Add all -Include cpp arguments
    if folders or config.include_dirs:
        folders |= set(config.include_dirs)
        path_list.extend('-I%s' % i for i in folders)

    # Define macros
    if platform is not None:
        path_list.extend(['-D%s=%s' % (i, j)
                for i, j in platform.macros.items()])

    # Add any C preprocesser arguments from CLI or config
    path_list.extend('-D%s' % i for i in config.defines)
    path_list.extend('-U%s' % i for i in config.undefines)
    path_list.extend(config.arguments)

    if config.includes or includes:
        # Find all includes and their dependencies
        unprosess = [filename] + includes + config.includes
        processed = set()
        all_includes = []
        while len(unprosess) > 0:
            file = unprosess.pop(0)
            processed.add(file)
            if file in all_includes:
                all_includes.remove(file) # Move it to the front
            all_includes.insert(0, file)
            unprosess.extend(i for i in Options.match_file(file).includes
                    if i not in processed)


        feed = '\n'.join('#include "%s"' % i for i in all_includes) + '\n'
        #print(feed)
    else:
        path_list.append(filename)
        feed = ''

    # Missing universal newlines forces input to expect bytes
    if sys.platform.startswith('win'):
        newlines = True
    else:
        feed = bytes(feed, 'ascii')
        newlines = False

    # Call C preprocessor with args and file
    with Popen(path_list, stdin=PIPE, stdout=PIPE,
            stderr=PIPE, universal_newlines=newlines) as proc:
        text, warnings = proc.communicate(input=feed)
    if warnings:
        print(warnings.strip(), file=sys.stderr)

    return '\n'.join(post_cpp(text.split('\n')))


def post_cpp(lines):
    """Perform a post preprocessing step, removing unsupported C code."""
    tokens = ('#pragma', '__extension__', '__attribute', '__inline__')
    for i, line in enumerate(lines):
        for token in tokens:
            if token in line:
                lines[i] = line.split(token, 1)[0]
    lines.append(';\n') # Ugly hack to avoid feeding pycparser an "empty" file
    return lines


def _get_cpp():
    """Find the path and args to the C preprocessor."""
    if Options.cpp_path is not None:
        return Options.cpp_path
    path = ['cpp']
    if sys.platform == 'win32':
        path = ['../utils/cpp.exe'] # Windows don't come with a CPP
    elif sys.platform == 'darwin':
        path = ['gcc', '-E'] # Fix for a bug in Mac GCC 4.2.1
    return path

