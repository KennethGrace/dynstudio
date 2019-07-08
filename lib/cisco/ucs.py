# This python module expands on the host abstract class
# CiscoUCS adds objects and methods for intent operation against a CiscoUCS Fabric
#

from dynstudio.host import abstractHost

from ucsmsdk.ucshandle import UcsHandle

#Create a null UCS Handler Object
handler = UcsHandle('null','null','null')

class Host(abstractHost):
    def __init__(self, name):
        super().__init__(name)

    def connect(self, user, password):
        handler = UcsHandle(self.name, user, password)
        handler.login()
        self.difLAN()

    def difLAN(self):
        self.lan = Lan(self)

    def commit(self):
        handler.commit()

    def disconnect(self):
        handler.logout()

class Lan():
    vlanGroups = {}
    vlans = {}
    def __init__(self, host, mo=None):
        self.host = host
        if not mo:
            self.mo = handler.query_dn('fabric/lan')
        self._discoverFabric()

    def _discoverFabric(self):
        # Query the Fabric/Lan Tree for all child objects
        objs = handler.query_dn(self.mo.dn, hierarchy=True)
        # Parse the Fabric/Lan Tree into native objects
        for obj in objs:
            if obj._class_id == 'FabricVlan':
                self.vlans.update({obj.name: Vlan(self, obj.name, mo=obj)})
            elif obj._class_id == 'FabricNetGroup':
                self.vlanGroups.update({obj.name: VlanGroup(self, obj.name, mo=obj)})

    def createVlan(self, name, id):
        """ Difine and create a new VLAN on the UCS fabric
        """
        from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
        mo = FabricVlan(parent_mo_or_dn=self.mo,name=name,id=id)
        handler.add_mo(mo, modify_present=True)
        self.vlans.update({name: Vlan(self, name, mo=mo)})
        return mo

    def removeVlansByID(self, id):
        for vlan in self.vlans.values():
            if vlan.mo.id == id:
                handler.remove_mo(vlan.mo)
                del self.vlans[vlan.name]

    def removeVlan(self, name):
        """ Strip the UCS Fabric of the vlan instance which matches passed name
        """
        t_vlan = self.vlans[name]
        handler.remove_mo(t_vlan.mo)
        del self.vlans[name]

class VlanGroup():
    groupVlans = []
    def __init__(self, lan, name, mo=None):
        self.lan = lan
        self.name = name
        self.mo = mo
        if not mo:
            self.mo = handler.query_dn('fabric/lan/net-group-{}'.format(name))
        # Init Vlans List
        self.groupVlans = handler.query_dn(self.mo.dn, hierarchy=True)

    def removeVlansByID(self, id):
        """ Strips the Vlan Group of all instances of the passed Vlan ID
        """
        for vlan in self.lan.vlans.values():
            if vlan.mo.id == id:
                for groupVlan in self.groupVlans:
                    if groupVlan.name == vlan.mo.name:
                        handler.remove_mo(groupVlan)

    def removeVlan(self, name):
        if name in self.lan.vlans.keys():
            t_vlan = self.lan.vlans[name]
            for groupVlan in self.groupVlans:
                if groupVlan.name == t_vlan.mo.name:
                    handler.remove_mo(groupVlan)

    def addVlansByID(self, id):
        """ Appends the Vlan Group with all instances of the passed Vlan ID
        """
        from ucsmsdk.mometa.fabric.FabricPooledVlan import FabricPooledVlan
        for vlan in self.lan.vlans.values():
            if vlan.mo.id == id:
                tmp = FabricPooledVlan(parent_mo_or_dn=self.mo, name=vlan.name)
                handler.add_mo(tmp, modify_present=True)

    def addVlan(self, name):
        from ucsmsdk.mometa.fabric.FabricPooledVlan import FabricPooledVlan
        if name in self.lan.vlans.keys():
            tmp = FabricPooledVlan(parent_mo_or_dn=self.mo, name=name)
            handler.add_mo(tmp, modify_present=True)

class Vlan():
    groups = {}
    def __init__(self, lan, name, mo=None):
        self.name = name
        self.lan = lan
        self.mo = mo
        if not mo:
            self.mo = handler.query_dn('fabric/lan/net-{}'.format(name))
