"""Examples NbApi.dcim.device_types.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.device_types.get()

# WEB UI Filter parameters
objects = nb.dcim.device_types.get(q=["DEVICE TYPE"])
objects = nb.dcim.device_types.get(tag="tag1")
objects = nb.dcim.device_types.get(or_tag=["tag1", "tag2"])

# Hardware
objects = nb.dcim.device_types.get(manufacturer=["MANUFACTURER1", "MANUFACTURER2"])
objects = nb.dcim.device_types.get(manufacturer_id=[1, 2])
objects = nb.dcim.device_types.get(part_number=["PART NUMBER1", "PART NUMBER2"])

# Data Filter parameters
objects = nb.dcim.device_types.get(id=[1, 2])
objects = nb.dcim.device_types.get(name=["DEVICE TYPE1", "DEVICE TYPE2"])
objects = nb.dcim.device_types.get(slug=["device-type1", "device-type2"])
objects = nb.dcim.device_types.get(description=["DESCRIPTION1", "DESCRIPTION2"])
