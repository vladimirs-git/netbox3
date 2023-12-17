"""Demo NbForager tasks."""
import logging

from netbox3 import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN, threads=1)

# Create tasks
nbf.ipam.prefixes.get(q=["172.16", "172.17"])
nbf.ipam.prefixes.get(q=["172.16", "172.17"], task=True)
nbf.run_tasks()
print(nbf.ipam.prefixes)
x = 1