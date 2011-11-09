"""
Module for performing C preprocessor step on C header files.
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
        folders.union(config.include_dirs)
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
        all_includes = []
        while len(unprosess) > 0:
            file = unprosess.pop(0)
            if file in all_includes:
                all_includes.remove(file) # Move it to the front
            all_includes.insert(0, file)
            unprosess.extend(Options.match_file(file).includes)

        feed = '\n'.join('#include "%s"' % i for i in all_includes) + '\n'
    else:
        path_list.append(filename)
        feed = ''

    # Call C preprocessor with args and file
    with Popen(path_list, stdin=PIPE, stdout=PIPE,
            universal_newlines=True) as proc:
        if sys.platform.startswith('sunos'):
            # Missing universal newlines forces input to expect bytes
            text = proc.communicate(input=bytes(feed, 'ascii'))[0]
        else:
            text = proc.communicate(feed)[0]

    return '\n'.join(post_cpp(text.split('\n')))


def post_cpp(lines):
    """Perform a post preprocessing step.

    Should remove #pragma directives.
    """
    for i, line in enumerate(lines):
        if '#pragma' in line:
            lines[i] = line.split('#pragma', 1)[0]
        if '__attribute__' in line:
            lines[i] = line.split('__attribute__', 1)[0]
    lines.append(';') # Ugly hack to avoid feeding pycparser an "empty" file
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

