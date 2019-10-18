# This python module expands on the host abstract class
# vCenter adds objects and methods for intent operation against a vMware vCenter
#

from dynstudio.host import abstractHost

from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect

serviceInstance = None

class Host(abstractHost):
    """
    The Host Object for DynStudio vCenter Implementation.
    Ties to a real VMWare vCenter.
    Attributes of this class relate to objects managed by vCenter.
    Methods of this class relate to changes in the
    Management Plane of the vCenter. 
    """
    def __init__(self, name, host=None):
        self.name = name
        self.host = host
        if not self.host:
            self.host = name

    def connect(self, user, pswd, port=443):
        serviceInstance = SmartConnectNoSSL(host=self.host, user=user, pwd=pswd, port=port)
        return serviceInstance