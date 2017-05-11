#!/usr/bin/env python3
"""
===============================================================================
Listcopy copies files from lines in a text document to a specified directory.
===============================================================================
"""


import sys
import argparse
from pathlib import Path
from textwrap import dedent
from shutil import copy2


def get_file_list(sourceFile):
    """split lines from source file into list"""
    try:
        with open('{}'.format(sourceFile)) as file:
            fileList = file.read().splitlines()
    except FileNotFoundError as error:
        sys.exit(error)
    return fileList


def copy_files(destinationPath, fileList):
    """copy listed files to destination directory"""
    dpath = Path(destinationPath)
    if dpath.is_dir():
        dpath = str(dpath)
        for line in fileList:
            try:
                copy2(line, dpath)
            except FileNotFoundError as error:
                print(error)
                continue
    else:
        sys.exit("Invalid destination.")


def main(*args):
    """
    COMMANDLINE OPTIONS
    """
    parser = argparse.ArgumentParser(
        prog=sys.argv[0][2:], description=dedent("""\
            %(prog)s copies any valid files listed in the source file on separate 
            lines into the given destination directory."""),
        epilog="""Author: rockhazard License: MIT""")
    parser.add_argument('--version', help='print version info then exit',
                        version='%(prog)s 1.0', action='version')
    parser.add_argument('--list', '-l', nargs=1, metavar=('SOURCE_FILE'),
                        help='List all files in source')
    parser.add_argument('--copy', '-c', nargs=2,
                        metavar=('SOURCE_FILE', 'DIRECTORY'),
                        help='Copy all files listed in SOURCE_FILE to DIRECTORY.')

    args = parser.parse_args()

    if args.list:
        print(get_file_list(args.list[0]))
    elif args.copy:
        lines = get_file_list(args.copy[0])
        copy_files(args.copy[1], lines)

if __name__ == "__main__":  # if not imported as module, execute script
    sys.exit(main(sys.argv[1:]))
