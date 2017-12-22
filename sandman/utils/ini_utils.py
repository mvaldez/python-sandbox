#!/usr/bin/python3
import os
import sys
import os.path
import argparse
import traceback
import configparser

__author__ = 'Mark Valdez'

"""
Simple utility for dealing with ini files
"""


def print_sys_info():
    print('-------------------')
    print('Python Version Info: ' + sys.version)
    print('Author: ' + __author__)
    print('Current Working Directory: ' + os.getcwd())
    print('-------------------')
    print('')


def get_child_dirs(parent_dir):
    print('Getting all child directories for ' + parent_dir)
    return [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]


def get_sections(args, dirs):
    config = configparser.ConfigParser()
    results = set()
    for child in dirs:
        print('Reading ' + os.path.join(args.parent_dir, child, args.file_name))
        config.read(os.path.join(args.parent_dir, child, args.file_name))
        sections = config.sections()
        for s in sections:
            if s not in results:
                results.add(s)
    return results


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir',
                        dest='parent_dir',
                        help='Absolute path to parent directory')
    parser.add_argument('--file-name',
                        dest='file_name',
                        help='ini file name')
    parser.add_argument('--list-sections',
                        action='store_true',
                        help='List unique sections for all directories under parent directory')
    return parser


class UtilityManagerException(Exception):
    def __init__(self, msg):
        self.msg = msg


class UtilityManager(object):
    def __init__(self, args):
        if args.list_sections:
            if not os.path.exists(args.parent_dir):
                raise UtilityManagerException('Parent directory' + args.parent_dir + ' does not exist')
            children = get_child_dirs(args.parent_dir)
            print('Sections found: {}'.format(get_sections(args, children)))


if __name__ == '__main__':
    print_sys_info()
    op = configure_options()
    if len(sys.argv) == 1:
        op.print_help()
        sys.exit(1)
    try:
        um = UtilityManager(op.parse_args())
    except Exception as e:
        traceback.print_exc()
        op.print_help()
        sys.exit(1)

