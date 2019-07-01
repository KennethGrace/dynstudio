#! /usr/bin/python
import sys
import json

import exception as ex

import host
from modules.cisco import cisco_ucs

VERSION = "0.0.1"

min_args = 7

def hand_off(key):
    pass

def main(*args, **kwargs):
    host = cisco_ucs.CiscoUCS(args[0])
    host.connect(*args[1:3])
    host.lan.vlanGroups[args[3]].removeVlanByID(args[5])
    host.lan.vlanGroups[args[4]].addVlanByID(args[5])
    host.commit()
    host.disconnect()
    pass

if __name__ == '__main__':
    print('DYNSTUDIO v'+VERSION)
    if len(sys.argv) >= min_args:
        main(*sys.argv[1:])
    else:
        raise ValueError(ex.args(len(sys.argv),min_args))
