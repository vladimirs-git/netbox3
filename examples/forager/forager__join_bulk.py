"""Examples NbForager.grow_tree() bulk of objects."""
import logging
from datetime import datetime

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get the objects from Netbox using nested mode to requests all related objects.
start = datetime.now()
nbf.dcim.devices.get(nested=True)
nbf.ipam.aggregates.get(nested=True)
nbf.ipam.prefixes.get(nested=True)
nbf.ipam.ip_addresses.get(nested=True)
nbf.circuits.circuits.get(nested=True)
nbf.circuits.circuit_terminations.get(nested=True)
seconds = (datetime.now() - start).seconds
print(f"{seconds=}")
print(f"NbForager.root devices={len(nbf.root.dcim.devices)} objects={nbf.root.count()}")
nbf.grow_tree()
print(f"NbForager.tree devices={len(nbf.tree.dcim.devices)} objects={nbf.tree.count()}")
