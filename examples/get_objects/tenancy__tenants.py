"""Examples NbApi.tenancy.tenants.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.tenancy.tenants.get()

# WEB UI Filter parameters
objects = nb.tenancy.tenants.get(q=["TENANT1", "TENANT2"])
objects = nb.tenancy.tenants.get(tag=["tag1", "tag2"])
objects = nb.tenancy.tenants.get(group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.tenancy.tenants.get(group_id=[1, 2])

# Data Filter parameters
objects = nb.tenancy.tenants.get(id=[1, 2])
objects = nb.tenancy.tenants.get(name=["TENANT1", "TENANT2"])
objects = nb.tenancy.tenants.get(slug=["tenant1", "tenant2"])
