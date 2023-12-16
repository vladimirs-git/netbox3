"""Demo NbApi.dcim.sites.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.sites.get()

# WEB UI Filter parameters
objects = nb.dcim.sites.get(q=["SITE"])
objects = nb.dcim.sites.get(tag="tag1")
objects = nb.dcim.sites.get(or_tag=["tag1", "tag2"])

# Attributes
objects = nb.dcim.sites.get(status=["active", "planned"])
objects = nb.dcim.sites.get(region=["REGION1", "REGION2"])
objects = nb.dcim.sites.get(region_id=[1, 2])
objects = nb.dcim.sites.get(group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.dcim.sites.get(group_id=[1, 2])
objects = nb.dcim.sites.get(asn=[65101, 65102])
objects = nb.dcim.sites.get(asn_id=[1, 2])

# Tenant
objects = nb.dcim.sites.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.dcim.sites.get(tenant_group_id=[1, 2])
objects = nb.dcim.sites.get(tenant=["TENANT1", "TENANT2"])
objects = nb.dcim.sites.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.dcim.sites.get(id=[1, 2])
objects = nb.dcim.sites.get(name=["SITE1", "SITE2"])
objects = nb.dcim.sites.get(slug=["site1", "site2"])
objects = nb.dcim.sites.get(description=["DESCRIPTION1", "DESCRIPTION2"])
