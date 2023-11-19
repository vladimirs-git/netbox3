"""Examples NbApi.dcim.sites.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.sites.get()

# WEB UI Filter parameters
objects = nb.dcim.sites.get(q=["SITE"])
objects = nb.dcim.sites.get(tag=["tag1", "tag2"])
objects = nb.dcim.sites.get(status=["active", "planned"])
objects = nb.dcim.sites.get(region=["REGION1", "REGION2"])
objects = nb.dcim.sites.get(region_id=[1, 2])
objects = nb.dcim.sites.get(group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.dcim.sites.get(group_id=[1, 2])
objects = nb.dcim.sites.get(asn=[65101, 65102])
objects = nb.dcim.sites.get(asn_id=[1, 2])
objects = nb.dcim.sites.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.dcim.sites.get(tenant_group_id=[1, 2])
objects = nb.dcim.sites.get(tenant=["TENANT1", "TENANT2"])
objects = nb.dcim.sites.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.dcim.sites.get(id=[1, 2])
objects = nb.dcim.sites.get(name=["SITE1", "SITE2"])
objects = nb.dcim.sites.get(slug=["site1", "site2"])
objects = nb.dcim.sites.get(description=["DESCRIPTION1", "DESCRIPTION2"])
