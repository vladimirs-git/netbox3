"""Examples NbForager.grow_tree() all objects."""
import logging
from datetime import datetime

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get all object from Netbox.
start = datetime.now()
nbf.get()
seconds = (datetime.now() - start).seconds

nbf.grow_tree()
print(f"{seconds=}")
print(f"NbForager.tree devices={len(nbf.tree.dcim.devices)} objects={nbf.tree.count()}")
# seconds=41
# NbForager.tree devices=67 objects=2371
