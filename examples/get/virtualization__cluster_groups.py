"""Examples NbApi.virtualization.cluster_groups.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.virtualization.cluster_groups.get()

# WEB UI Filter parameters
objects = nb.virtualization.cluster_groups.get(q=["CLUSTER GROUP"])
objects = nb.virtualization.cluster_groups.get(tag="tag1")
objects = nb.virtualization.cluster_groups.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.virtualization.cluster_groups.get(id=[1, 2])
objects = nb.virtualization.cluster_groups.get(name=["CLUSTER GROUP1", "CLUSTER GROUP2"])
objects = nb.virtualization.cluster_groups.get(slug=["cluster-group1", "cluster-group2"])
objects = nb.virtualization.cluster_groups.get(description=["DESCRIPTION1", "DESCRIPTION2"])
