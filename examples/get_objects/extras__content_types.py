"""Examples NbApi.extras.content_types.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.extras.content_types.get()

# WEB UI Filter parameters

# Data Filter parameters
objects = nb.extras.content_types.get(q=["admin", "auth"])
objects = nb.extras.content_types.get(id=[1, 2])
objects = nb.extras.content_types.get(app_label=["dcim", "ipam"])
objects = nb.extras.content_types.get(model=["aggregate", "site"])
