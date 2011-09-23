import sys
import argparse
import cparser
import config


def main():
    parser = argparse.ArgumentParser(description='Generate Wireshark'
            ' dissectors from C structs.')
    
    parser.add_argument('header', nargs='?', action='store')
    #Flags listed first:
    # Verbose flag
    parser.add_argument('-v', '--verbose', action='store_true',
            dest='verbose', help='Print information about AST tree, ect.')
    # Debug flag
    parser.add_argument('-d', '--debug', action='store_true',
            dest='debug', help='Enable debugger')
    # No CPP flag
    parser.add_argument('-nocpp', action='store_false',
            dest='cpp', help='Disable C preprocessor')
    #Followed by input and output files
    # C-header file
    parser.add_argument('-ch', '--cheader', nargs='*',
            action='store', dest='hfile',
            type=str, help='C-header file to parse')
    # Configuration file
    parser.add_argument('-c', '--config', nargs='*',
            type=str, action='store',help='Configuration file')
    # Write output to destination file
    parser.add_argument('-output', nargs='*',
            type=str, help='Write output to file')

    args = parser.parse_args()
    if len(sys.argv) > 1:
        print(args)
        if args.header:
            cparser.parse_file(args.header)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

