"""
Module for performing C preprocessor step on C header files.
"""
import sys
import os
from subprocess import Popen, PIPE

from config import Options


def parse_file(filename, platform=None, includes=None):
    """Run a C header or code file through C preprocessor program.

    'filename' is the file to feed CPP.
    'platform' is the platform to simulate.
    'includes' is a set of filename to #include.
    """
    # Just read the content of the file if we don't want to use cpp
    if not Options.use_cpp:
        with open(filename, 'r') as f:
            return f.read()

    if includes is None:
        includes = []

    config = Options.match_file(filename)
    path_list = _get_cpp()

    # Add fake includes and includes from configuration
    path_list.append(r'-I../utils/fake_libc_include')

    # Add as include the folder the files are located in
    if os.path.dirname(filename):
        path_list.append('-I%s' % os.path.dirname(filename))

    # Define macros
    if platform is not None:
        #path_list.append('-undef') # Remove system-specific defines
        path_list.extend(['-D%s=%s' % (i, j)
                for i, j in platform.macros.items()])

    # Add any C preprocesser arguments from CLI or config
    path_list.extend('-I%s' % i for i in config.include_dirs)
    path_list.extend('-D%s' % i for i in config.defines)
    path_list.extend('-U%s' % i for i in config.undefines)
    path_list.extend(config.arguments)

    # Add arguments to #include if 'includes' is given
    if config.includes or includes:
        inc = config.includes + includes + [filename]
        include_text = '\n'.join('#include "%s"' % i for i in inc) + '\n'
    else:
        path_list.append(filename)
        include_text = ''

    # Call C preprocessor with args and file
    pipe = Popen(path_list, stdin=PIPE, stdout=PIPE, universal_newlines=True)
    text = pipe.communicate(include_text)[0]

    return '\n'.join(post_cpp(text.split('\n')))


def post_cpp(lines):
    """Perform a post preprocessing step.

    Should remove #pragma directives.
    """
    for i, line in enumerate(lines):
        if '#pragma' in line:
            lines[i] = line.split('#pragma', 1)[0]
    return lines


def pre_cpp(lines):
    """Perform a pre preprocessing step."""
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

