"""Demo for README."""
import logging
from datetime import datetime

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"

# Get data in threading mode.
start = datetime.now()
nb = NbApi(host=HOST, token=TOKEN, threads=10, interval=0.1, limit=200)
objects = nb.ipam.ip_addresses.get()
seconds = (datetime.now() - start).seconds
print([d["address"] for d in objects])
print(f"{len(objects)=} {seconds=}")
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/?brief=1&limit=1 ...
# DEBUG    Starting new HTTPS connection (2): demo.netbox.dev:443
# DEBUG    Starting new HTTPS connection (3): demo.netbox.dev:443
# DEBUG    Starting new HTTPS connection (4): demo.netbox.dev:443
# DEBUG    Starting new HTTPS connection (5): demo.netbox.dev:443
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
# len(objects)=4153 seconds=3


# Get data in loop mode, to compare time performance.
start = datetime.now()
nb = NbApi(host=HOST, token=TOKEN)
objects = nb.ipam.ip_addresses.get()
seconds = (datetime.now() - start).seconds
print(f"{len(objects)=} {seconds=}")
# DEBUG    : Starting new HTTPS connection (1): demo.netbox.dev:443
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
# DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
# len(objects)=4153 seconds=7
