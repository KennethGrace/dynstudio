#! /usr/bin/python
import sys
import json

import exception as ex

import host
from modules.cisco import cisco_ucs

min_args = 2

def hand_off(key):
    pass

def main(*args, **kwargs):
    print(args)
    cisco_ucs_host = cisco_ucs.CiscoUCS('172.27.0.1')
    cisco_ucs_host.connect('var1', 'var2')
    cisco_ucs_host.queryH('fabric/lan/net-group-ACI-PCI')
    print(cisco_ucs_host)
    #print(json.dumps(r, indent=2))

if __name__ == '__main__':
    if len(sys.argv) >= min_args:
        main(*sys.argv[1:])
    else:
        raise ValueError(ex.args(len(sys.argv),min_args))
