"""Examples NbApi.dcim.device_types.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.device_types.get()

# WEB UI Filter parameters
objects = nb.dcim.device_types.get(q=["DEVICE TYPE"])
objects = nb.dcim.device_types.get(tag=["tag1", "tag2"])
objects = nb.dcim.device_types.get(manufacturer=["MANUFACTURER1", "MANUFACTURER2"])
objects = nb.dcim.device_types.get(manufacturer_id=[1, 2])
objects = nb.dcim.device_types.get(part_number=["PART NUMBER1", "PART NUMBER2"])

# Data Filter parameters
objects = nb.dcim.device_types.get(id=[1, 2])
objects = nb.dcim.device_types.get(name=["DEVICE TYPE1", "DEVICE TYPE2"])
objects = nb.dcim.device_types.get(slug=["device-type1", "device-type2"])
objects = nb.dcim.device_types.get(description=["DESCRIPTION1", "DESCRIPTION2"])
