"""Examples NbApi.virtualization.virtual_machines.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.virtualization.virtual_machines.get()

# WEB UI Filter parameters
objects = nb.virtualization.virtual_machines.get(q=["VIRTUAL MACHINE"])
objects = nb.virtualization.virtual_machines.get(tag="tag1")
objects = nb.virtualization.virtual_machines.get(or_tag=["tag1", "tag2"])

# Cluster
objects = nb.virtualization.virtual_machines.get(cluster_group=["CLUSTER GROUP1"])
objects = nb.virtualization.virtual_machines.get(cluster_type=["CLUSTER TYPE1"])
objects = nb.virtualization.virtual_machines.get(cluster=["CLUSTER1"])
objects = nb.virtualization.virtual_machines.get(device=["DEVICE1"])

# Location
objects = nb.virtualization.virtual_machines.get(region=["REGION1"])
objects = nb.virtualization.virtual_machines.get(region_id=[1, 2])
objects = nb.virtualization.virtual_machines.get(site_group=["SITE GROUP1"])
objects = nb.virtualization.virtual_machines.get(site_group_id=[1, 2])
objects = nb.virtualization.virtual_machines.get(site=["SITE1"])
objects = nb.virtualization.virtual_machines.get(site_id=[1, 2])

# Attributes
objects = nb.virtualization.virtual_machines.get(status=["active", "planned"])
objects = nb.virtualization.virtual_machines.get(role=["DEVICE ROLE1", "DEVICE ROLE2"])
objects = nb.virtualization.virtual_machines.get(role_id=[1, 2])
objects = nb.virtualization.virtual_machines.get(platform=["PLATFORM1", "PLATFORM2"])
objects = nb.virtualization.virtual_machines.get(platform_id=[1, 2])
objects = nb.virtualization.virtual_machines.get(mac_address=["000000000001"])
objects = nb.virtualization.virtual_machines.get(has_primary_ip=True)
objects = nb.virtualization.virtual_machines.get(local_context_data=True)

# Tenant
objects = nb.virtualization.virtual_machines.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.virtualization.virtual_machines.get(tenant_group_id=[1, 2])
objects = nb.virtualization.virtual_machines.get(tenant=["TENANT1", "TENANT2"])
objects = nb.virtualization.virtual_machines.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.virtualization.virtual_machines.get(id=[1, 2])
objects = nb.virtualization.virtual_machines.get(name=["VIRTUAL MACHINE1", "VIRTUAL MACHINE2"])
objects = nb.virtualization.virtual_machines.get(description=["DESCRIPTION1", "DESCRIPTION2"])
