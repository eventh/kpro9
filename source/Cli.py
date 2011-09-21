import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate Wireshark'
            ' dissectors from C structs.')

    # C-header file
    parser.add_argument('-ch', '--cheader', nargs='*',
            help='C-header file to parse', metavar='HEADER')

    # Configuration file
    parser.add_argument('-c', '--config', action='store',
            help='Configuration file', metavar='FILE', dest='configname',
            nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    # Write output to destination file
    parser.add_argument('-output', nargs='*', help='Write output to file',
            metavar='FILE', dest='test.txt',
            type=argparse.FileType('w'), default=sys.stdout)

    # Verbose flag
    parser.add_argument('-v', '--verbose', action='store_true',
            dest='verbose', help='Print information about AST tree, ect.')

    # Debug flag
    parser.add_argument('-d', '--debug', action='store_true',
            dest='debug', help='Enable debugger')

    # No CPP flag
    parser.add_argument('-nocpp', action='store_false',
            dest='cpp', help='Disable C preprocessor')

    # Set default values
    parser.set_defaults(verbose=False, debug=False, cpp=True)


    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()

