import argparse
import utilities
import os.path
from enum import Enum


class outputFileType(Enum):
    """Flag for type of output file entered"""
    _ascii = 1
    _binary = 2


class Parser:
    """Parses command line arguments"""

    def __init__(self):
        """add doc"""
        self.args = None
        self.output_file_type = None
        self.no_merge_flag = False
    def parse_command_line(self):
        """creates a ArgumentParsers and parses the console for given arguments
        Also checks for mistakes in console arguments

        Arguments:

        Returns None
        """
        arg_parser = argparse.ArgumentParser()

        arg_parser.add_argument("-i", "--input", required=True, type=lambda s: self.file_extension_check(("stl", ), s),
                                help="numele unui fisier de input, in format STL, ASCII sau binary")
        arg_parser.add_argument("-o", "--output", type=lambda s: self.file_extension_check(("stl",), s),
                                help="numele unui fisier, unde va fi salvat output-ul programului")
        arg_parser.add_argument("--no_merge", help='vertices with coordinates under threshold'
                                                   ' will not be merged for statistical purposes', action='store_true')

        exclusive_group = arg_parser.add_mutually_exclusive_group()
        exclusive_group.add_argument("--ascii", help="output-ul programului va fi salvat in format STL ASCII",
                                     action="store_true")
        exclusive_group.add_argument("--binary", help="output-ul programului va fi salvat in format STL binary",
                                     action="store_true")

        self.args = arg_parser.parse_args()

        if self.args.input is None:
            utilities.error("Error Input file missing", 1)

        if self.args.output:
            print("outputFile entered")
            if self.args.ascii or self.args.binary:
                print("output flag entered")
                if self.args.ascii:
                    self.output_file_type = outputFileType._ascii
                elif self.args.binary:
                    self.output_file_type = outputFileType._binary
            else:
                utilities.error("Error no mentioned Type(ascii or binary) for output File ", 1)
        if (self.args.ascii or self.args.binary) and (not self.args.output):
            utilities.error("Output file Type mentioned without output file entered ", 1)
        if self.args.no_merge:
            self.no_merge_flag = True

    def file_extension_check(self, choices, file_name):
        """checks if file extension matches approved list

        Arguments:
        choices (tuple): approved extensions as strings
        file_name (str): name of file from console

        Returns string containing input from console
        """
        ext = os.path.splitext(file_name)[1][1:]
        if ext not in choices:
            utilities.error("outputFile doesn't end with one of {}".format(choices), exitCode=1)
        return file_name
