from __future__ import unicode_literals
from dynstudio.host import Host

from dynstudio.lib.cisco.aci.apic import Host as APIC
from dynstudio.lib.cisco.ucs import Host as UCSM
from dynstudio.lib.cisco.catalyst.ios import Host as IOS

__version__ = "0.0.2"
__all__ = ("Host", "APIC", "UCSM", "CISCO_IOS")