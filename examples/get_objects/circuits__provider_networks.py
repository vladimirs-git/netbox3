"""Examples NbApi.circuits.provider_networks.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.provider_networks.get()

# WEB UI Filter parameters
objects = nb.circuits.provider_networks.get(q=["PROVIDER NETWORK"])
objects = nb.circuits.provider_networks.get(tag=["tag1", "tag2"])
objects = nb.circuits.provider_networks.get(provider=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.provider_networks.get(provider_id=[1, 2])
objects = nb.circuits.provider_networks.get(service_id=["Service ID"])

# Data Filter parameters
objects = nb.circuits.provider_networks.get(id=[1, 2])
objects = nb.circuits.provider_networks.get(name=["PROVIDER NETWORK1", "PROVIDER NETWORK2"])
objects = nb.circuits.provider_networks.get(description=["DESCRIPTION1", "DESCRIPTION2"])
