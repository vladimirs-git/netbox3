"""Examples NbApi.dcim.device_roles.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.device_roles.get()

# WEB UI Filter parameters
objects = nb.dcim.device_roles.get(q=["DEVICE ROLE"])
objects = nb.dcim.device_roles.get(tag=["tag1", "tag2"])
objects = nb.dcim.device_roles.get(vm_role=True)

# Data Filter parameters
objects = nb.dcim.device_roles.get(id=[1, 2])
objects = nb.dcim.device_roles.get(name=["DEVICE ROLE1", "DEVICE ROLE2"])
objects = nb.dcim.device_roles.get(slug=["device-role1", "device-role2"])
objects = nb.dcim.device_roles.get(description=["DESCRIPTION1", "DESCRIPTION2"])
