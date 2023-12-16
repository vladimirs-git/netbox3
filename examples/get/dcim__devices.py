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
objects = nb.dcim.devices.get(q="DEVICE")
objects = nb.dcim.devices.get(tag="tag1")
objects = nb.dcim.devices.get(or_tag=["tag1", "tag2"])

# Location
objects = nb.dcim.devices.get(region="REGION1")
objects = nb.dcim.devices.get(site_group="SITE GROUP1")
objects = nb.dcim.devices.get(site="SITE1")
objects = nb.dcim.devices.get(location=["LOCATION1", "LOCATION2"])
objects = nb.dcim.devices.get(rack=["RACK1", "RACK2"])

# Operation
objects = nb.dcim.devices.get(status="offline")
objects = nb.dcim.devices.get(role=["DEVICE ROLE1", "DEVICE ROLE2"])
objects = nb.dcim.devices.get(airflow=["rear-to-front", "left-to-right"])
objects = nb.dcim.devices.get(or_airflow=["rear-to-front", "left-to-right"])
objects = nb.dcim.devices.get(serial=["serial1", "serial2"])
objects = nb.dcim.devices.get(asset_tag=["AssetTag1", "AssetTag2"])
objects = nb.dcim.devices.get(mac_address=["00:00:00:00:00:01", "00:00:00:00:01:01"])

# Hardware
objects = nb.dcim.devices.get(manufacturer=["MANUFACTURER1", "MANUFACTURER2"])
objects = nb.dcim.devices.get(device_type=["MODEL1", "MODEL2"])
objects = nb.dcim.devices.get(platform=["PLATFORM1", "PLATFORM2"])

# Tenant
objects = nb.dcim.devices.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.dcim.devices.get(tenant=["TENANT1", "TENANT2"])

# Contacts
# Contact
# Contact Role
# Contact Group

# Components
objects = nb.dcim.devices.get(console_ports=True)
objects = nb.dcim.devices.get(console_server_ports=True)
objects = nb.dcim.devices.get(power_ports=True)
objects = nb.dcim.devices.get(power_outlets=True)
objects = nb.dcim.devices.get(interfaces=True)
objects = nb.dcim.devices.get(pass_through_ports=True)

# Miscellaneous
objects = nb.dcim.devices.get(has_primary_ip=True)
objects = nb.dcim.devices.get(has_oob_ip=True)
objects = nb.dcim.devices.get(virtual_chassis_member=True)
# Virtual chassis member
objects = nb.dcim.devices.get(local_context_data=True)

# Data Filter parameters
objects = nb.dcim.devices.get(id=[1, 2])
objects = nb.dcim.devices.get(name=["DEVICE1", "DEVICE2"])
objects = nb.dcim.devices.get(description=["DESCRIPTION1", "DESCRIPTION2"])
