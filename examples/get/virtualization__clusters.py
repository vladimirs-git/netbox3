"""Examples NbApi.virtualization.clusters.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.virtualization.clusters.get()

# WEB UI Filter parameters
objects = nb.virtualization.clusters.get(q=["CLUSTER"])
objects = nb.virtualization.clusters.get(tag="tag1")
objects = nb.virtualization.clusters.get(or_tag=["tag1", "tag2"])

# Attributes
objects = nb.virtualization.clusters.get(group=["CLUSTER GROUP1", "CLUSTER GROUP2"])
objects = nb.virtualization.clusters.get(group_id=[6, 7])

# Location

# Tenant

# Data Filter parameters
objects = nb.virtualization.clusters.get(id=[41, 42])
objects = nb.virtualization.clusters.get(name=["CLUSTER1", "CLUSTER2"])
objects = nb.virtualization.clusters.get(description=["DESCRIPTION1", "DESCRIPTION2"])
