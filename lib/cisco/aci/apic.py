import builtins

from dynstudio.util import url
from dynstudio.util.rscmanager import fetch, render

from dynstudio.host import abstractHost

from dynstudio.lib.cisco.aci import tenant
from dynstudio.lib.cisco.aci import switching


import json

class Host(abstractHost):
    """
    The Host Object for DynStudio ACI Implementation.
    Ties to a real Cisco Application Policy Infastructure Controller (APIC).
    Attributes and methods of this class relate to changes in the
    Management Plane of the APIC.
    """
    url = 'https://{0}/api/'
    tenants = {}
    def __init__(self, name):
        self.name = name
        self.url = render(self.url,name=name)
        print(self.url)
        self.fabric = switching.Fabric(self)

    def connect(self, user, pswd):
        """
        Launch a login request to recieve a token for future use.
        Store token in a requests cookie jar object in url module.
        """
        #TODO: Implement Requests Testing of the user/pswd combo before running discovery
        obj = fetch('cisco/aci/aaaLogin.json', username=user, password=pswd)
        r = url.post(self.url+'aaaLogin.json', obj, json=True)
        auth_token = r.json()['imdata'][0]['aaaLogin']['attributes']['token']
        url.jar.set('APIC-Cookie',auth_token)
        self._discoverTenants()

    def _discoverTenants(self):
        # Request the list of all Tenant objects
        t_url = self.url+'node/class/fvTenant.json'
        r = url.get(t_url)
        for tenant_cls in r.json()['imdata']:
            name = tenant_cls['fvTenant']['attributes']['name']
            if name != 'common':
                self.tenants.update({name: tenant.fvTenant(self, name)})
            else:
                self.tenants.update({name: tenant.cmnFvTenant(self, name)})

    def disconnect(self):
        pass