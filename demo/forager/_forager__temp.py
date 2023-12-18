"""Demo NbForager tasks."""
import logging

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN, threads=10)

# get
# nbf.ipam.ip_addresses.get(q=["172.16", "172.17"])
nbf.ipam.ip_addresses.tasks.get(q=["172.16", "172.17"])
results = nbf.tasks.run()
print(results)
print(nbf.ipam.ip_addresses)

# update
objs = nbf.api.ipam.ip_addresses.get(id=[31, 361])
datas = [{"id": d["id"], "description": "DESCR1"} for d in objs]
nbf.ipam.ip_addresses.tasks.update(datas)
results = nbf.tasks.run()
print(results)
print(nbf.ipam.ip_addresses)
x = 1
