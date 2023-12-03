"""Examples NbForager.join_tree() join devices."""
import logging
from pprint import pprint

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# Get device with all related object using nested mode.
# Note that retrieved also tags, tenants, device-roles and any other related objects.
nbf.dcim.devices.get(nested=True)
print(f"{len(nbf.root.dcim.devices)=}")
print(f"{len(nbf.root.dcim.device_roles)=}")
print(f"{len(nbf.root.tenancy.tenants)=}")
print(f"{len(nbf.root.extras.tags)=}")
# len(nbf.root.dcim.devices)=78
# len(nbf.root.dcim.device_roles)=10
# len(nbf.root.tenancy.tenants)=5
# len(nbf.root.extras.tags)=2


# Assemble objects within self.
# Note that the device includes all other objects as multidimensional dictionary.
tree = nbf.join_tree()
pprint(list(tree.dcim.devices.values())[0])
# {"id": 1,
#  "name": "dmi01-akron-rtr01",
#  "rack": {"id": 1,
#           "name": "Comms closet",
#           "site": {"id": 2,
#                    "name": "DM-Akron",
#                    "tenant": {"id": 5,
#                               "name": "Dunder-Mifflin, Inc.",
#                               "group": {"id": 1,
#                                         "name": "Customers",
#                                         ...
#           "tenant": {"id": 5,
#                      "name": "Dunder-Mifflin, Inc.",
#                      "group": {"id": 1,
#                                "name": "Customers",
#                                ...
# ...
