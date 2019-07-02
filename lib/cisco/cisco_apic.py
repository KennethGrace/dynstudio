from dynstudio.host import abstractHost

import requests

class Host(abstractHost):
    def __init__(self, name):
        self.name = name

    def connect(self, user, pswd):
        pass