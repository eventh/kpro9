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

    path_list = _get_cpp()

    # Add fake includes and includes from configuration
    path_list.append(r'-I../utils/fake_libc_include')

    # Add as include the folder the files are located in
    if os.path.dirname(filename):
        path_list.append('-I%s' % os.path.dirname(filename))

    # Add arguments to #include if 'includes' is given
    #if includes is not None:
    #    print("wtf", ['-i "%s"' % i for i in includes])
    #    path_list.extend(['-include%s' % i for i in includes])
    # TODO: cpp.exe dont accept -include,wtf!

    # Define macros
    if platform is not None:
        #path_list.append('-undef') # Remove system-specific defines
        path_list.extend(['-D%s=%s' % (i, j)
                for i, j in platform.macros.items()])

    # Add any C preprocesser arguments from CLI or config
    path_list.extend('-I%s' % i for i in Options.cpp_include_dirs)
    path_list.extend('-include "%s"' % i for i in Options.cpp_includes)
    path_list.extend('-D%s' % i for i in Options.cpp_defines)
    path_list.extend('-U%s' % i for i in Options.cpp_undefines)
    path_list.extend(Options.cpp_args)

    # Call C preprocessor with args and file
    path_list.append(filename)
    pipe = Popen(path_list, stdout=PIPE, universal_newlines=True)
    text = pipe.communicate()[0]

    return '\n'.join(post_cpp(text.split('\n')))


def post_cpp(lines):
    """Perform a post preprocessing step.

    Should remove #pragma directives.
    """
    for i, line in enumerate(lines):
        if '#pragma' in line:
            lines[i] = line.split('#pragma', 1)[0] + '\n'
    return lines


def pre_cpp(lines):
    """Perform a pre preprocessing step."""
    return lines


'''Not needed yet.
def pre_cpp_files(files):
    """Modify all 'files' to ensure we can parse them."""
    # Create directory for holding the new files
    tmp_folder = 'csjark_tmp_files'
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder, exist_ok=True)
    if not os.path.isdir(tmp_folder):
        raise IOError('Failed to create tmp folder %s' % tmp_folder)

    # Go though one file at a time and rewrite them
    mapping = {}
    for filename in files:
        lines = pre_process(filename)

        # Write the new lines in a file
        new_file = os.path.join(tmp_folder, filename)
        os.makedirs(os.path.dirname(new_file), exist_ok=True)
        with open(new_file, 'w') as f:
            f.write(''.join(lines))

        mapping[new_file] = filename

    # Return new filenames and mapping of new to old filename
    return list(mapping.keys()), mapping
'''


def _get_cpp():
    """Find the path and args to the C preprocessor."""
    path = ['cpp']
    if sys.platform == 'win32':
        path = ['../utils/cpp.exe'] # Windows don't come with a CPP
    elif sys.platform == 'darwin':
        path = ['gcc', '-E'] # Fix for a bug in Mac GCC 4.2.1
    return path

