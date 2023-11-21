"""Examples NbApi.ipam.vlan_groups.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.vlan_groups.get()

# WEB UI Filter parameters
objects = nb.ipam.vlan_groups.get(q=["VLAN GROUP"])
objects = nb.ipam.vlan_groups.get(tag="tag1")
objects = nb.ipam.vlan_groups.get(or_tag=["tag1", "tag2"])

# Location
objects = nb.ipam.vlan_groups.get(region=["REGION1", "REGION2"])  # not working
objects = nb.ipam.vlan_groups.get(region_id=[1, 2])  # not working
objects = nb.ipam.vlan_groups.get(site_group=["SITE GROUP1", "SITE GROUP2"])  # not working
objects = nb.ipam.vlan_groups.get(site_group_id=[1, 2])  # not working
objects = nb.ipam.vlan_groups.get(site=["SITE1", "SITE2"])
objects = nb.ipam.vlan_groups.get(site_id=[1, 2])
objects = nb.ipam.vlan_groups.get(location=["LOCATION1", "LOCATION2"])
objects = nb.ipam.vlan_groups.get(location_id=[1, 2])
objects = nb.ipam.vlan_groups.get(rack=["RACK1", "RACK2"])
objects = nb.ipam.vlan_groups.get(rack_id=[1, 2])

# VLAN ID
objects = nb.ipam.vlan_groups.get(min_vid=[1])
objects = nb.ipam.vlan_groups.get(max_vid=[4094])

# Data Filter parameters
objects = nb.ipam.vlan_groups.get(id=[1, 2])
objects = nb.ipam.vlan_groups.get(name=["VLAN GROUP1", "VLAN GROUP2"])
objects = nb.ipam.vlan_groups.get(slug=["vlan-group1", "vlan-group2"])
objects = nb.ipam.vlan_groups.get(description=["DESCRIPTION1", "DESCRIPTION2"])
