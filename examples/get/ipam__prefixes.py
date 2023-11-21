"""Examples NbApi.ipam.prefixes.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.prefixes.get()

# WEB UI Filter parameters
objects = nb.ipam.prefixes.get(q=["10.1.1", "10.2.2"])
objects = nb.ipam.prefixes.get(tag="tag1")
objects = nb.ipam.prefixes.get(or_tag=["tag1", "tag2"])

# Addressing
objects1 = nb.ipam.prefixes.get(within_include="10.0.0.0/20")
objects2 = nb.ipam.prefixes.get(within_include="10.11.0.0/16")
objects = nb.ipam.prefixes.get(within_include=["10.0.0.0/20", "10.11.0.0/16"])
objects = nb.ipam.prefixes.get(family=[4, 6])
objects = nb.ipam.prefixes.get(status=["active"])
objects = nb.ipam.prefixes.get(role=["ROLE1", "ROLE2"])
objects = nb.ipam.prefixes.get(role_id=[1, 2])
objects = nb.ipam.prefixes.get(mask_length=[24, 28])
objects = nb.ipam.prefixes.get(is_pool=True)
objects = nb.ipam.prefixes.get(mark_utilized=True)

# VRF
objects = nb.ipam.prefixes.get(vrf=["null"])
objects = nb.ipam.prefixes.get(vrf=["VRF1", "VRF2"])
objects = nb.ipam.prefixes.get(vrf_id=[1, 2])
objects = nb.ipam.prefixes.get(present_in_vrf=["VRF1", "VRF2"])
objects = nb.ipam.prefixes.get(present_in_vrf_id=[1, 2])

# Location
objects = nb.ipam.prefixes.get(region=["REGION1", "REGION2"])
objects = nb.ipam.prefixes.get(region_id=[1, 2])
objects = nb.ipam.prefixes.get(site_group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.ipam.prefixes.get(site_group_id=[1, 2])
objects = nb.ipam.prefixes.get(site=["SITE1", "SITE2"])
objects = nb.ipam.prefixes.get(site_id=[1, 2])

# Tenant
objects = nb.ipam.prefixes.get(tenant_group=["TENANT GROUP1"])
objects = nb.ipam.prefixes.get(tenant_group_id=[1])
objects = nb.ipam.prefixes.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.prefixes.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.prefixes.get(id=[1, 2])
objects = nb.ipam.prefixes.get(prefix=["10.1.1.0/24", "10.2.2.0/28"])
objects = nb.ipam.prefixes.get(description=["DESCRIPTION1", "DESCRIPTION2"])
