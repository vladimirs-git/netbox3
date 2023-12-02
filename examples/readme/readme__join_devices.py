"""Examples NbForager.grow_tree() join devices."""
from pprint import pprint

from netbox3 import NbForager, NbBranch

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN)

# Request specific devices and all sites from Netbox.
# Note that the site in the device only contains basic data and
# does not include tags, region and other extended data.
nbf.dcim.devices.get(q="PP:B")
nbf.dcim.sites.get()
device = nbf.root.dcim.devices[88]
pprint(device)
# {"id": 88,
#  "name": "PP:B117",
#  "site": {"display": "MDF",
#           "id": 21,
#           "name": "MDF",
#           "slug": "ncsu-065",
#           "url": "https://demo.netbox.dev/api/dcim/sites/21/"},
#  ...

# Assemble objects within self as multidimensional dictionary.
# Note that the device now includes site region and all other data.
tree = nbf.grow_tree()
device = tree.dcim.devices[88]
pprint(device)
# {"id": 88,
#  "name": "PP:B117",
#  "site": {"display": "MDF",
#           "id": 21,
#           "name": "MDF",
#           "slug": "ncsu-065",
#           "url": "https://demo.netbox.dev/api/dcim/sites/21/"
#           "region": {"_depth": 2,
#                      "display": "North Carolina",
#                      "id": 40,
#                      "name": "North Carolina",
#                      "slug": "us-nc",
#                      "url": "https://demo.netbox.dev/api/dcim/regions/40/"},
#           "tenant": {"display": "NC State University",
#                      "id": 13,
#                      "name": "NC State University",
#                      "slug": "nc-state",
#                      "url": "https://demo.netbox.dev/api/tenancy/tenants/13/"},
#           ...
# ...

# Access site attribute through a device.
region = device["site"]["region"]["name"]
print(f"{region=}")  # region="North Carolina"

# Use NbBranch to ensure the data type if any dictionary in the chain is missing.
region = NbBranch(device).str("site", "region", "name")
print(f"{region=}")  # region="North Carolina"
