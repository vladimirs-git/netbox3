"""Examples NbApi.ipam.vlans.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.vlans.get()

# WEB UI Filter parameters
objects = nb.ipam.vlans.get(q=["VLAN"])
objects = nb.ipam.vlans.get(tag=["tag1", "tag2"])
objects = nb.ipam.vlans.get(region=["REGION1", "REGION2"])
objects = nb.ipam.vlans.get(region_id=[1, 2])  # not working
objects = nb.ipam.vlans.get(site_group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.ipam.vlans.get(site_group_id=[1, 2])  # not working
objects = nb.ipam.vlans.get(site=["SITE1", "SITE2"])
objects = nb.ipam.vlans.get(site_id=[1, 2])

objects = nb.ipam.vlans.get(group=["VLAN GROUP1", "VLAN GROUP2"])
objects = nb.ipam.vlans.get(group_id=[1, 2])
objects = nb.ipam.vlans.get(status=["deprecated", "reserved"])
objects = nb.ipam.vlans.get(role=["ROLE1", "ROLE2"])
objects = nb.ipam.vlans.get(vid=[1, 2])
objects = nb.ipam.vlans.get(l2vpn=[])
objects = nb.ipam.vlans.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.ipam.vlans.get(tenant_group_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.vlans.get(id=[1, 2])
objects = nb.ipam.vlans.get(name=["VLAN1", "VLAN2"])
objects = nb.ipam.vlans.get(description=["DESCRIPTION1", "DESCRIPTION2"])
objects = nb.ipam.vlans.get(created=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
objects = nb.ipam.vlans.get(last_updated=["2000-12-31T23:59:59Z", "2001-01-01T01:01:01Z"])
