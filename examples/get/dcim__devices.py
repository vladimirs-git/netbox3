"""Examples NbApi.dcim.devices.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.devices.get()

# WEB UI Filter parameters
objects = nb.dcim.devices.get(q=["DEVICE"])
objects = nb.dcim.devices.get(tag="tag1")
objects = nb.dcim.devices.get(or_tag=["tag1", "tag2"])

# Location
# Region
# Site group
# Site
# Location
# Rack

# Operation
# Status
# Role
# Airflow
# Serial
# Asset tag
# MAC address

# Hardware
# Manufacturer
# Model
# Platform

# Tenant
# Tenant group
# Tenant

# Contacts
# Contact
# Contact Role
# Contact Group

# Components
# Has console ports
# Has console server ports
# Has power ports
# Has power outlets
# Has interfaces
# Has pass-through port

# Miscellaneous
# Has a primary IP
# Has an OOB IP
# Virtual chassis member
# Config template
# Has local config context data

# Data Filter parameters
objects = nb.dcim.devices.get(id=[1, 2])
objects = nb.dcim.devices.get(name=["DEVICE1", "DEVICE2"])
objects = nb.dcim.devices.get(description=["DESCRIPTION1", "DESCRIPTION2"])
