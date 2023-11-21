"""Examples for README: create, update, delete ip address object."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# Create 2 addresses with different methods (different outputs)
response = nb.ip_addresses.create(address="1.2.3.4/24", tags=[1], status="active")
print(response)  # <Response [201]>
data = nb.ip_addresses.create_d(address="1.2.3.4/24", tags=[2], status="reserved")
print(data)  # {'id': 183, 'display': '1.2.3.4/24', ...

# Get all addresses
addresses = nb.ip_addresses.get()
print(len(addresses))  # 181

# Get all ip-addresses in global routing
addresses = nb.ip_addresses.get(vrf="null")
print(len(addresses))  # 30
# Get newly created ip-addresses
addresses = nb.ip_addresses.get(tag="alpha")
print(len(addresses))  # 1
addresses = nb.ip_addresses.get(or_tag=["alpha", "bravo"])
print(len(addresses))  # 2

# Complex filter.
# Get addresses that do not have VRF and
# (have either the tag "alpha" or "bravo") and
# (have a status of either active or reserved).
addresses = nb.ip_addresses.get(vrf="null",
                                or_tag=["alpha", "bravo"],
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
