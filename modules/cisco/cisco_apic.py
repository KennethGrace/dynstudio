import requests
from host import Host

class CiscoAPIC(Host):
    def __init__(self, name):
        self.name = name

    def connect(self, user, pswd):
        pass