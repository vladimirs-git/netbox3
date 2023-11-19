"""Examples NbApi.ipam.asns.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.asns.get()

# WEB UI Filter parameters
objects = nb.ipam.asns.get(q=["65001", "65002"])
objects = nb.ipam.asns.get(tag=["tag1", "tag2"])
objects = nb.ipam.asns.get(rir=["ARIN", "RFC 6996"])
objects = nb.ipam.asns.get(rir_id=[1, 2])
objects = nb.ipam.asns.get(site=["SITE1", "SITE2"])
objects = nb.ipam.asns.get(site_id=[1, 2])
objects = nb.ipam.asns.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.ipam.asns.get(tenant_group_id=[1, 2])
objects = nb.ipam.asns.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.asns.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.asns.get(id=[1, 2])
objects = nb.ipam.asns.get(asn=[65001, 65002])
