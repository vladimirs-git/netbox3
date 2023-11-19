"""Examples NbApi.dcim.rack_roles.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.rack_roles.get()

# WEB UI Filter parameters
objects = nb.dcim.rack_roles.get(q=["RACK ROLE"])
objects = nb.dcim.rack_roles.get(tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.rack_roles.get(id=[1, 2])
objects = nb.dcim.rack_roles.get(name=["RACK ROLE1", "RACK ROLE2"])
objects = nb.dcim.rack_roles.get(slug=["rack-role1", "rack-role2"])
objects = nb.dcim.rack_roles.get(description=["DESCRIPTION1", "DESCRIPTION2"])
