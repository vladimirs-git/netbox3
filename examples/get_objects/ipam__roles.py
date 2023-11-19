"""Examples NbApi.ipam.roles.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.roles.get()

# WEB UI Filter parameters
objects = nb.ipam.roles.get(q=["ROLE"])
objects = nb.ipam.roles.get(tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.ipam.roles.get(id=[1, 2])
objects = nb.ipam.roles.get(name=["ROLE1", "ROLE2"])
objects = nb.ipam.roles.get(slug=["role1", "role2"])
objects = nb.ipam.roles.get(description="DESCRIPTION1")
objects = nb.ipam.roles.get(created=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
objects = nb.ipam.roles.get(last_updated=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
