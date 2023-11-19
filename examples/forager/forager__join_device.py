"""Examples NbForager.grow_tree() single device."""
from pprint import pprint

from netbox3 import NbForager

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nbf = NbForager(host=HOST, token=TOKEN)

# Get all sites and only 3 devices from Netbox.
# Note that the site in the device only contains basic data and
# does not include tags, region and other extended data.
nbf.dcim.sites.get()
nbf.dcim.devices.get(max_limit=3)
pprint(nbf.root.dcim.devices)
# {88: {'id': 88,
#       'name': 'PP:B117',
#       'site': {'id': 21,
#                'name': 'MDF',
#                'slug': 'ncsu-065',
#                'url': 'https://demo.netbox.dev/api/dcim/sites/21/'},
#      ...

# Join objects within self.
# Note that the device now includes site region and all other data.
tree = nbf.grow_tree()
pprint(tree.dcim.devices)
# {88: {'id': 88,
#       'name': 'PP:B117',
#       'site': {'id': 21,
#                'region': {'id': 40,
#                           'name': 'North Carolina',
#                           'url': 'https://demo.netbox.dev/api/dcim/regions/40/'},
#      ...

# You can access any site attribute through a device.
print(tree.dcim.devices[88]["site"]["region"]["name"])  # North Carolina
