"""Examples NbForager.grow_tree() bulk of objects."""
import logging
from datetime import datetime

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get the objects from Netbox using nested mode to requests all related objects.
start = datetime.now()
nbf.dcim.devices.get(include_nested=True)
nbf.ipam.aggregates.get(include_nested=True)
nbf.ipam.prefixes.get(include_nested=True)
nbf.ipam.ip_addresses.get(include_nested=True)
nbf.circuits.circuits.get(include_nested=True)
nbf.circuits.circuit_terminations.get(include_nested=True)
seconds = (datetime.now() - start).seconds
print(f"{seconds=}")
print(f"NbForager.root devices={len(nbf.root.dcim.devices)} objects={nbf.root.count()}")
nbf.grow_tree()
print(f"NbForager.tree devices={len(nbf.tree.dcim.devices)} objects={nbf.tree.count()}")
