#!/usr/bin/python3
import argparse
import os
import subprocess
import sys
import traceback

__author__ = 'Mark Valdez'

"""
Simple utility to execute git commands.  Useful when you have to batch process git commands against a 
remote repository.

TODO: replace print with proper logger
"""


def print_sys_info():
    print('-------------------')
    print('Python Version Info: ' + sys.version)
    print('Author: ' + __author__)
    print('Current Working Directory: ' + os.getcwd())
    print('-------------------')
    print('')


def dogit_clone(args, project):
    cwd = os.path.join(os.getcwd(), args.destination)
    if not os.path.exists(cwd):
        raise UtilityManagerException(cwd + ' does not exist')
    if args.url is None:
        raise UtilityManagerException('URL required for using clone command')
    cmd = 'git clone ' + args.options + ' ' + args.url + project
    doit_cmd(cmd, cwd)


def dogit_commit(args, project):
    cwd = os.path.join(os.getcwd(), args.destination, project)
    if not os.path.exists(cwd):
        raise UtilityManagerException(cwd + ' does not exist')
    cmd = 'git commit ' + args.options
    doit_cmd(cmd, cwd)


def dogit_add(args, project):
    cwd = os.path.join(os.getcwd(), args.destination, project)
    if not os.path.exists(cwd):
        raise UtilityManagerException(cwd + ' does not exist')
    cmd = 'git add ' + args.options
    doit_cmd(cmd, cwd)


def dogit_log(args, project):
    cwd = os.path.join(os.getcwd(), args.destination, project)
    if not os.path.exists(cwd):
        raise UtilityManagerException(cwd + ' does not exist')
    cmd = 'git log ' + args.options
    doit_cmd(cmd, cwd)


def doit_cmd(cmd, cwd):
    print('Executing: ' + cmd)
    print('Destination: ' + cwd)
    pr = subprocess.Popen(cmd,
                          cwd=cwd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    stdout, stderr = pr.communicate()
    print(stdout)
    print(stderr)


def get_child_dirs(parent_dir):
    return [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]


def configure_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clone',
                        action='store_true',
                        help='Git command to execute a clone')
    parser.add_argument('--commit',
                        action='store_true',
                        help='Git command to execute a commit')
    parser.add_argument('--add',
                        action='store_true',
                        help='Git comment to execute an add')
    parser.add_argument('--log',
                        action='store_true',
                        help='Git comment to execute a log')
    parser.add_argument('--opts',
                        dest='options',
                        default='',
                        help='Git command options')
    parser.add_argument('--url',
                        dest='url',
                        help='Git repository location')
    parser.add_argument('-d', '--destination',
                        dest='destination',
                        help='Destination directory. Relative to current working dir.')
    parser.add_argument('-p', '--projects',
                        dest='projects',
                        help='Explicitly specify project name(s) separated by spaces')
    parser.add_argument('-r', "--recursive",
                        action='store_true',
                        help="Use destination's child directories to implicitly determine project(s)")
    return parser


class UtilityManagerException(Exception):
    def __init__(self, msg):
        self.msg = msg


class UtilityManager(object):
    def __init__(self, args):

        if args.projects is not None:
            plist = args.projects.split()
        elif args.recursive:
            plist = get_child_dirs(args.destination)
        else:
            raise UtilityManagerException('Missing option: Choose either recursive or destination for projects')

        if args.clone:
            for p in plist:
                dogit_clone(args, p)
        elif args.commit:
            for p in plist:
                dogit_commit(args, p)
        elif args.add:
            for p in plist:
                dogit_add(args, p)
        elif args.log:
            for p in plist:
                dogit_log(args, p)
        else:
            raise UtilityManagerException('Unsupported command')


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
