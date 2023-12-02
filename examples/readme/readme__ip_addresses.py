"""Examples for README: create, update, delete ip address object."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# Create 2 addresses with different methods (different outputs)
response = nb.ipam.ip_addresses.create(address="1.2.3.4/24", tags=[2], status="active")
print(response)  # <Response [201]>
data = nb.ipam.ip_addresses.create_d(address="1.2.3.4/24", tags=[3], status="reserved")
print(data)  # {"id": 183, "display": "1.2.3.4/24", ...

# Get all addresses
addresses = nb.ipam.ip_addresses.get()
print(len(addresses))  # 181

# Get all ip-addresses in global routing
addresses = nb.ipam.ip_addresses.get(vrf="null")
print(len(addresses))  # 30

# Get newly created ip-addresses by complex filter
# Note, you can use parameters similarly to the ``OR`` operator.
# Filter addresses in the global routing AND
# (have either the tag "bravo" OR "charlie") AND
# (have a status of either active OR reserved).
addresses = nb.ipam.ip_addresses.get(or_q=["1.2.3", "4.5.6"],
                                     vrf="null",
                                     or_tag=["bravo", "charlie"],
                                     status=["active", "reserved"])
print(len(addresses))  # 2

addresses = nb.ipam.ip_addresses.get(address="1.2.3.4/24")
for address in addresses:
    # Update
    id_ = address["id"]
    response = nb.ipam.ip_addresses.update(id=id_, description="text")
    print(response)  # <Response [200]>
    print(nb.ipam.ip_addresses.get(id=id_)[0]["description"])  # text

    # Delete
    response = nb.ipam.ip_addresses.delete(id=id_)
    print(response)  # <Response [204]>
