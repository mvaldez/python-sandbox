#!/usr/bin/python3
import argparse
import os
import subprocess
import sys
import traceback

__author__ = 'Mark Valdez'
"""
Simple utility to execute commands line tasks.  Useful when you have to 
batch process commands.

TODO: replace print with proper logger
"""


def print_sys_info():
    print('-------------------')
    print('Python Version Info: ' + sys.version)
    print('Author: ' + __author__)
    print('Current Working Directory: ' + os.getcwd())
    print('-------------------')
    print('')


def get_child_dirs(parent_dir):
    return [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]


def exec_cmd(args):
    if args.recursive:
        print('Recursive option enabled')
        children = get_child_dirs(args.dest_dir)
        for child in children:
            cwd = os.path.join(args.dest_dir, child)
            doit_cmd(args, cwd)
    else:
        doit_cmd(args, args.dest_dir)


def doit_cmd(args, dest):
    print('CWD: ' + dest)
    print('Executing: ' + args.exec_cmd)
    if args.verbose:
        print('Verbose option enabled')
        pr = subprocess.Popen(args.exec_cmd,
                              cwd=dest,
                              shell=True,
                              stderr=subprocess.PIPE)
    else:
        pr = subprocess.Popen(args.exec_cmd,
                              cwd=dest,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    stdout, stderr = pr.communicate()
    print(stdout)
    print(stderr)


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cmd', dest='exec_cmd', help="Command to execute")
    parser.add_argument('-d', "--dest-dir", dest='dest_dir', help="Destination working directory. Absolute path.")
    parser.add_argument('-r', "--recursive", action='store_true', help="Execute command in child directories")
    parser.add_argument('-v', '--verbose', action='store_true', help='Output stdout to console during execution')
    return parser


class UtilityManagerException(Exception):
    def __init__(self, msg):
        self.msg = msg


class UtilityManager(object):
    def __init__(self, args):
        if os.path.exists(args.dest_dir):
            exec_cmd(args)
        else:
            raise UtilityManagerException(args.dest_dir + ' does not exist')


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
