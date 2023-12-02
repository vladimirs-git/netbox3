"""Examples NbApi.tenancy.tenants.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.tenancy.tenants.get()

# WEB UI Filter parameters
objects = nb.tenancy.tenants.get(q=["TENANT1", "TENANT2"])
objects = nb.tenancy.tenants.get(tag="tag1")
objects = nb.tenancy.tenants.get(or_tag=["tag1", "tag2"])
objects = nb.tenancy.tenants.get(group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.tenancy.tenants.get(group_id=[1, 2])

# Data Filter parameters
objects = nb.tenancy.tenants.get(id=[1, 2])
objects = nb.tenancy.tenants.get(name=["TENANT1", "TENANT2"])
objects = nb.tenancy.tenants.get(slug=["tenant1", "tenant2"])
