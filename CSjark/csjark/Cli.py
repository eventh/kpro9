import sys
import argparse
import cparser
import config
import os


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
            type=str, dest='config', action='store',help='Configuration file'
    'to parse')
    # Write output to destination file
    parser.add_argument('-output', nargs='*',
            type=str, help='Write output to file')



    args = parser.parse_args()

    #make for loop for support of multiple header files at once
    if args.header:
        if not os.path.exists(args.header):
            print('Error: headerfile does not exist')

    if args.config:
        if not os.path.exists(args.config):
            print('Error: configfile does not exist')


    if len(sys.argv) > 1:
        print(args)
        if args.header:
            if os.path.exists(args.header):
                cparser.parse_file(args.header , use_cpp=args.cpp)
            else:
                print('error')
        if args.config:
            if os.path.exists(args.config):
                config.parse_file(args.config)
            else:
                print('error')
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

