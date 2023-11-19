"""Examples NbApi.ipam.prefixes.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.prefixes.get()

# WEB UI Filter parameters
objects = nb.ipam.prefixes.get(q=["10.1.1", "10.2.2"])
objects = nb.ipam.prefixes.get(tag=["tag1", "tag2"])
objects = nb.ipam.prefixes.get(family=[4, 6])
objects = nb.ipam.prefixes.get(status=["active"])
objects = nb.ipam.prefixes.get(role=["ROLE1", "ROLE2"])
objects = nb.ipam.prefixes.get(role_id=[1, 2])
objects = nb.ipam.prefixes.get(mask_length=[24, 28])
objects = nb.ipam.prefixes.get(is_pool=True)
objects = nb.ipam.prefixes.get(mark_utilized=True)
objects = nb.ipam.prefixes.get(vrf=["null"])
objects = nb.ipam.prefixes.get(vrf=["VRF1", "VRF2"])
objects = nb.ipam.prefixes.get(vrf_id=[1, 2])
objects = nb.ipam.prefixes.get(present_in_vrf=["VRF1", "VRF2"])
objects = nb.ipam.prefixes.get(present_in_vrf_id=[1, 2])
objects = nb.ipam.prefixes.get(region=["REGION1", "REGION2"])
objects = nb.ipam.prefixes.get(region_id=[1, 2])
objects = nb.ipam.prefixes.get(site_group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.ipam.prefixes.get(site_group_id=[1, 2])
objects = nb.ipam.prefixes.get(site=["SITE1", "SITE2"])
objects = nb.ipam.prefixes.get(site_id=[1, 2])
objects = nb.ipam.prefixes.get(tenant_group=["TENANT GROUP1"])
objects = nb.ipam.prefixes.get(tenant_group_id=[1])
objects = nb.ipam.prefixes.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.prefixes.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.prefixes.get(id=[1, 2])
objects = nb.ipam.prefixes.get(prefix=["10.1.1.0/24", "10.2.2.0/28"])
objects = nb.ipam.prefixes.get(description=["DESCRIPTION1", "DESCRIPTION2"])
objects = nb.ipam.prefixes.get(created=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
objects = nb.ipam.prefixes.get(last_updated=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
