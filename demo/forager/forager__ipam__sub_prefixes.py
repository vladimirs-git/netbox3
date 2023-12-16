"""Demo, How to create super_prefix, sub_prefixes for ipam objects.

Add key/values ipv4, aggregate super_prefix, sub_prefixes to the following objects:

- NbForager.tree.ipam.aggregates
- NbForager.tree.ipam.prefixes
- NbForager.tree.ipam.ip_addresses
"""
import logging

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get the objects from Netbox
nbf.ipam.aggregates.get()
nbf.ipam.prefixes.get()
nbf.ipam.ip_addresses.get()
nbf.join_tree()

aggregate = nbf.ipam.aggregates.find_tree(family__value=4)[0]
print(f"aggregate ipv4: ", aggregate["ipv4"])
print(f"aggregate sub_prefixes: ", [d["prefix"] for d in aggregate["sub_prefixes"]])
# aggregate ipv4:  <IPv4Obj 10.0.0.0/8>
# aggregate sub_prefixes:  ["10.3.0.0/23", "10.3.0.0/23", "10.3.0.0/23", ...

prefix = nbf.ipam.prefixes.find_tree(family__value=4, vrf=None)[0]
print(f"prefix ipv4: ", prefix["ipv4"])
print(f"prefix aggregate: ", prefix["aggregate"].get("prefix"))
print(f"prefix super_prefix: ", prefix["super_prefix"].get("prefix"))
print(f"prefix sub_prefixes: ", [d["prefix"] for d in prefix["sub_prefixes"]])
# prefix ipv4:  <IPv4Obj 10.112.0.0/15>
# prefix aggregate:  10.0.0.0/8
# prefix super_prefix:  None
# prefix sub_prefixes:  ["10.112.0.0/17", "10.112.128.0/17"]

ip_address = nbf.ipam.ip_addresses.find_tree(family__value=4, vrf=None)[0]
print(f"ip_address ipv4: ", ip_address["ipv4"])
print(f"ip_address super_prefix: ", ip_address["super_prefix"].get("prefix"))
# ip_address ipv4:  <IPv4Obj 10.3.0.1/24>
# ip_address super_prefix:  10.3.0.0/24
