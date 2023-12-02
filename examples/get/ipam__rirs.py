"""Examples NbApi.ipam.rirs.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.rirs.get()

# WEB UI Filter parameters
objects = nb.ipam.rirs.get(q=["RFC"])
objects = nb.ipam.rirs.get(is_private=True)
objects = nb.ipam.rirs.get(tag="tag1")
objects = nb.ipam.rirs.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.ipam.rirs.get(id=[1, 2])
objects = nb.ipam.rirs.get(name=["ARIN", "RFC 1918"])
objects = nb.ipam.rirs.get(slug=["arin", "rfc-1918"])
objects = nb.ipam.rirs.get(description="DESCRIPTION1")
