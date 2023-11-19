"""Examples NbApi.ipam.rirs.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.rirs.get()

# WEB UI Filter parameters
objects = nb.ipam.rirs.get(q=["RFC"])
objects = nb.ipam.rirs.get(is_private=True)
objects = nb.ipam.rirs.get(tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.ipam.rirs.get(id=[1, 2])
objects = nb.ipam.rirs.get(name=["ARIN", "RFC 1918"])
objects = nb.ipam.rirs.get(slug=["arin", "rfc-1918"])
objects = nb.ipam.rirs.get(description="text")
objects = nb.ipam.rirs.get(created=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
objects = nb.ipam.rirs.get(last_updated=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
