"""Examples NbApi.dcim.devices.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.devices.get()

# WEB UI Filter parameters
objects = nb.dcim.devices.get(q=["DEVICE"])
objects = nb.dcim.devices.get(tag="tag1")
objects = nb.dcim.devices.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.devices.get(id=[1, 2])
objects = nb.dcim.devices.get(name=["DEVICE1", "DEVICE2"])
objects = nb.dcim.devices.get(description=["DESCRIPTION1", "DESCRIPTION2"])
