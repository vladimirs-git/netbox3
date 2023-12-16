"""Demo NbApi.dcim.interfaces.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.interfaces.get()

# WEB UI Filter parameters
objects = nb.dcim.interfaces.get(q=["GigabitEthernet"])
objects = nb.dcim.interfaces.get(tag="tag1")
objects = nb.dcim.interfaces.get(or_tag=["tag1", "tag2"])

# Attributes
objects = nb.dcim.interfaces.get(name=["GigabitEthernet1/0/1"])
objects = nb.dcim.interfaces.get(label=["LABEL1"])
objects = nb.dcim.interfaces.get(kind=["physical", "virtual", "wireless"])
objects = nb.dcim.interfaces.get(type=["virtual", "bridge", "lag", "100base-fx"])
objects = nb.dcim.interfaces.get(speed=[1000000])
objects = nb.dcim.interfaces.get(duplex=["half", "full", "auto"])
objects = nb.dcim.interfaces.get(enabled=True)
objects = nb.dcim.interfaces.get(mgmt_only=True)

# Addressing
objects = nb.dcim.interfaces.get(vrf=["VRF1", "VRF2"])
objects = nb.dcim.interfaces.get(vrf_id=[1, 2])
# L2VPN
# MAC address
# WWN

# PoE
# PoE mode
# PoE type

# Wireless
# Wireless role
# Wireless channel
# Channel width (MHz)
# Transmit power (dBm)

# Location
objects = nb.dcim.interfaces.get(region=["REGION1", "REGION2"])
objects = nb.dcim.interfaces.get(region_id=[1, 2])
objects = nb.dcim.interfaces.get(site_group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.dcim.interfaces.get(site_group_id=[1, 2])
objects = nb.dcim.interfaces.get(site=["SITE1", "SITE2"])
objects = nb.dcim.interfaces.get(site_id=[1, 2])
objects = nb.dcim.interfaces.get(location=["LOCATION1", "LOCATION2"])
objects = nb.dcim.interfaces.get(location_id=[1, 2])
objects = nb.dcim.interfaces.get(rack=["RACK1", "RACK2"])
objects = nb.dcim.interfaces.get(rack_id=[1, 2])

# Device
objects = nb.dcim.interfaces.get(device_type=["MODEL1", "MODEL2"])
objects = nb.dcim.interfaces.get(device_type_id=[1, 2])
objects = nb.dcim.interfaces.get(device_role=["DEVICE ROLE1", "DEVICE ROLE2"])
objects = nb.dcim.interfaces.get(device_role_id=[1, 2])
objects = nb.dcim.interfaces.get(device=["DEVICE1", "DEVICE2"])
objects = nb.dcim.interfaces.get(device_id=[1, 2])
objects = nb.dcim.interfaces.get(virtual_chassis=["VIRTUAL CHASSIS1"])
objects = nb.dcim.interfaces.get(virtual_chassis_id=[1, 2])

# Connection
objects = nb.dcim.interfaces.get(cabled=True)
objects = nb.dcim.interfaces.get(connected=True)
objects = nb.dcim.interfaces.get(occupied=True)

# Data Filter parameters
objects = nb.dcim.interfaces.get(id=[1, 2])
objects = nb.dcim.interfaces.get(description=["DESCRIPTION1", "DESCRIPTION2"])
