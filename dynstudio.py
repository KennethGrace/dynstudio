#! /usr/bin/python
import sys
import json

import exception as ex

import host
from modules.cisco import cisco_ucs

VERSION = "0.0.1"

min_args = 2

def hand_off(key):
    pass

def main(*args, **kwargs):
    pass

if __name__ == '__main__':
    print('DYNSTUDIO v'+VERSION)
    if len(sys.argv) >= min_args:
        main(*sys.argv[1:])
    else:
        raise ValueError(ex.args(len(sys.argv),min_args))
