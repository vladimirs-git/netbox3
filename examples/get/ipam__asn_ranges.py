"""Examples NbApi.ipam.asn_ranges.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.asn_ranges.get()

# WEB UI Filter parameters
objects = nb.ipam.asn_ranges.get(q=["ASN"])  # not working
objects = nb.ipam.asn_ranges.get(tag="tag1")
objects = nb.ipam.asn_ranges.get(or_tag=["tag1", "tag2"])

# Range
objects = nb.ipam.asn_ranges.get(rir=["ARIN", "RFC 6598"])  # not working
objects = nb.ipam.asn_ranges.get(rir_id=[1, 2])
objects = nb.ipam.asn_ranges.get(start=[65001])
objects = nb.ipam.asn_ranges.get(end=[65003])

# Tenant
objects = nb.ipam.asn_ranges.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.ipam.asn_ranges.get(tenant_group_id=[1, 2])
objects = nb.ipam.asn_ranges.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.asn_ranges.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.asn_ranges.get(id=[1, 2])
objects = nb.ipam.asn_ranges.get(name=["ANS_RANGES1"])
objects = nb.ipam.asn_ranges.get(description=["DESCRIPTION1", "DESCRIPTION2"])
