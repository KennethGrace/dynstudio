from dynstudio.util import url
from dynstudio.util.rscmanager import fetch, render, grab




#########################
###                   ###
###  Special Objects  ###
###                   ###
#########################

class infraAccBndlGrp():
    """
    ACI PC/vPC Interface Policy
    Used to define a port group which connects down from two leaves to legacy switch hardware
    """
    children = []
    rn_url = 'accbundle-{{name}}/'
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.rn_url = render(self.rn_url, name=name)
        self.url = parent.url + self.rn_url
        self.children = grab('cisco/aci/infraAccBndlGrp.json')['infraAccBndlGrp']['children']

    def setVPC(self, vpc):
        lagT = 'link'
        if vpc:
            lagT = 'node'
        pyld = {"infraAccBndlGrp":{"attributes":{"dn":"uni/infra/funcprof/accbundle-"+self.name,"lagT":lagT},"children":[]}}
        r = url.post(self.url[:-1]+'.json', pyld, json=True)
        return r

    def setAEP(self, profileName):
        pass

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

class fabricHIfPol():
    def __init__(self, parent, name):
        pass