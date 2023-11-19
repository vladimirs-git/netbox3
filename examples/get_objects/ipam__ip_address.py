"""Examples NbApi.ipam.ip_addresses.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.ip_addresses.get(description__n="description1")  # not
objects = nb.ipam.ip_addresses.get()

# WEB UI Filter parameters
objects = nb.ipam.ip_addresses.get(q="172.16.0")
objects = nb.ipam.ip_addresses.get(q=["172.16.0", "172.16.1"])
objects = nb.ipam.ip_addresses.get(tag=["tag1", "tag2"])

# Attributes
objects = nb.ipam.ip_addresses.get(parent=["172.16.0.0/24", "172.16.1.0/24"])
objects = nb.ipam.ip_addresses.get(family=[4, 6])
objects = nb.ipam.ip_addresses.get(status=["active", "reserved"])
objects = nb.ipam.ip_addresses.get(role=["secondary", "hsrp"])
objects = nb.ipam.ip_addresses.get(mask_length=[24, 32])
objects = nb.ipam.ip_addresses.get(assigned_to_interface=True)
objects = nb.ipam.ip_addresses.get(dns_name="domain.com")

# VRF
objects = nb.ipam.ip_addresses.get(vrf="null")
objects = nb.ipam.ip_addresses.get(vrf=["Alpha", "Bravo"])
objects = nb.ipam.ip_addresses.get(vrf_id=[1, 2])
objects = nb.ipam.ip_addresses.get(present_in_vrf=["alpha", "bravo"])
objects = nb.ipam.ip_addresses.get(present_in_vrf_id=[1, 2])

# Tenant
objects = nb.ipam.ip_addresses.get(tenant_group=["TENANT GROUP1"])
objects = nb.ipam.ip_addresses.get(tenant_group_id=[1])
objects = nb.ipam.ip_addresses.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.ip_addresses.get(tenant_id=[1, 2])

# Device/VM
objects = nb.ipam.ip_addresses.get(device=["DEVICE1", "DEVICE2"])
objects = nb.ipam.ip_addresses.get(device_id=[1, 2])
objects = nb.ipam.ip_addresses.get(virtual_machine=["VM1", "VM2"])
objects = nb.ipam.ip_addresses.get(virtual_machine_id=[1, 2])

# Custom fields
objects = nb.ipam.ip_addresses.get(cf_name=["value1", "value2"])

# Data Filter parameters
objects = nb.ipam.ip_addresses.get(id=[1, 2])
objects = nb.ipam.ip_addresses.get(address=["172.16.0.1/24", "172.16.1.1/24"])

# Text pattern
objects = nb.ipam.ip_addresses.get(description=["DESCRIPTION1", "DESCRIPTION2"])  # case-sensitive
objects = nb.ipam.ip_addresses.get(description__empty=True)  # is empty
objects = nb.ipam.ip_addresses.get(description__ic="script")  # case-insensitive contains
objects = nb.ipam.ip_addresses.get(description__ie="description1")  # case-insensitive exact
objects = nb.ipam.ip_addresses.get(description__iew="tion1")  # case-insensitive ends with
objects = nb.ipam.ip_addresses.get(description__isw="descr")  # case-insensitive starts with
objects = nb.ipam.ip_addresses.get(description__n="DESCRIPTION1")  # not case-sensitive
objects = nb.ipam.ip_addresses.get(description__nic="script")  # not case-insensitive contains
objects = nb.ipam.ip_addresses.get(description__nie="description1")  # not case-insensitive exact
objects = nb.ipam.ip_addresses.get(description__niew="tion1")  # not case-insensitive ends with
objects = nb.ipam.ip_addresses.get(description__nisw="descr")  # not case-insensitive starts with

# Date pattern
objects = nb.ipam.ip_addresses.get(created="2000-12-31T23:59:59Z")
objects = nb.ipam.ip_addresses.get(created__empty=True)  # is empty
objects = nb.ipam.ip_addresses.get(created__gt="2000-12-31T23:59")  # greater than
objects = nb.ipam.ip_addresses.get(created__gte="2000-12-31T23:59")  # greater than or equal
objects = nb.ipam.ip_addresses.get(created__lt="2000-12-31T23:59")  # less than
objects = nb.ipam.ip_addresses.get(created__lte="2000-12-31T23:59")  # less than or equal
objects = nb.ipam.ip_addresses.get(created__n="2000-12-31T23:59")  # not

objects = nb.ipam.ip_addresses.get(last_updated="2000-12-31T23:59:59Z")
objects = nb.ipam.ip_addresses.get(last_updated__empty=True)
objects = nb.ipam.ip_addresses.get(last_updated__gt="2000-12-31T23:59")
objects = nb.ipam.ip_addresses.get(last_updated__gte="2000-12-31T23:59")
objects = nb.ipam.ip_addresses.get(last_updated__lt="2000-12-31T23:59")
objects = nb.ipam.ip_addresses.get(last_updated__lte="2000-12-31T23:59")
objects = nb.ipam.ip_addresses.get(last_updated__n="2000-12-31T23:59")
