"""Examples NbApi.tenancy.tenant_groups.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.tenancy.tenant_groups.get()

# WEB UI filter parameters
objects = nb.tenancy.tenant_groups.get(q=["TENANT GROUP1"])
objects = nb.tenancy.tenant_groups.get(tag=["tag1", "tag2"])
objects = nb.tenancy.tenant_groups.get(parent=["TENANT GROUP1"])
objects = nb.tenancy.tenant_groups.get(parent_id=[1, 2])
# 
# Data filter parameters
objects = nb.tenancy.tenant_groups.get(id=[1, 2])
objects = nb.tenancy.tenant_groups.get(name=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.tenancy.tenant_groups.get(slug=["tenant-group1", "tenant-group2"])
