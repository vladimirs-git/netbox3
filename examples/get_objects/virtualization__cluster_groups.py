"""Examples NbApi.virtualization.cluster_groups.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.virtualization.cluster_groups.get()

# WEB UI Filter parameters
objects = nb.virtualization.cluster_groups.get(q=["CLUSTER GROUP"])
objects = nb.virtualization.cluster_groups.get(tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.virtualization.cluster_groups.get(id=[1, 2])
objects = nb.virtualization.cluster_groups.get(name=["CLUSTER GROUP1", "CLUSTER GROUP2"])
objects = nb.virtualization.cluster_groups.get(slug=["cluster-group1", "cluster-group2"])
objects = nb.virtualization.cluster_groups.get(description=["DESCRIPTION1", "DESCRIPTION2"])
