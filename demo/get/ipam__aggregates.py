"""Demo NbApi.ipam.aggregates.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.aggregates.get()

# WEB UI Filter parameters
objects = nb.ipam.aggregates.get(q=["10.0.0.0", "192.168.0.0"])
objects = nb.ipam.aggregates.get(tag="tag1")
objects = nb.ipam.aggregates.get(or_tag=["tag1", "tag2"])

objects = nb.ipam.aggregates.get(family=[4, 6])
objects = nb.ipam.aggregates.get(rir=["RFC 1918"])
objects = nb.ipam.aggregates.get(rir_id=[1])

# Tenant
objects = nb.ipam.aggregates.get(tenant_group=["TENANT GROUP1"])
objects = nb.ipam.aggregates.get(tenant_group_id=[1])
objects = nb.ipam.aggregates.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.aggregates.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.aggregates.get(id=[1, 2])
objects = nb.ipam.aggregates.get(prefix=["10.0.0.0/8", "192.168.0.0/16"])
objects = nb.ipam.aggregates.get(description=["DESCRIPTION1", "DESCRIPTION2"])
