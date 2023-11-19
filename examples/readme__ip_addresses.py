"""Examples for README: create, update, delete ip address object."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# Create 2 addresses with different parameters
response = nb.ip_addresses.create(address="1.2.3.4/24", tags=[1], status="active")
print(response)  # <Response [201]>
response = nb.ip_addresses.create(address="1.2.3.4/24", tags=[2], status="reserved")
print(response)  # <Response [201]>

# Get all addresses
addresses = nb.ip_addresses.get()
print(len(addresses))  # 181

# Simple filter
addresses = nb.ip_addresses.get(vrf="null")
print(len(addresses))  # 30
addresses = nb.ip_addresses.get(tag=["alpha", "bravo"])
print(len(addresses))  # 4

# Complex filter.
# Get addresses that do not have VRF and
# (have either the tag "alpha" or "bravo") and
# (have a status of either active or reserved).
addresses = nb.ip_addresses.get(vrf="null",
                                tag=["alpha", "bravo"],
                                status=["active", "reserved"])
print(len(addresses))  # 2

addresses = nb.ip_addresses.get(address="1.2.3.4/24")
for address in addresses:
    # Update
    id_ = address["id"]
    response = nb.ip_addresses.update(id=id_, description="text")
    print(response)  # <Response [200]>
    print(nb.ip_addresses.get(id=id_)[0]["description"])  # text

    # Delete
    response = nb.ip_addresses.delete(id=id_)
    print(response)  # <Response [204]>
