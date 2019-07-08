from __future__ import unicode_literals
from dynstudio.util.rscmanager import fetch, render

class l3extOut():
    """
    ACI Layer 3 Exstention Out
    """
    rn_url = r'out-{{name}}/'
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url, name=name)
        self.url = parent.url + self.rn_url
        pass

class fvCtx():
    """
    ACI Virtual Routing and Forwarding
    This object is for managing all the properties and sub objects
    of a VRF object within ACI
    """
    rn_url = r'ctx-{{name}}/'
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url,name=name)
        self.url = parent.url + self.rn_url




#########################
###                   ###
###  Special Objects  ###
###                   ###
#########################

class ospfIfPol():
    """
    ACI OSPF Interface Policy
    This object is only a member of the common tenant
    to be used by the common tenant object and refrenced
    in other tenants.
    """
    rn_url = r'ospfIfPol-{{name}}/'
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url,name=name)
        self.url = parent.url + self.rn_url

