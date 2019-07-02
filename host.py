import importlib
from abc import ABC, abstractmethod

class abstractHost(ABC):
    name = 'null'
    def __init__(self, name):
        self.name = name
        pass

    @abstractmethod
    def connect(self):
        pass

def newHost(name, vendor, module):
    mod = importlib.import_module('modules.{0}.{1}'.format(vendor, module))
    hostObject = getattr(mod, 'Host')
    return hostObject(name)
