from dynstudio.util import url
from dynstudio.util.rscmanager import fetch, render, grab

class Fabric():
    rn_url = r'node/mo/uni/infra/'
    portChannels = {}
    interfaceProfiles = {}
    def __init__(self, parent):
        self.parent = parent
        self.url = parent.url + self.rn_url

    def createPortChannel(self, name, vpc=False):
        obj = infraAccBndlGrp(self, name)
        self.portChannels.update({name: obj})
        pyld = fetch('cisco/aci/infraAccBndlGrp.json', name=name)
        if vpc:
            pyld['infraAccBndlGrp']['attributes']['lagT'] = 'node'
        t_url = self.url + 'funcprof/accbundle-{}.json'.format(name)
        r = url.post(t_url, pyld, json=True)
        return obj, r

    def createInterfaceProfile(self, name):
        obj = infraAccPortP(self, name)
        self.interfaceProfiles.update({name: obj})
        pyld = fetch('cisco/aci/infraAccPortP.json', name=name)
        t_url = self.url + 'accportprof-{}.json'.format(name)
        r = url.post(t_url, pyld, json=True)
        return obj, r

#########################
###                   ###
###  Special Objects  ###
###                   ###
#########################

class infraNodeP():
    def __init__(self, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url, name=name)
        self.url = parent.url + self.rn_url

class infraAccBndlGrp():
    """
    ACI PC/vPC Interface Policy
    Used to define a port group which connects down from two leaves to legacy switch hardware
    """
    children = []
    rn_url = 'funcprof/accbundle-{{name}}/'
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url, name=name)
        self.url = parent.url + self.rn_url

    def setVPC(self, vpc):
        lagT = 'link'
        if vpc:
            lagT = 'node'
        pyld = {"infraAccBndlGrp":{"attributes":{"dn":"uni/infra/funcprof/accbundle-"+self.name,"lagT":lagT},"children":[]}}
        r = url.post(self.url[:-1]+'.json', pyld, json=True)
        return r

    def setAEP(self, profileName):
        tDn = 'uni/infra/attentp-' + profileName
        pyld = {"infraRsAttEntP":{"attributes":{"tDn":tDn},"children":[]}}
        r = url.post(self.url+'rsattEntP.json', pyld, json=True)
        return r

    def setCDP(self, policyName):
        pyld = {"infraRsCdpIfPol":{"attributes":{"tnCdpIfPolName":policyName},"children":[]}}
        r = url.post(self.url+'rscdpIfPol.json', pyld, json=True)
        return r

    def setLinkLevel(self, policyName):
        pyld = {"infraRsHIfPol":{"attributes":{"tnFabricHIfPolName":policyName},"children":[]}}
        r = url.post(self.url+'rshIfPol.json', pyld, json=True)
        return r

    def setPortChannelPolicy(self, policyName):
        pyld = {"infraRsLacpPol":{"attributes":{"tnLacpLagPolName":policyName},"children":[]}}
        r = url.post(self.url+'rslacpPol.json', pyld, json=True)
        return r

    def setLLDP(self, policyName):
        pyld = {"infraRsLldpIfPol":{"attributes":{"tnLldpIfPolName":policyName},"children":[]}}
        r = url.post(self.url+'rslacpPol.json', pyld, json=True)
        return r

    def setLACP(self, policyName):
        pyld = {"infraRsLacpPol":{"attributes":{"tnLacpLagPolName":policyName},"children":[]}}
        r = url.post(self.url+'rslacpPol.json', pyld, json=True)
        return r

class infraAccPortP():
    """
    ACI Leaf Interface Profile
    A leaf interface profile is refrenced by a leaf profile to tie to
    physical nodes and holds Port Selector objects to apply policy to
    specific ports.
    """
    rn_url = 'accportprof-{{name}}/'
    portSelectors = {}
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url, name=name)
        self.url = parent.url + self.rn_url
        self._discoverPortSelectors()

    def _discoverPortSelectors(self):
        pars = {
            'query-target':'subtree',
            'target-subtree-class':'infraHPortS'
        }
        t_url = self.url[:-1]+'.json'
        r = url.get(t_url, params=pars)
        print(r.text)

    def createPortSelector(self, name):
        obj = infraHPortS(self, name)
        self.portSelectors.update({name: obj})
        pyld = fetch('cisco/aci/infraHPortS.json', name=name, parent=self)
        t_url = self.url + 'hports-{}-typ-range.json'.format(name)
        r = url.post(t_url, pyld, json=True)
        return obj, r

class infraHPortS():
    """
    ACI Access Port Selector
    A port selector object defines ports in terms of blocks and applies
    an interface policy to the 'selected' ports.
    """
    rn_url = 'hports-{{name}}-typ-range/'
    portBlocks = {}
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url, name=name)
        self.url = parent.url + self.rn_url
        self._discoverPortBlocks()

    def _discoverPortBlocks(self):
        pars = {
            'query-target':'subtree',
            'target-subtree-class':'infraPortBlk'
        }
        t_url = self.url[:-1]+'.json'
        r = url.get(t_url, params=pars)
        imdata = r.json()['imdata']
        for data in imdata:
            prtblk = data['infraPortBlk']['attributes']
            self.portBlocks.update({prtblk['name']:prtblk})
        print(self.portBlocks)

    def setPortBlock(self, id, fromCard, fromPort, toCard=None, toPort=None):
        if not toCard: toCard=fromCard
        if not toPort: toPort=fromPort
        pyld = {
            "infraPortBlk": {
                "attributes": {
                    "dn": "uni/infra/accportprof-{0}/hports-{1}/portblk-{2}".format(self.parent.name, self.name, id),
                    "fromPort": fromPort,
                    "toPort": toPort,
                    "rn": "portblk-"+id
                },
                "children": []
            }
        }
        print(pyld)
        r = url.post(self.url+'rscdpIfPol.json', pyld, json=True)
        return r