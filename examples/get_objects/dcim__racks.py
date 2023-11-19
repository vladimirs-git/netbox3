"""Examples NbApi.dcim.racks.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.racks.get()

# WEB UI Filter parameters
objects = nb.dcim.racks.get(q=["RACK"])
objects = nb.dcim.racks.get(tag=["tag1", "tag2"])
objects = nb.dcim.racks.get(status=["planned"])
objects = nb.dcim.racks.get(region=["REGION1", "REGION2"])
objects = nb.dcim.racks.get(region_id=[1, 2])
objects = nb.dcim.racks.get(site_group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.dcim.racks.get(site_group_id=[1, 2])
objects = nb.dcim.racks.get(site=["SITE1", "SITE2"])
objects = nb.dcim.racks.get(site_id=[1, 2])
objects = nb.dcim.racks.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.dcim.racks.get(tenant_group_id=[1, 2])
objects = nb.dcim.racks.get(tenant=["TENANT1", "TENANT2"])
objects = nb.dcim.racks.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.dcim.racks.get(id=[1, 2])
objects = nb.dcim.racks.get(name=["RACK1", "RACK2"])
objects = nb.dcim.racks.get(description=["DESCRIPTION1", "DESCRIPTION2"])
