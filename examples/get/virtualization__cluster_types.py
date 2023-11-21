"""Examples NbApi.virtualization.cluster_types.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.virtualization.cluster_types.get()

# WEB UI Filter parameters
objects = nb.virtualization.cluster_types.get(q=["CLUSTER TYPE"])
objects = nb.virtualization.cluster_types.get(tag="tag1")
objects = nb.virtualization.cluster_types.get(or_tag=["tag1", "tag2"])

# Data Filter parameters
objects = nb.virtualization.cluster_types.get(id=[1, 2])
objects = nb.virtualization.cluster_types.get(name=["CLUSTER TYPE1", "CLUSTER TYPE2"])
objects = nb.virtualization.cluster_types.get(slug=["cluster-type1", "cluster-type2"])
objects = nb.virtualization.cluster_types.get(description=["DESCRIPTION1", "DESCRIPTION2"])
