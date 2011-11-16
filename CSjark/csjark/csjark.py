#! /usr/bin/env python3
"""
A module for creating Wireshark dissectors from C structs.

Usage:
    csjark.py [-h] [-v] [-d] [-s] [-f [header [header ...]]]
          [-c [config [config ...]]] [-x [path [path ...]]]
          [-o [output]] [-p] [-n] [-C [cpp]] [-i [header [header ...]]]
          [-I [directory [directory ...]]]
          [-D [name=definition [name=definition ...]]]
          [-U [name [name ...]]] [-A [argument [argument ...]]]
          [header] [config]


Generate Wireshark dissectors from C structs.

positional arguments:
  header                C header file to parse
  config                yaml config file to parse

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print detailed information
  -d, --debug           print debugging information
  -s, --strict          only generate dissectors for known structs
  -n, --nocpp           disable C preprocessor
  -p, --placeholders    generate placeholder config file for unknown structs
  -f, --file            C header or code file(s) to parse
  -c, --config          configuration file(s) to parse
  -x, --exclude         file or folders to exclude from parsing
  -o, --output          write output to directory/file
  -C, --CPP             which C preprocessor to use
  -i, --include         process file as Cpp #include "file" directive
  -I, --Includes        directories to be searched for Cpp includes
  -D, --Define          predefine name as a Cpp macro
  -U, --Undefine        cancel any previous Cpp definition of name
  -A, --Additional      any additional C preprocessor arguments

Example:
"python csjark.py -v --nocpp headerfile.h configfile.yml"
"""
import sys
import os
import argparse

import cpp
import cparser
import config
from config import Options, FileConfig
from field import ProtocolField


def parse_args(args=None):
    """Parse arguments given in sys.argv.

    'args' is a list of strings to parse instead of sys.argv.
    """
    parser = argparse.ArgumentParser(
            description='Generate Wireshark dissectors from C structs.')

    # A single C header file
    parser.add_argument('header', nargs='?', help='C header file to parse')

    # A single config file
    parser.add_argument('config', nargs='?', help='yaml config file to parse')

    # Verbose flag
    parser.add_argument('-v', '--verbose', action='store_true',
            default=Options.verbose, help='print detailed information')

    # Debug flag
    parser.add_argument('-d', '--debug', action='store_true',
            default=Options.debug, help='print debugging information')

    # Strict flag, not in use yet
    parser.add_argument('-s', '--strict', action='store_true',
            default=Options.strict,
            help='only generate dissectors for known structs')

    # A list of C header files
    parser.add_argument('-f', '--file', metavar='header',
            default=[], nargs='*', help='C header or code file(s) to parse')

    # A list of configuration files
    parser.add_argument('-c', '--config', metavar='config', dest='configs',
            default=[], nargs='*', help='configuration file(s) to parse')

    # A list of files or folders to ignore
    parser.add_argument('-x', '--exclude', metavar='path', default=[],
            nargs='*', help='file or folders to exclude from parsing')

    # Write output to destination file
    parser.add_argument('-o', '--output', metavar='output',
            nargs='?', help='write output to directory/file')

    # Generate placeholder config files
    parser.add_argument('-p', '--placeholders', action='store_true',
            default=Options.generate_placeholders,
            help='generate placeholder config file for unknown structs')

    # No CPP flag
    parser.add_argument('-n', '--nocpp', action='store_false', dest='nocpp',
            default=Options.use_cpp, help='disable C preprocessor')

    # Argument for specifying which CPP to use
    parser.add_argument('-C', '--CPP', metavar='cpp',
            nargs='?', help='which C preprocessor to use')

    # CPP include arguments
    parser.add_argument('-i', '--include', metavar='header', default=[],
            nargs='*', help='process file as Cpp #include "file" directive')

    # CPP Includes directories arguments
    parser.add_argument('-I', '--Includes', metavar='directory', default=[],
            nargs='*', help='directories to be searched for Cpp includes')

    # CPP Define macro arguments
    parser.add_argument('-D', '--Define', metavar='name=definition',
            default=[], nargs='*', help='predefine name as a Cpp macro')

    # CPP Undefine macro arguments
    parser.add_argument('-U', '--Undefine', metavar='name', default=[],
            nargs='*', help='cancel any previous Cpp definition of name')

    # Additional CPP arguments
    parser.add_argument('-A', '--Additional', metavar='argument', default=[],
            nargs='*', help='any additional C preprocessor arguments')

    # Parse arguments
    if args is None:
        namespace = parser.parse_args()
    else:
        namespace = parser.parse_args(args)

    # Store options
    Options.verbose = namespace.verbose
    Options.debug = namespace.debug
    Options.strict = namespace.strict
    Options.excludes.extend(os.path.normpath(i) for i in namespace.exclude)
    Options.generate_placeholders = namespace.placeholders
    Options.use_cpp = namespace.nocpp
    Options.cpp_path = namespace.CPP
    Options.default.includes = namespace.include
    Options.default.include_dirs = namespace.Includes
    Options.default.defines = namespace.Define
    Options.default.undefines = namespace.Undefine
    Options.default.args = namespace.Additional

    headers = namespace.file
    if namespace.header:
        headers.append(namespace.header)

    configs = namespace.configs
    if namespace.config:
        configs.append(namespace.config)

    # Find out where to store output from the generator
    if namespace.output:
        path = os.path.join(os.path.dirname(sys.argv[0]), namespace.output)
        if os.path.isdir(path):
            Options.output_dir = path
        else:
            Options.output_file = path

    # Need to provide either a header file or a config file
    if len(headers) == 1 and not configs and headers[0][-4:] == '.yml':
        configs.append(headers.pop())
    if not headers and not configs:
        parser.print_help()
        sys.exit(2)

    # Make sure the files provided actually exists
    missing = [i for i in headers + configs if not os.path.exists(i)]
    if missing:
        print('Unknown file(s): %s' % ', '.join(missing))
        sys.exit(2)

    # Recursively search folders for C header and config files
    def files_in_folder(var, file_extensions):
        folders = [folder for folder in var if os.path.isdir(folder)]
        while len(folders):
            folder = folders.pop()
            if folder in var:
                var.remove(folder)
            for path in os.listdir(folder):
                full_path = os.path.normpath(os.path.join(folder, path))
                if full_path in Options.excludes:
                    continue
                if os.path.isdir(full_path):
                    folders.append(full_path)
                elif os.path.splitext(path)[1] in file_extensions:
                    var.append(full_path)

    files_in_folder(headers, ('.h', '.hpp'))
    files_in_folder(configs, ('.yml', ))

    return headers, configs


def parse_headers(headers):
    """Parse 'headers' to create a Wireshark protocol dissector."""
    folders = {os.path.dirname(i) for i in headers} # Folders to -Include
    failed = [] # Filenames, platforms pairs we have failed to parse so far

    def include_heuristics(filename, platform, error):
        """Try to find missing includes from error message."""
        include = None
        msg = str(error)
        if 'before: ' in msg:
            key = msg.rsplit('before: ', 1)[1].strip()
            include = cparser.StructVisitor.all_known_types.get(key, None)
        #print(filename, include)
        if include is None:
            return False, None

        # Problem with typedef, TODO: improve this error handling
        if os.path.normpath(filename) == os.path.normpath(include):
            return False, None

        new_error = create_dissector(filename, platform, folders, [include])
        if new_error != error:
            FileConfig.add_include(filename, include)
            if new_error is None:
                return True, None # Worked
            return False, new_error # Try more
        return False, None # Give up

    def print_status(tries=[]):
        """Print a status message with how many headers failed to parse."""
        if tries and tries[-1] == 0:
            return
        tries.append(len({i for i, j, k in failed}))
        if tries[-1] == 0:
            msg = 'Successfully parsed all %i' % len(headers)
        else:
            msg = 'Failed to parse %i out of %i' % (tries[-1], len(headers))
        print('[%i] %s header files (%i platforms)' % (
                len(tries), msg, len(Options.platforms)))

    def filenames_have_shared_path(f1, f2):
        p1 = os.path.dirname(f1)
        p2 = os.path.dirname(f2)
        c = os.path.commonprefix([p1, p2])
        return c == p1 or c == p2

    print('[0] Attempting to parse %i header files' % len(headers))

    # First try, in the order given through the CLI
    counter = 0
    for filename in headers:
        for platform in Options.platforms:
            error = create_dissector(filename, platform, folders)
            if error is not None:
                failed.append([filename, platform, error])
        counter += 1
        print("Parsed file %i '%s'" % (counter, filename))
    print_status()

    # Try to include files based on decoding the error messages
    work_list = failed[:]
    for tmp in range(2, 4):
        for i in reversed(range(len(work_list))):
            status, new_error = include_heuristics(*work_list[i])
            if not status and new_error is not None:
                work_list[i][2] = new_error
            else:
                if status:
                    failed.remove(work_list[i])
                work_list.pop(i)
        print_status()

    # Try to include all who worked as it might help
    failed_names = [filename for filename, platform, error in failed]
    includes = [f for f in headers if f not in failed_names and
                            filenames_have_shared_path(filename, f)]

    for i in reversed(range(len(failed))):
        filename, platform, tmp = failed.pop(i)
        error = create_dissector(filename, platform, folders, includes)
        if error is None:
            # Worked, record it in case anyone else needs this file
            for inc in includes:
                FileConfig.add_include(filename, inc)
            includes.append(filename)
        else:
            failed.append([filename, platform, error])
    print_status()

    # Try to include files based on decoding the error messages
    work_list = failed[:]
    for tmp in range(5, 7):
        for i in reversed(range(len(work_list))):
            status, new_error = include_heuristics(*work_list[i])
            if not status and new_error is not None:
                work_list[i][2] = new_error
            else:
                if status:
                    failed.remove(work_list[i])
                work_list.pop(i)
        print_status()

    # Give up!
    for filename, platform, error in failed:
        print('Skipped "%s":%s as it raised %s' % (
                filename, platform.name, repr(error)))

    return len({i for i, j, k in failed})

def create_dissector(filename, platform, folders=None, includes=None):
    """Parse 'filename' to create a Wireshark protocol dissector.

    'filename' is the C header/code file to parse.
    'platform' is the platform we should simulate.
    'folders' is a set of all folders to -Include.
    'includes' is a set of filenames to #include.
    Returns the error if parsing failed, None if succeeded.
    """
    try:
        text = cpp.parse_file(filename, platform, folders, includes)
        ast = cparser.parse(text, filename)
        cparser.find_structs(ast, platform)
    except OSError:
        raise
    except Exception as err:
        # TODO some cleanup, now half-finished things might linger!
        if Options.verbose:
            print('Failed "%s":%s which raised %s' % (
                    filename, platform.name, repr(err)))
        if Options.debug:
            sys.excepthook(*sys.exc_info())
        return err

    if Options.verbose:
        print("Parsed header file '%s':%s successfully." % (
                filename, platform.name))

    #if Options.debug:
    #    ast.show()


def write_dissectors_to_file(all_protocols):
    """Write lua dissectors to file(s)."""
    # Delete output_file if it already exists
    if Options.output_file and os.path.isfile(Options.output_file):
        os.remove(Options.output_file)

    # Sort which dissectors to write out
    protocols = all_protocols
    if Options.strict:
        def find_proto(proto):
            found = []
            # Possible endless loop?
            for child in proto.children:
                if isinstance(child, ProtocolField):
                    found.append(child.proto.name)
                found.extend(find_proto(child))
            return found

        protocols = {p.name: p for p in protocols.values() if p.id}
        for proto in list(protocols.values()):
            names = find_proto(proto.dissectors.values())
            protocols.update({name: all_protocols[name] for name in names})

    # Generate and write lua dissectors
    for name, proto in protocols.items():
        path = '%s.lua' % name
        flag = 'w'
        if Options.output_dir:
            path = '%s/%s' % (Options.output_dir, path)
        elif Options.output_file:
            path = Options.output_file
            flag = 'a'

        code = proto.generate()
        with open(path, flag) as f:
            f.write(code)

        if Options.verbose:
            print("Wrote %s to '%s' (%i platform(s))" %
                    (name, path, len(proto.children)))

    return len(protocols)


def write_delegator_to_file():
    """Write the lua file which delegates dissecting to dissectors."""
    filename = 'luastructs.lua'
    if Options.output_dir:
        filename = '%s/%s' % (Options.output_dir, filename)

    with open(filename, 'w') as f:
        f.write(Options.delegator.generate())

    if Options.verbose:
        print("Wrote delegator file to '%s'" % filename)


def write_placeholders_to_file(protocols):
    """Write a placeholder file for 'protocols' with no configuration."""
    if not protocols or not Options.generate_placeholders:
        return

    text, count = config.generate_placeholders(protocols)
    filename = 'placeholders.yml'
    with open(filename, 'w') as f:
        f.write(text)

    if Options.verbose:
        print("Wrote %i config placeholders to '%s'" % (count, filename))


def main():
    """Run the CSjark program."""
    headers, configs = parse_args()

    # Parse config files
    for filename in configs:
        config.parse_file(filename)
    Options.prepare_for_parsing()

    # Remove excluded headers
    for path in set(Options.excludes):
        for filename in [i for i in headers if i.startswith(path)]:
            headers.remove(filename)

    # Parse all headers to create protocols
    failed = parse_headers(headers)

    # Write dissectors to disk
    protocols = cparser.StructVisitor.all_protocols
    wrote = write_dissectors_to_file(protocols)
    write_delegator_to_file()
    write_placeholders_to_file(protocols)

    # Write out a status message
    if failed:
        count = len(headers) - failed
        msg = 'Successfully parsed %i out of %i files' % (count, len(headers))
    else:
        msg = 'Successfully parsed all %i files' % len(headers)
    print("%s for %i platforms, created %i dissectors" % (
            msg, len(Options.platforms), wrote))


if __name__ == "__main__":
    main()

