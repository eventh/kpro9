"""
Module for performing C preprocessor step on C header files.
"""
import sys
import os
from subprocess import Popen, PIPE

from config import Options


def _get_cpp():
    """Find the path and args to the C preprocessor."""
    path = ['cpp']
    if sys.platform == 'win32':
        path = ['../utils/cpp.exe'] # Windows don't come with a CPP
    elif sys.platform == 'darwin':
        path = ['gcc', '-E'] # Fix for a bug in Mac GCC 4.2.1
    return path


def parse_files(filenames, platform=None):
    pass


def parse_file(filename, platform=None):
    """Run 'filename' through C preprocessor."""
    # Just read the content of the file if we don't want to use cpp
    if not Options.use_cpp:
        with open(filename, 'r') as f:
            return f.read()

    file = filename
    path_list = _get_cpp()

    # Add fake includes and includes from configuration
    path_list.append(r'-I../utils/fake_libc_include')
    path_list.extend(Options.cpp_includes)

    # Add as include the folder the files are located in
    # Need to use absolute paths to avoid a pycparser #line bug
    if os.path.dirname(filename):
        path_list.append(r'-I%s' %
                os.path.abspath(os.path.dirname(filename)))

    # Create temporary header with platform-specific macros
    if platform is not None:
        file = 'temp-%s.tmp.h' % os.path.split(filename)[1]
        with open(file, 'w') as fp:
            fp.write('%s\n#include "%s"\n\n' % (
                    platform.header, os.path.basename(filename)))

    # Call C preprocessor with args and file
    path_list.append(file)
    pipe = Popen(path_list, stdout=PIPE, universal_newlines=True)
    text = pipe.communicate()[0]

    # Delete temp file, can't use real tempfile as we call CPP program
    if file != filename:
        os.remove(file)

    return text

