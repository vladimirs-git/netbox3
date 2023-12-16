"""Demo NbApi.dcim.device_roles.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.device_roles.get()

# WEB UI Filter parameters
objects = nb.dcim.device_roles.get(q=["DEVICE ROLE"])
objects = nb.dcim.device_roles.get(tag="tag1")
objects = nb.dcim.device_roles.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.device_roles.get(id=[1, 2])
objects = nb.dcim.device_roles.get(name=["DEVICE ROLE1", "DEVICE ROLE2"])
objects = nb.dcim.device_roles.get(vm_role=True)
objects = nb.dcim.device_roles.get(slug=["device-role1", "device-role2"])
objects = nb.dcim.device_roles.get(description=["DESCRIPTION1", "DESCRIPTION2"])
