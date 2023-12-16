"""Demo NbApi.dcim.console_ports.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.console_ports.get()

# WEB UI Filter parameters
objects = nb.dcim.console_ports.get(q=["CONSOLE PORT"])
objects = nb.dcim.console_ports.get(tag="tag1")
objects = nb.dcim.console_ports.get(or_tag=["tag1", "tag2"])

# Attributes
# Name
# Label
# Type
# Speed

# Location
# Region
# Site group
# Site
# Location
# Rack

# Device
# Device type
# Device role
# Device
# Virtual Chassis

# Cable
# Cabled
# Occupied

# Data Filter parameters
objects = nb.dcim.console_ports.get(id=[1, 2])
objects = nb.dcim.console_ports.get(name=["CONSOLE PORT1", "CONSOLE PORT2"])
objects = nb.dcim.console_ports.get(description=["DESCRIPTION1", "DESCRIPTION2"])
