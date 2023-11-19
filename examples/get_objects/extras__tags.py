"""Examples NbApi.extras.tags.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.extras.tags.get()

# WEB UI Filter parameters
objects = nb.extras.tags.get(q=["TAG"])
objects = nb.extras.tags.get(content_type=["circuits | circuit type", "circuits | provider"])
objects = nb.extras.tags.get(content_type_id=[22, 23])  # 22=circuits.circuittype
objects = nb.extras.tags.get(for_object_type=["circuits | circuit type", "circuits | provider"])
objects = nb.extras.tags.get(for_object_type_id=[22, 23])  # 23=circuits.provider

# Data Filter parameters
objects = nb.extras.tags.get(id=[1, 2])
objects = nb.extras.tags.get(name=["TAG1", "TAG2"])
objects = nb.extras.tags.get(slug=["tag1", "tag2"])
