"""Examples, How to create ... 

TODO DELETE

- NbForager.tree.dcim.devices
"""
import logging

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get the objects from Netbox
nbf.dcim.devices.get(name=["DEVICE1", "DEVICE2"])
nbf.dcim.interfaces.get(name="GigabitEthernet1/0/2", device=["DEVICE1", "DEVICE2"])
nbf.dcim.cables.get(id=[129])
nbf.circuits.circuits.get(cid=["CID1"])
nbf.circuits.circuit_terminations.get(id=[57])
nbf.write_cache()
nbf.read_cache()
nbf.grow_tree()

x = 1
