"""Examples NbApi.extras.content_types.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.extras.content_types.get()

# WEB UI Filter parameters

# Data Filter parameters
objects = nb.extras.content_types.get(q=["admin", "auth"])

objects1 = nb.extras.content_types.get(id=1)
objects2 = nb.extras.content_types.get(id=2)
objects = nb.extras.content_types.get(id=[1, 2])

objects1 = nb.extras.content_types.get(app_label="dcim")
objects2 = nb.extras.content_types.get(app_label="ipam")
objects = nb.extras.content_types.get(app_label=["dcim", "ipam"])

objects1 = nb.extras.content_types.get(model="aggregate")
objects2 = nb.extras.content_types.get(model="site")
objects = nb.extras.content_types.get(model=["aggregate", "site"])
x = 1
