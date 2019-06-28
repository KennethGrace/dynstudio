#! /usr/bin/python
import sys
import exception as ex

import modules.host
import modules.cisco

min_args = 2

def hand_off(key):
    pass

def main(*args, **kwargs):
    print(args)
    host = modules.host.Host('10.215.27.1')
    cisco_host = modules.cisco.cisco_ucs.CiscoUCS('10.215.27.1')
    pass

if __name__ == '__main__':
    if len(sys.argv) >= min_args:
        main(*sys.argv[1:])
    else:
        raise ValueError(ex.args(len(sys.argv),min_args))
