"""Examples NbApi.dcim.site_groups.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.site_groups.get()

# WEB UI Filter parameters
objects = nb.dcim.site_groups.get(q=["GROUP"])
objects = nb.dcim.site_groups.get(tag="tag1")
objects = nb.dcim.site_groups.get(or_tag=["tag1", "tag2"])
objects = nb.dcim.site_groups.get(parent=["SITE GROUP1"])
objects = nb.dcim.site_groups.get(parent_id=[8])

# Data Filter parameters
objects = nb.dcim.site_groups.get(id=[1, 2])
objects = nb.dcim.site_groups.get(name=["SITE GROUP1", "SITE GROUP2"])
objects = nb.dcim.site_groups.get(slug=["site-group1", "site-group2"])
objects = nb.dcim.site_groups.get(description=["DESCRIPTION1", "DESCRIPTION2"])
