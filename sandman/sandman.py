#!/usr/bin/python3
import os
import sys
import os.path
import argparse
import traceback

__author__ = 'Mark Valdez'

"""
TODO: document
"""


def print_sys_info():
    print('-------------------')
    print('Python Version Info: ' + sys.version)
    print('Author: ' + __author__)
    print('Current Working Directory: ' + os.getcwd())
    print('-------------------')
    print('')


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir',
                        dest='parent_dir',
                        help='Absolute path to parent directory')
    return parser


if __name__ == '__main__':
    print_sys_info()
    op = configure_options()
    if len(sys.argv) == 1:
        op.print_help()
        sys.exit(1)
    try:
        args = op.parse_args()
        # TODO: do stuff
    except Exception as e:
        traceback.print_exc()
        op.print_help()
        sys.exit(1)
