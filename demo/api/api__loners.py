"""Demo of how to set loners."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# Just for demonstration, switch filtering parameters to Netbox API default behavior
nb.ipam.aggregates._loners = []

# Attempting to filter two aggregates
# Note: The Netbox API only returns an object for the last value
# https://github.com/netbox-community/netbox/discussions/14305
objects = nb.ipam.aggregates.get(prefix=["10.0.0.0/8", "192.168.0.0/16"])
print([d["prefix"] for d in objects])
# ["192.168.0.0/16"]

# Fixing ipam/aggregates, to get multiple objects for multiple prefixes in request
loners = {"ipam/aggregates/": ["^prefix$"]}
nb = NbApi(host=HOST, token=TOKEN, loners=loners)

# Successfully filtered 2 aggregates.
objects = nb.ipam.aggregates.get(prefix=["10.0.0.0/8", "192.168.0.0/16"])
print([d["prefix"] for d in objects])
# ["10.0.0.0/8", "192.168.0.0/16"]
