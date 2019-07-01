#! /usr/bin/python
import sys, os
import json

import exception as ex

import host
from modules.cisco import cisco_ucs

VERSION = "0.0.1"

min_args = 2

def main(*args, **kwargs):
    sys.path.append(os.getcwd())
    mod = __import__(args[0])
    ent = getattr(mod, 'main')
    ent()
    pass

if __name__ == '__main__':
    print('DYNSTUDIO v'+VERSION)
    if len(sys.argv) >= min_args:
        main(*sys.argv[1:])
    else:
        raise ValueError(ex.args(len(sys.argv),min_args))
