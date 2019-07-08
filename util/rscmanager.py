# This module is used as an interface for other modules to load 
# static resources held in the resource folder
#
#
import sys, os

from jinja2 import Environment, BaseLoader, Template

import json

rsc_dir = r'../resource'

def grab(resource_name):
    o = None
    d = os.path.dirname(__file__)
    r = open(d+'/'+rsc_dir+'/'+resource_name)
    i = r.read()
    r.close()
    if resource_name.endswith('.json'):
        o = json.loads(i)
    return o

def fetch(resource_name, **kwargs):
    d = os.path.dirname(__file__)
    r = open(d+'/'+rsc_dir+'/'+resource_name)
    i = r.read()
    r.close()
    tpl = Template(i)
    o = tpl.render(kwargs)
    if resource_name.endswith('.json'):
        f_o = json.loads(o)
    return f_o

def render(str_tmp, **kwargs):
    """
    Accept a Jinja formatted string and keyword arguments, read
    the arguments into the string using Jinja.
    """
    tpl = Environment(loader=BaseLoader).from_string(str_tmp)
    return tpl.render(kwargs)