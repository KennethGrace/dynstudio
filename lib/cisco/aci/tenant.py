
import requests

from dynstudio.util import url
from dynstudio.util.rscmanager import fetch, render

from dynstudio.lib.cisco.aci import routing

class fvTenant():
    """
    ACI Tenant
    """
    rn_url = r'node/mo/uni/tn-{{name}}/'
    fvCtxs = {}
    l3extOuts = {}
    ospfIfPols = {}
    def __init__(self, host, name):
        self.name = name
        self.rn_url = render(self.rn_url,name=name)
        self.url = host.url + self.rn_url

    def createL3Out(self, name):
        obj = fetch('cisco/apic/l3extOut.json', tenant=self, name=name)
        t_url = self.url+'out-{}.json'.format(name)
        r = url.post(t_url, obj, json=True)
        new_l3extOut = routing.l3extOut(self, name)
        self.l3extOuts.update({name: new_l3extOut})
        return new_l3extOut

    def createVRF(self, name):
        obj = fetch('cisco/apic/fvCtx.json', tenant=self, name=name)
        t_url = self.url+'ctx-{}.json'.format(name)
        r = url.post(t_url, obj, json=True)
        new_fvCtx = routing.fvCtx(self, name)
        self.fvCtxs.update({name: new_fvCtx})
        return new_fvCtx

    def createOSPF(self, name):
        # Create OSPF Interface Policy
        obj = fetch('cisco/apic/ospfIfPol.json', tenant=self, name=name)
        t_url = self.url+'ospfIfPol-{}.json'.format(name)
        r = url.post(t_url, obj, json=True)
        new_ospfIfPol = routing.ospfIfPol(self, name)
        self.ospfIfPols.update({name: new_ospfIfPol})
        return new_ospfIfPol

class cmnFvTenant(fvTenant):
    def __init__(self, host, name):
        pass