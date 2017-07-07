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

TIP: Sublime Text and Atom will paste the full path of any files you copy to
the clipboard, allowing easy construction of source files for use with this
script.
================================================================================
"""


import sys
import argparse
from pathlib import Path
from textwrap import dedent
from shutil import copy2
# copytree won't write to an existing directory, but copy_tree will
from distutils.dir_util import copy_tree


def number_lines(fileList, index):
    """Ensures all line numbers have leading zeros matching the size of largest
    line number."""
    maxZeros = str(len(fileList))
    natNum = str(index + 1)
    nZeros = len(maxZeros) - len(natNum)
    if nZeros:
        zeros = "0" * nZeros
        lineNumber = zeros + natNum + " >> "
    else:
        lineNumber = natNum + " >> "
    return lineNumber


def get_file_list(sourceFile=None):
    """split lines from source file into list and strip non-files"""
    try:
        with open(sourceFile) as file:
            sourceList = file.read().splitlines()
        fileList = []
        for line in sourceList:
            if Path(line).exists():
                fileList.append(line)
        for line in sourceList:
            if not line:
                fileList.remove(line)
    except FileNotFoundError as error:
        sys.exit(error)
    except IsADirectoryError as error:
        sys.exit(error)
    return fileList


def copy_files(fileList, destinationPath, fcplib=copy2, tcplib=copy_tree):
    """copy listed files to destination directory"""
    dpath = Path(destinationPath)
    if dpath.is_dir():
        faults = []
        destination = str(dpath)
        print("copying files to {} ...".format(destination))
        for fileName in fileList:
            try:
                fcplib(fileName, destination)
                print("{}\"{}\"".format(number_lines(
                    fileList, fileList.index(fileName)), fileName))
            except IsADirectoryError:
                # create new directory then recursively copy contents of source
                newDir = str(Path(destination, Path(fileName).stem))
                tcplib(fileName, newDir)
                print("{}\"{}\"".format(number_lines(
                    fileList, fileList.index(fileName)), fileName))
                continue
            except FileNotFoundError as error:
                faults.append(error)
                print("{}\"{}\"".format(number_lines(
                    fileList, fileList.index(fileName)), error))
                continue
            
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
        fileList = get_file_list(args.list[0])
        print("Found {} valid files:".format(len(fileList)))
        for line in fileList:
            print("{}\"{}\"".format(number_lines(
                fileList, fileList.index(line)), line))
    elif args.copy:
        fileList = get_file_list(args.copy[0])
        copy_files(fileList, args.copy[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
