#!/usr/bin/env python3

"""
================================================================================
PROGRAM: Listcopy

LICENSE: MIT

FILE: lcp.py

DESCRIPTION: copies files from lines in a text document to a given directory.
Useful for collecting files scattered over multiple directories into one
place after compiling their locations in a list, especially when the files
have no pattern to filter against (for instance with find or other tools).

USAGE: lcp.py --help

CONTRIBUTORS: rockhazardz@gmail.com

TIP: Sublime Text and Atom will paste the full path of any files you copy to the
clipboard, allowing easy construction of source files for use with this script.
================================================================================
"""


import sys
import argparse
import pprint
from pathlib import Path
from textwrap import dedent
from shutil import copy2


def get_file_list(sourceFile):
    """split lines from source file into list and strip non-files"""
    try:
        with open(sourceFile) as file:
            sourceList = file.read().splitlines()
        fileList = []
        for line in sourceList:
            if Path(line).is_file():
                fileList.append(line)
    except FileNotFoundError as error:
        sys.exit(error)
    return fileList


def copy_files(fileList, destinationPath):
    """copy listed files to destination directory"""
    dpath = Path(destinationPath)
    if dpath.is_dir():
        faults = []
        destination = str(dpath)
        print("copying...")
        for fileName in fileList:
            try:
                copy2(fileName, destination)
                print(fileName)
            except FileNotFoundError as error:
                faults.append(error)
                print(error)
                continue
        print("to: {}".format(destination))
        print("Operation completed with {} errors.".format(len(faults)))
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
        pp = pprint.PrettyPrinter(indent=4)
        fileList = get_file_list(args.list[0])
        print("Found {} valid files:".format(len(fileList)))
        pp.pprint(fileList)
    elif args.copy:
        fileList = get_file_list(args.copy[0])
        copy_files(fileList, args.copy[1])

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
