
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
    def __init__(self, parent, name):
        self.name = name
        self.rn_url = render(self.rn_url,name=name)
        self.url = parent.url + self.rn_url

    def createL3Out(self, name):
        pyld = fetch('cisco/aci/l3extOut.json', tenant=self, name=name)
        t_url = self.url+'out-{}.json'.format(name)
        r = url.post(t_url, pyld, json=True)
        obj = routing.l3extOut(self, name)
        self.l3extOuts.update({name: obj})
        return obj, r

    def createVRF(self, name):
        pyld = fetch('cisco/aci/fvCtx.json', tenant=self, name=name)
        t_url = self.url+'ctx-{}.json'.format(name)
        r = url.post(t_url, pyld, json=True)
        obj = routing.fvCtx(self, name)
        self.fvCtxs.update({name: obj})
        return obj, r

class cmnFvTenant(fvTenant):
    def __init__(self, parent, name):
        super().__init__(parent, name)

    def createOSPF(self, name):
        # Create OSPF Interface Policy
        pyld = fetch('cisco/aci/ospfIfPol.json', tenant=self, name=name)
        t_url = self.url+'ospfIfPol-{}.json'.format(name)
        r = url.post(t_url, pyld, json=True)
        obj = routing.ospfIfPol(self, name)
        self.ospfIfPols.update({name: obj})
        return obj, r