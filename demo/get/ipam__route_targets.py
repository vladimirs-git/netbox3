"""Demo NbApi.ipam.route_targets.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.route_targets.get()

# WEB UI Filter parameters
objects = nb.ipam.route_targets.get(q=["65101"])
objects = nb.ipam.route_targets.get(tag="tag1")
objects = nb.ipam.route_targets.get(or_tag=["tag1", "tag2"])

# VRF
objects = nb.ipam.route_targets.get(importing_vrf=["VRF1", "VRF2"])
objects = nb.ipam.route_targets.get(importing_vrf_id=[1, 2])
objects = nb.ipam.route_targets.get(exporting_vrf=["VRF1", "VRF2"])
objects = nb.ipam.route_targets.get(exporting_vrf_id=[1, 2])

# Tenant
objects = nb.ipam.route_targets.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.ipam.route_targets.get(tenant_group_id=[1, 2])
objects = nb.ipam.route_targets.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.route_targets.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.route_targets.get(id=[1, 2])
objects = nb.ipam.route_targets.get(name=["65101:1", "65102:1"])
objects = nb.ipam.route_targets.get(description="DESCRIPTION1")
