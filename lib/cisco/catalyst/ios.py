import builtins

from dynstudio.util import url
from dynstudio.util.rscmanager import fetch, render

from dynstudio.host import abstractHost

from dynstudio.lib.cisco.catalyst import switching

from netmiko import ConnectHandler, ssh_exception
from paramiko import ssh_exception as para_ssh_exception

class Host(abstractHost):
    """ Cisco Catalyst IOS Network Host
    This class models the authorization and system level attributes and functions of a
    Cisco Catalyst IOS Network device. Subclasses model distinct operational capacities
    of this device type.
    """
    def __init__(self, name):
        self.name = name

    def connect(self, username, password):
        params = {
            'host': self.name,
            'device_type' : 'cisco_ios',
            'username': username,
            'password': password,
            'port': 22
        }
        self.connection = ConnectHandler(**params)

    def disconnect(self):
        pass
