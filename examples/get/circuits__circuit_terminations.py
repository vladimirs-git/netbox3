"""Examples NbApi.circuits.circuit_terminations.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.circuit_terminations.get()

# WEB UI Filter parameters

# Data Filter parameters
objects = nb.circuits.circuit_terminations.get(id=[1, 2])
objects = nb.circuits.circuit_terminations.get(tag="tag1")
objects = nb.circuits.circuit_terminations.get(or_tag=["tag1", "tag2"])

objects = nb.circuits.circuit_terminations.get(circuit=["CID1", "CID2"])
objects = nb.circuits.circuit_terminations.get(circuit_id=[1, 2])

objects = nb.circuits.circuit_terminations.get(site=["SITE1", "SITE2"])
objects = nb.circuits.circuit_terminations.get(site_id=[1, 2])
objects = nb.circuits.circuit_terminations.get(port_speed=[100000, 200000])

# Text pattern
objects = nb.circuits.circuit_terminations.get(
    description=["DESCRIPTION1", "DESCRIPTION2"])  # case-sensitive
objects = nb.circuits.circuit_terminations.get(description__empty=True)  # is empty
objects = nb.circuits.circuit_terminations.get(
    description__ic="script")  # case-insensitive contains
objects = nb.circuits.circuit_terminations.get(
    description__ie="description1")  # case-insensitive exact
objects = nb.circuits.circuit_terminations.get(
    description__iew="tion1")  # case-insensitive ends with
objects = nb.circuits.circuit_terminations.get(
    description__isw="descr")  # case-insensitive starts with
objects = nb.circuits.circuit_terminations.get(description__n="DESCRIPTION1")  # not case-sensitive
objects = nb.circuits.circuit_terminations.get(
    description__nic="script")  # not case-insensitive contains
objects = nb.circuits.circuit_terminations.get(
    description__nie="description1")  # not case-insensitive exact
objects = nb.circuits.circuit_terminations.get(
    description__niew="tion1")  # not case-insensitive ends with
objects = nb.circuits.circuit_terminations.get(
    description__nisw="descr")  # not case-insensitive starts with

# Date pattern
objects = nb.circuits.circuit_terminations.get(created="2000-12-31T23:59:59Z")
objects = nb.circuits.circuit_terminations.get(created__empty=True)  # is empty
objects = nb.circuits.circuit_terminations.get(created__gt="2000-12-31T23:59")  # greater than
objects = nb.circuits.circuit_terminations.get(
    created__gte="2000-12-31T23:59")  # greater than or equal
objects = nb.circuits.circuit_terminations.get(created__lt="2000-12-31T23:59")  # less than
objects = nb.circuits.circuit_terminations.get(
    created__lte="2000-12-31T23:59")  # less than or equal
objects = nb.circuits.circuit_terminations.get(created__n="2000-12-31T23:59")  # not

objects = nb.circuits.circuit_terminations.get(last_updated="2000-12-31T23:59:59Z")
objects = nb.circuits.circuit_terminations.get(last_updated__empty=True)
objects = nb.circuits.circuit_terminations.get(last_updated__gt="2000-12-31T23:59")
objects = nb.circuits.circuit_terminations.get(last_updated__gte="2000-12-31T23:59")
objects = nb.circuits.circuit_terminations.get(last_updated__lt="2000-12-31T23:59")
objects = nb.circuits.circuit_terminations.get(last_updated__lte="2000-12-31T23:59")
objects = nb.circuits.circuit_terminations.get(last_updated__n="2000-12-31T23:59")
