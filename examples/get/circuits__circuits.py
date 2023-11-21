"""Examples NbApi.circuits.circuits.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.circuits.get()

# WEB UI Filter parameters
objects = nb.circuits.circuits.get(q=["CID1", "CID2"])
objects = nb.circuits.circuits.get(tag="tag1")
objects = nb.circuits.circuits.get(or_tag=["tag1", "tag2"])

# Provider
objects = nb.circuits.circuits.get(provider=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.circuits.get(provider_id=[1, 2])
objects = nb.circuits.circuits.get(provider_account=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.circuits.get(provider_account_id=[1, 2])

# Attributes
objects = nb.circuits.circuits.get(type=["Direct Internet Access", "WAN link"])
objects = nb.circuits.circuits.get(type_id=[1, 2])
objects = nb.circuits.circuits.get(status=["active", "offline"])

# Location
objects = nb.circuits.circuits.get(region=["USA", "EU"])
objects = nb.circuits.circuits.get(region_id=[1, 2])
objects = nb.circuits.circuits.get(site_group=["GROUP1", "GROUP2"])
objects = nb.circuits.circuits.get(site_group_id=[1, 2])
objects = nb.circuits.circuits.get(site=["SITE1", "SITE2"])
objects = nb.circuits.circuits.get(site_id=[1, 2])

# Tenant
objects = nb.circuits.circuits.get(tenant_group=["GROUP1", "GROUP2"])
objects = nb.circuits.circuits.get(tenant_group_id=[1, 2])
objects = nb.circuits.circuits.get(tenant=["TENANT1", "TENANT2"])
objects = nb.circuits.circuits.get(tenant_id=[1, 2])

# custom_fields
objects = nb.circuits.circuits.get(cf_monitoring_ip=["10.0.0.1", "10.0.0.2"])

# Data Filter parameters
objects = nb.circuits.circuits.get(id=[1, 2])
objects = nb.circuits.circuits.get(cid=["CID1", "CID2"])
objects = nb.circuits.circuits.get(description=["DESCRIPTION1", "DESCRIPTION2"])
