"""Examples NbBranch."""

from netbox3 import NbApi, NbBranch

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# gGt object from Netbox
sites = nb.dcim.sites.get(tag="alpha")
site = sites[0]

# Get the tag slug using the NbBranch object.
branch = NbBranch(data=site)
tags = branch.tags()  # ['alpha', 'bravo', 'golf']
print(tags)
# Get

# To demonstrate the advantages of the NbBranch parser,
# getting the same data using dictionary keys as usual.
tags = [d["slug"] for d in site["tags"]]
print(tags)
