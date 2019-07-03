from dynstudio.host import abstractHost
from dynstudio.rscmanager import fetch, render

import json
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'Content-Type': 'application/json'}
jar = requests.cookies.RequestsCookieJar()

class Host(abstractHost):
    """
    ACI Virtual Routing and Forwarding Object
    """
    url = r'https://{{name}}/api/'
    tenants = {}
    def __init__(self, name):
        self.name = name
        self.url = render(self.url,name=name)
        print(self.url)

    def connect(self, user, pswd):
        """
        Launch a login request to recieve a token for future use.
        Store token in a requests cookie jar object.
        """
        #TODO: Implement Requests Testing of the user/pswd combo before running discovery
        obj = fetch('cisco/apic/aaaLogin.json', username=user, password=pswd)
        r = requests.post(self.url+'aaaLogin.json', json=obj, headers=headers, verify=False)
        auth_token = r.json()['imdata'][0]['aaaLogin']['attributes']['token']
        jar.set('APIC-Cookie',auth_token)
        self._discoverTenants()

    def _discoverTenants(self):
        # Request the list of all Tenant objects
        url = self.url+'node/class/fvTenant.json'
        r = requests.get(url, headers=headers, verify=False, cookies=jar)
        for tenant in r.json()['imdata']:
            print(tenant)
            name = tenant['fvTenant']['attributes']['name']
            print(name)
            self.tenants.update({name: fvTenant(self, name)})

    def disconnect(self):
        pass

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
        r = requests.post(t_url, headers=headers, json=obj, verify=False, cookies=jar)
        print(json.dumps(r.json(), indent=2))
        new_l3extOut = l3extOut(self, name)
        self.l3extOuts.update({name: new_l3extOut})
        return new_l3extOut

    def createVRF(self, name):
        obj = fetch('cisco/apic/fvCtx.json', tenant=self, name=name)
        t_url = self.url+'ctx-{}.json'.format(name)
        r = requests.post(t_url, headers=headers, json=obj, verify=False, cookies=jar)
        print(json.dumps(r.json(), indent=2))
        new_fvCtx = fvCtx(self, name)
        self.fvCtxs.update({name: new_fvCtx})
        return new_fvCtx

    def createOSPF(self, name):
        obj = fetch('cisco/apic/ospfIfPol.json', tenant=self, name=name)
        t_url = self.url+'ospfIfPol-{}.json'.format(name)
        r = requests.post(t_url, headers=headers, json=obj, verify=False, cookies=jar)
        print(json.dumps(r.json(), indent=2))
        new_ospfIfPol = ospfIfPol(self, name)
        self.ospfIfPols.update({name: new_ospfIfPol})
        return new_ospfIfPol

class l3extOut():
    """
    ACI Layer 3 Exstention Out
    """
    rn_url = r'out-{{name}}/'
    def __init__(self, tenant, name):
        self.name = name
        self.tenant = tenant
        self.rn_url = render(self.rn_url,name=name)
        self.url = tenant.url + self.rn_url
        pass

class fvCtx():
    """
    ACI Virtual Routing and Forwarding Object
    """
    rn_url = r'ctx-{{name}}/'
    def __init__(self, tenant, name):
        self.name = name
        self.tenant = tenant
        self.rn_url = render(self.rn_url,name=name)
        self.url = tenant.url + self.rn_url

class ospfIfPol():
    """
    ACI OSPF Interface Policy
    """
    rn_url = r'ospfIfPol-{{name}}/'
    def __init__(self, tenant, name):
        self.name = name
        self.tenant = tenant
        self.rn_url = render(self.rn_url,name=name)
        self.url = tenant.url + self.rn_url
