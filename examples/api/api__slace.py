"""Examples NbApi.ipam.ip_addresses.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN, url_length=200, threads=20)

addresses = [f"172.16.0.{i}/24" for i in range(256)]
objects = nb.ipam.ip_addresses.get(address=addresses, family=4)
print(f"{len(objects)=}")
