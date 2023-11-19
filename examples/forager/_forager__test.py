"""Examples NbForager.grow_tree() all objects."""
import logging
from datetime import datetime

from netbox3 import NbForager

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get all object from Netbox.
start = datetime.now()
nbf.circuits.get(include_nested=False)
nbf.core.get(include_nested=False)
nbf.dcim.get(include_nested=False)
nbf.extras.get(include_nested=False)
nbf.ipam.get(include_nested=False)
nbf.tenancy.get(include_nested=False)
nbf.users.get(include_nested=False)
nbf.virtualization.get(include_nested=False)
nbf.wireless.get(include_nested=False)
seconds = (datetime.now() - start).seconds

nbf.grow_tree()
print(f"{seconds=}")
print(f"NbForager.tree devices={len(nbf.tree.dcim.devices)} objects={nbf.tree.count()}")
# seconds=41
# NbForager.tree devices=67 objects=2371
