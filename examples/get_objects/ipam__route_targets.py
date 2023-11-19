"""Examples NbApi.ipam.route_targets.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.route_targets.get()

# WEB UI Filter parameters
objects = nb.ipam.route_targets.get(q=["65101"])
objects = nb.ipam.route_targets.get(tag=["tag1", "tag2"])
objects = nb.ipam.route_targets.get(importing_vrf=["VRF1", "VRF2"])
objects = nb.ipam.route_targets.get(importing_vrf_id=[1, 2])
objects = nb.ipam.route_targets.get(exporting_vrf=["VRF1", "VRF2"])
objects = nb.ipam.route_targets.get(exporting_vrf_id=[1, 2])
objects = nb.ipam.route_targets.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.ipam.route_targets.get(tenant_group_id=[1, 2])
objects = nb.ipam.route_targets.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.route_targets.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.route_targets.get(id=[1, 2])
objects = nb.ipam.route_targets.get(name=["65101:1", "65102:1"])
objects = nb.ipam.route_targets.get(description="DESCRIPTION1")
objects = nb.ipam.route_targets.get(created=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
objects = nb.ipam.route_targets.get(last_updated=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
