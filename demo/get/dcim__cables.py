"""Demo NbApi.dcim.cables.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.cables.get()

# WEB UI Filter parameters

# Data Filter parameters
objects = nb.dcim.cables.get(id=[21, 22])
objects = nb.dcim.cables.get(display=["#21", "#22"])
