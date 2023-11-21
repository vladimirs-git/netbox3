"""Examples NbApi.dcim.manufacturers.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.manufacturers.get()

# WEB UI Filter parameters
objects = nb.dcim.manufacturers.get(q=["MANUFACTURER"])
objects = nb.dcim.manufacturers.get(tag="tag1")
objects = nb.dcim.manufacturers.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.dcim.manufacturers.get(id=[1, 2])
objects = nb.dcim.manufacturers.get(name=["MANUFACTURER1", "MANUFACTURER2"])
objects = nb.dcim.manufacturers.get(slug=["manufacturer1", "manufacturer2"])
objects = nb.dcim.manufacturers.get(description=["DESCRIPTION1", "DESCRIPTION2"])
