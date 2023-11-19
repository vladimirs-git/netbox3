"""Examples NbApi.circuits.circuit_terminations.get()."""
import logging

from netbox3 import NbApi

# Enable DEBUG mode to demonstrate the speed of requests to the Netbox API
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.circuit_terminations.get()

# WEB UI Filter parameters

# Data Filter parameters
objects = nb.circuits.circuit_terminations.get(id=[1, 2])
objects = nb.circuits.circuit_terminations.get(tag=["tag1", "tag2"])
objects = nb.circuits.circuit_terminations.get(circuit=["CID1", "CID2"])
objects = nb.circuits.circuit_terminations.get(circuit_id=[1, 2])
objects = nb.circuits.circuit_terminations.get(site=["SITE1", "SITE2"])
objects = nb.circuits.circuit_terminations.get(site_id=[1, 2])
objects = nb.circuits.circuit_terminations.get(port_speed=[100000, 200000])
