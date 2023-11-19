"""Examples NbApi.dcim.regions.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.regions.get()

# WEB UI Filter parameters
objects = nb.dcim.regions.get(q=["REGION"])
objects = nb.dcim.regions.get(tag=["tag1", "tag2"])
objects = nb.dcim.regions.get(parent=["REGION1"])
objects = nb.dcim.regions.get(parent_id=[1, 2])

# not working
# objects = nb.dcim.regions.get(contact=["CONTACT1"])
# objects = nb.dcim.regions.get(contact_id=[1])
# objects = nb.dcim.regions.get(contact_role=["CONTACT1"])
# objects = nb.dcim.regions.get(contact_role_id=[1])
# objects = nb.dcim.regions.get(contact_group=["CONTACT ROLE1"])
# objects = nb.dcim.regions.get(contact_group_id=[1])

# Data Filter parameters
objects = nb.dcim.regions.get(id=[1, 2])
objects = nb.dcim.regions.get(name=["REGION1", "REGION2"])
objects = nb.dcim.regions.get(slug=["region1", "region2"])
objects = nb.dcim.regions.get(description=["DESCRIPTION1", "DESCRIPTION2"])
