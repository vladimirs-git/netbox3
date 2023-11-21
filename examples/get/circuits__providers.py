"""Examples NbApi.circuits.providers.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.providers.get()

# WEB UI Filter parameters
objects = nb.circuits.providers.get(q=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.providers.get(tag="tag1")
objects = nb.circuits.providers.get(or_tag=["tag1", "tag2"])

# Location
objects = nb.circuits.providers.get(region=["USA", "EU"])
objects = nb.circuits.providers.get(region_id=[1, 2])
objects = nb.circuits.providers.get(site_group=["GROUP1", "GROUP2"])
objects = nb.circuits.providers.get(site_group_id=[1, 2])
objects = nb.circuits.providers.get(site=["SITE1", "SITE2"])
objects = nb.circuits.providers.get(site_id=[1, 2])

# Data Filter parameters
objects = nb.circuits.providers.get(id=[1, 2])
objects = nb.circuits.providers.get(name=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.providers.get(slug=["provider1", "provider2"])
objects = nb.circuits.providers.get(description=["DESCRIPTION1", "DESCRIPTION2"])
