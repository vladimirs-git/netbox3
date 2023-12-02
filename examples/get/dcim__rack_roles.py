"""Examples NbApi.dcim.rack_roles.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.rack_roles.get()

# WEB UI Filter parameters
objects = nb.dcim.rack_roles.get(q=["RACK ROLE"])
objects = nb.dcim.rack_roles.get(tag="tag1")
objects = nb.dcim.rack_roles.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.rack_roles.get(id=[1, 2])
objects = nb.dcim.rack_roles.get(name=["RACK ROLE1", "RACK ROLE2"])
objects = nb.dcim.rack_roles.get(slug=["rack-role1", "rack-role2"])
objects = nb.dcim.rack_roles.get(description=["DESCRIPTION1", "DESCRIPTION2"])
