"""Examples NbApi.dcim.platforms.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.platforms.get()

# WEB UI Filter parameters
objects = nb.dcim.platforms.get(q=["PLATFORM"])
objects = nb.dcim.platforms.get(tag="tag1")
objects = nb.dcim.platforms.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.platforms.get(id=[1, 2])
objects = nb.dcim.platforms.get(name=["PLATFORM1", "PLATFORM2"])
objects = nb.dcim.platforms.get(slug=["platform1", "platform2"])
objects = nb.dcim.platforms.get(description=["DESCRIPTION1", "DESCRIPTION2"])
