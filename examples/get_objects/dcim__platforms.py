"""Examples NbApi.dcim.platforms.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.platforms.get()

# WEB UI Filter parameters
objects = nb.dcim.platforms.get(q=["PLATFORM"])
objects = nb.dcim.platforms.get(tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.platforms.get(id=[1, 2])
objects = nb.dcim.platforms.get(name=["PLATFORM1", "PLATFORM2"])
objects = nb.dcim.platforms.get(slug=["platform1", "platform2"])
objects = nb.dcim.platforms.get(description=["DESCRIPTION1", "DESCRIPTION2"])
