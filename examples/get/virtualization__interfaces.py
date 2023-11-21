"""Examples NbApi.virtualization.interfaces.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.virtualization.interfaces.get()

# WEB UI Filter parameters
objects = nb.virtualization.interfaces.get(q=["INTERFACE"])
objects = nb.virtualization.interfaces.get(tag="tag1")
objects = nb.virtualization.interfaces.get(or_tag=["tag1", "tag2"])

# Virtual Machine
objects = nb.virtualization.interfaces.get(cluster=["CLUSTER1", "CLUSTER2"])
objects = nb.virtualization.interfaces.get(cluster_id=[1, 2])
objects = nb.virtualization.interfaces.get(virtual_machine=["VIRTUAL MACHINE1", "VIRTUAL MACHINE2"])
objects = nb.virtualization.interfaces.get(virtual_machine_id=[1, 2])

# Attributes
objects = nb.virtualization.interfaces.get(enabled=True)
objects = nb.virtualization.interfaces.get(mac_address=["000000000001"])
objects = nb.virtualization.interfaces.get(vrf=["VRF1", "VRF2"])
objects = nb.virtualization.interfaces.get(l2vpn=["L2VPN1", "L2VPN2"])

# Data Filter parameters
objects = nb.virtualization.interfaces.get(id=[1, 2])
objects = nb.virtualization.interfaces.get(description=["DESCRIPTION1", "DESCRIPTION2"])
objects = nb.virtualization.interfaces.get(parent=["INTERFACE2"])
objects = nb.virtualization.interfaces.get(parent_id=[1631])
objects = nb.virtualization.interfaces.get(bridge=["INTERFACE2"])
objects = nb.virtualization.interfaces.get(bridge_id=[1631])
