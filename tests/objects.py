"""Test helpers data."""
from copy import deepcopy

from netbox3.nb_tree import (
    TenancyM,
    IpamM,
    DcimM,
    CircuitsM,
    NbTree,
    ExtrasM,
    VirtualizationM,
    WirelessM,
)
from netbox3.types_ import DAny, DiDAny, LInt

# circuits
CIRCUIT_TYPE1: DAny = {
    "url": "/api/circuits/circuit-types/1",
    "id": 1,
    "name": "CIRCUIT TYPE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "circuit-type1",
}
CIRCUIT1: DAny = {
    "url": "/api/circuits/circuits/1",
    "id": 1,
    "cid": "CID1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "provider": {"id": 1, "name": "PROVIDER1", "url": "/api/circuits/providers/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "type": {"id": 1, "name": "WAN", "url": "/api/circuits/circuit-types/1"},
    "termination_a": {
        "id": 1,
        "url": "/api/circuits/circuit-terminations/1",
        "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    },
    "termination_z": {
        "id": 2,
        "url": "/api/circuits/circuit-terminations/2",
        "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    },
}
PROVIDER1: DAny = {
    "url": "/api/circuits/providers/1",
    "id": 1,
    "name": "PROVIDER1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "provider1",
    "asns": {"id": 1, "asn": 65001, "url": "/api/ipam/asns/1"},
}
PROVIDER_ACCOUNT1: DAny = {
    "url": "/api/circuits/provider-accounts/1",
    "id": 1,
    "name": "PROVIDER ACCOUNT1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "provider": {"id": 1, "name": "PROVIDER1", "url": "/api/circuits/providers/1"},
}
PROVIDER_NETWORK1: DAny = {
    "url": "/api/circuits/provider-networks/1",
    "id": 1,
    "name": "PROVIDER NETWORK1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "provider": {"id": 1, "name": "PROVIDER1", "url": "/api/circuits/providers/1"},
}
TERMINATION1: DAny = {
    "url": "/api/circuits/circuit-terminations/1",
    "id": 1,
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "circuit": {"id": 1, "cid": "CID1", "url": "/api/circuits/circuits/1"},
    "term_side": "A",
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "link_peers_type": "dcim.interface",
    "link_peers": [
        {
            "id": 1,
            "url": "/api/dcim/interfaces/1/",
            "name": "Ethernet1/1",
            "device": {"id": 1, "name": "DEVICE1", "url": "/api/dcim/devices/1"},
        },
    ],
}
TERMINATION2: DAny = {
    "url": "/api/circuits/circuit-terminations/2",
    "id": 2,
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "circuit": {"id": 1, "cid": "CID1", "url": "/api/circuits/circuits/1"},
    "term_side": "Z",
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "link_peers_type": "dcim.interface",
    "link_peers": [
        {
            "id": 2,
            "url": "/api/dcim/interfaces/2/",
            "name": "Ethernet2/2",
            "device": {"id": 2, "name": "DEVICE2", "url": "/api/dcim/devices/2"},
        },
    ],
}
TENANT_GROUP1: DAny = {
    "url": "/api/tenancy/tenant-groups/1",
    "id": 1,
    "name": "TENANT GROUP1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "tenant-group1",
    "parent": None,
}

# dcim
DEVICE_ROLE1: DAny = {
    "url": "/api/dcim/device-roles/1",
    "id": 1,
    "name": "DEVICE ROLE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "device-role1",
}
DEVICE_TYPE1: DAny = {
    "url": "/api/dcim/device-types/1",
    "id": 1,
    "name": "MODEL1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "model1",
    "manufacturer": {"id": 1, "name": "MANUFACTURER1", "url": "/api/dcim/manufacturers/1"},
}
MANUFACTURER1: DAny = {
    "url": "/api/dcim/manufacturers/1",
    "id": 1,
    "name": "MANUFACTURER1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "manufacturer1",
}
PLATFORM1: DAny = {
    "url": "/api/dcim/platforms/1",
    "id": 1,
    "name": "PLATFORM1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "platform1",
}
DEVICE1: DAny = {
    "url": "/api/dcim/devices/1",
    "id": 1,
    "name": "DEVICE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "primary_ip4": {"address": "10.1.1.1/24"},
    "serial": "SERIAL1",
    "device_role": {"id": 1, "name": "DEVICE ROLE1", "url": "/api/dcim/device-roles/1"},
    "device_type": {"id": 1, "name": "MODEL1", "url": "/api/dcim/device-types/1"},
    "location": {"id": 1, "name": "LOCATION1", "url": "/api/dcim/locations/1"},
    "platform": {"id": 1, "name": "PLATFORM1", "url": "/api/dcim/platforms/1"},
    "rack": {"id": 1, "name": "RACK1", "url": "/api/dcim/racks/1"},
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
DEVICE2: DAny = {
    "url": "/api/dcim/devices/2",
    "id": 2,
    "name": "DEVICE2",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "primary_ip4": {"address": "10.2.2.2/24"},
    "serial": "SERIAL2",
    "device_role": {"id": 1, "name": "DEVICE ROLE1", "url": "/api/dcim/device-roles/1"},
    "device_type": {"id": 1, "name": "MODEL1", "url": "/api/dcim/device-types/1"},
    "location": {"id": 1, "name": "LOCATION1", "url": "/api/dcim/locations/1"},
    "platform": {"id": 1, "name": "PLATFORM1", "url": "/api/dcim/platforms/1"},
    "rack": {"id": 1, "name": "RACK1", "url": "/api/dcim/racks/1"},
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
INTERFACE1: DAny = {
    "url": "/api/dcim/interfaces/1",
    "id": 1,
    "name": "GigabitEthernet1/0/1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "device": {"id": 1, "name": "DEVICE1", "url": "/api/dcim/devices/1"},
    "vdcs": [],
    "module": None,
    "label": "LABEL1",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:01",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION1",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": {"id": 1, "vid": 1, "name": "VLAN1", "url": "/api/ipam/vlans/1"},
    "tagged_vlans": [{"id": 2, "vid": 2, "name": "VLAN2", "url": "/api/ipam/vlans/2"}],
    "mark_connected": True,
    "cable": None,
    "cable_end": "",
    "wireless_link": None,
    "link_peers": [],
    "link_peers_type": None,
    "wireless_lans": [],
    "vrf": {"id": 1, "name": "VRF1", "url": "/api/ipam/vrfs/1"},
    "l2vpn_termination": None,
    "connected_endpoints": None,
    "connected_endpoints_type": None,
    "connected_endpoints_reachable": None,
    "custom_fields": {},
}
INTERFACE2: DAny = {
    "url": "/api/dcim/interfaces/2",
    "id": 2,
    "name": "GigabitEthernet1/0/1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "device": {"id": 1, "name": "DEVICE1", "url": "/api/dcim/devices/1"},
    "vdcs": [],
    "module": None,
    "label": "LABEL2",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:02",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION2",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": {"id": 1, "vid": 1, "name": "VLAN1", "url": "/api/ipam/vlans/1"},
    "tagged_vlans": [{"id": 2, "vid": 2, "name": "VLAN2", "url": "/api/ipam/vlans/2"}],
    "mark_connected": True,
    "cable": None,
    "cable_end": "",
    "wireless_link": None,
    "link_peers": [],
    "link_peers_type": None,
    "wireless_lans": [],
    "vrf": {"id": 1, "name": "VRF1", "url": "/api/ipam/vrfs/1"},
    "l2vpn_termination": None,
    "connected_endpoints": None,
    "connected_endpoints_type": None,
    "connected_endpoints_reachable": None,
    "custom_fields": {},
}
LOCATION1: DAny = {
    "url": "/api/dcim/locations/1",
    "id": 1,
    "name": "LOCATION1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "parent": None,
    "slug": "location1",
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
RACK_ROLE1: DAny = {
    "url": "/api/dcim/rack-roles/1",
    "id": 1,
    "name": "RACK ROLE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "rack-role1",
}
RACK1: DAny = {
    "url": "/api/dcim/racks/1",
    "id": 1,
    "name": "RACK1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "location": {"id": 1, "name": "LOCATION1", "url": "/api/dcim/locations/1"},
    "role": {"id": 1, "name": "RACK ROLE1", "url": "/api/dcim/rack-roles/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "tenant_group": {"id": 1, "name": "TENANT GROUP1", "url": "/api/tenancy/tenant-groups/1"},
}
REGION1: DAny = {
    "url": "/api/dcim/regions/1",
    "id": 1,
    "name": "REGION1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "parent": None,
    "slug": "region1",
}
SITE_GROUP1: DAny = {
    "url": "/api/dcim/site-groups/1",
    "id": 1,
    "name": "SITE GROUP1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "parent": None,
    "slug": "site-group1",
}
SITE1: DAny = {
    "url": "/api/dcim/sites/1",
    "id": 1,
    "name": "SITE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "group": {"id": 1, "name": "SITE GROUP1", "url": "/api/dcim/site-groups/1"},
    "region": {"id": 1, "name": "REGION1", "url": "/api/dcim/regions/1"},
    "slug": "site1",
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "asns": {"id": 1, "asn": 65001, "url": "/api/ipam/asns/1"},
}

# extras
TAG1: DAny = {
    "url": "/api/extras/tags/1",
    "id": 1,
    "name": "TAG1",
    "slug": "tag1",
    "color": "aa1409",
}
# ipam
AGGREGATE1: DAny = {
    "url": "/api/ipam/aggregates/1",
    "id": 1,
    "prefix": "10.0.0.0/16",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "family": {"value": 4},
    "rir": {"id": 1, "name": "RFC 1918", "url": "/api/ipam/rirs/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
ASN_RANGE1: DAny = {
    "url": "/api/ipam/asn-ranges/1",
    "id": 1,
    "name": "ASN RANGE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "asn-range1",
    "rir": {"id": 2, "name": "RFC 6996", "url": "/api/ipam/rirs/2"},
    "start": 65001,
    "end": 65002,
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
ASN1: DAny = {
    "url": "/api/ipam/asns/1",
    "id": 1,
    "asn": 65001,
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "rir": {"id": 2, "name": "RFC 6996", "url": "/api/ipam/rirs/2"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
ASN2: DAny = {
    "url": "/api/ipam/asns/2",
    "id": 2,
    "asn": 65002,
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "rir": {"id": 2, "name": "RFC 6996", "url": "/api/ipam/rirs/2"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
IP_ADDRESS1: DAny = {  # private
    "url": "/api/ipam/ip-addresses/1",
    "id": 1,
    "address": "10.0.0.1/24",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "nat_inside": None,
    "nat_outside": [{"id": 2, "address": "1.0.0.1/24"}],
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "vrf": {"id": 1, "name": "VRF1", "url": "/api/ipam/vrfs/1"},
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": 1,
    "assigned_object": {
        "id": 1,
        "url": "/api/dcim/interfaces/1",
        "name": "GigabitEthernet1/0/1",
        "cable": 1,
        "device": {
            "id": 1,
            "url": "/api/dcim/devices/1",
            "name": "DEVICE1",
        },
    },
}
IP_ADDRESS2: DAny = {  # public
    "url": "/api/ipam/ip-addresses/2",
    "id": 2,
    "address": "1.0.0.1/24",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "nat_inside": {"id": 1, "address": "10.0.0.1/24", "url": "/api/ipam/ip-addresses/1"},
    "nat_outside": [],
    "tenant": None,
    "vrf": None,
    "assigned_object": None,
}
PREFIX1: DAny = {
    "url": "/api/ipam/prefixes/1",
    "id": 1,
    "prefix": "10.0.0.0/24",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "role": {"id": 1, "name": "ROLE1", "url": "/api/ipam/prefixes/1"},
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "vlan": {"id": 1, "vid": 1, "name": "VLAN1", "url": "/api/ipam/vlans/1"},
    "vrf": {"id": 1, "name": "VRF1", "url": "/api/ipam/vrfs/1"},
}
RIR1: DAny = {
    "url": "/api/ipam/rirs/1",
    "id": 1,
    "name": "RFC 1918",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "rfc-1918",
}
RIR2: DAny = {
    "url": "/api/ipam/rirs/2",
    "id": 2,
    "name": "RFC 6996",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "rfc-6996",
}
ROLE1: DAny = {
    "url": "/api/ipam/roles/1",
    "id": 1,
    "name": "ROLE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "role1",
}
ROUTE_TARGET1: DAny = {
    "url": "/api/ipam/route-targets/1",
    "id": 1,
    "name": "65000:1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
VLAN_GROUP1: DAny = {
    "url": "/api/ipam/vlan-groups/1",
    "id": 1,
    "name": "VLAN GROUP1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "vlan-group1",
    "scope_type": "dcim.site",
    "scope_id": 1,
    "scope": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "min_vid": 1,
    "max_vid": 4094,
}
VLAN1: DAny = {
    "url": "/api/ipam/vlans/1",
    "id": 1,
    "vid": 1,
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "site": None,  # mutually exclusive: group, site
    "group": {"id": 1, "name": "VLAN GROUP1", "url": "/api/ipam/vlan-groups/1"},
    "role": {"id": 1, "name": "ROLE1", "url": "/api/ipam/prefixes/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
VLAN2: DAny = {
    "url": "/api/ipam/vlans/2",
    "id": 2,
    "vid": 2,
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "group": None,  # mutually exclusive: group, site
    "role": {"id": 1, "name": "ROLE1", "url": "/api/ipam/prefixes/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
}
VRF1: DAny = {
    "url": "/api/ipam/vrfs/1",
    "id": 1,
    "name": "VRF1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "import_targets": [{"id": 1, "name": "65000:1"}],
    "export_targets": [{"id": 1, "name": "65000:1"}],
}

# tenancy
TENANT1: DAny = {
    "url": "/api/tenancy/tenants/1",
    "id": 1,
    "name": "TENANT1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "tenant1",
    "group": {"id": 1, "name": "TENANT GROUP1", "url": "/api/tenancy/tenant-groups/1"},
}

# virtualization
CLUSTER_GROUP1: DAny = {
    "url": "/api/virtualization/cluster-groups/1",
    "id": 1,
    "name": "CLUSTER GROUP1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "cluster-group1",
}
CLUSTER_TYPE1: DAny = {
    "url": "/api/virtualization/cluster-types/1",
    "id": 1,
    "name": "CLUSTER TYPE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "cluster-type1",
}
CLUSTER1: DAny = {
    "url": "/api/virtualization/clusters/1",
    "id": 1,
    "name": "CLUSTER1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "slug": "cluster1",
    "type": {"id": 1, "name": "CLUSTER TYPE1", "url": "/api/virtualization/cluster-types/1"},
    "group": {"id": 1, "name": "CLUSTER GROUP1", "url": "/api/virtualization/cluster-groups/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
}
VIRTUAL_INTERFACE1: DAny = {
    "url": "/api/virtualization/interfaces/1",
    "id": 1,
    "name": "INTERFACE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "virtual_machine": {
        "id": 1,
        "name": "VIRTUAL MACHINE1",
        "url": "/api/virtualization/virtual_machines/1",
    },
    "enabled": True,
    "parent": {"id": 1, "name": "INTERFACE1", "url": "/api/virtualization/interfaces/1"},
    "bridge": {"id": 1, "name": "INTERFACE1", "url": "/api/virtualization/interfaces/1"},
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:01",
    "description": "DESCRIPTION1",
    "mode": {"value": "tagged", "label": "Tagged"},
    "untagged_vlan": {"id": 1, "vid": 1, "name": "VLAN1", "url": "/api/ipam/vlans/1"},
    "tagged_vlans": [{"id": 2, "vid": 2, "name": "VLAN2", "url": "/api/ipam/vlans/2"}],
    "vrf": {"id": 1, "name": "VRF1", "url": "/api/ipam/vrfs/1"},
    "l2vpn_termination": None,
    "custom_fields": {},
}
VIRTUAL_MACHINE1: DAny = {
    "url": "/api/virtualization/virtual_machines/1",
    "id": 1,
    "name": "VIRTUAL MACHINE1",
    "tags": [{"id": 1, "name": "TAG1", "url": "/api/extras/tags/1"}],
    "site": {"id": 1, "name": "SITE1", "url": "/api/dcim/sites/1"},
    "cluster": {"id": 1, "name": "CLUSTER1", "url": "/api/virtualization/clusters/1"},
    "device": {"id": 1, "name": "DEVICE1", "url": "/api/dcim/devices/1"},
    "role": {"id": 1, "name": "DEVICE ROLE1", "url": "/api/dcim/device-roles/1"},
    "tenant": {"id": 1, "name": "TENANT1", "url": "/api/tenancy/tenants/1"},
    "platform": {"id": 1, "name": "PLATFORM1", "url": "/api/dcim/platforms/1"},
}


def full_tree() -> NbTree:
    """Init tree with data, ready for tests."""
    tree = NbTree(
        circuits=CircuitsM(
            circuit_terminations={int(d["id"]): d for d in [TERMINATION1, TERMINATION2]},
            circuit_types={d["id"]: d for d in [CIRCUIT_TYPE1]},
            circuits={d["id"]: d for d in [CIRCUIT1]},
            provider_accounts={d["id"]: d for d in [PROVIDER_ACCOUNT1]},
            provider_networks={d["id"]: d for d in [PROVIDER_NETWORK1]},
            providers={d["id"]: d for d in [PROVIDER1]},
        ),
        dcim=DcimM(
            cable_terminations={},
            cables={},
            # connected_device, is not model
            console_port_templates={},
            console_ports={},
            console_server_port_templates={},
            console_server_ports={},
            device_bay_templates={},
            device_bays={},
            device_roles={d["id"]: d for d in [DEVICE_ROLE1]},
            device_types={d["id"]: d for d in [DEVICE_TYPE1]},
            devices={d["id"]: d for d in [DEVICE1, DEVICE2]},
            front_port_templates={},
            front_ports={},
            interface_templates={},
            interfaces={d["id"]: d for d in [INTERFACE1, INTERFACE2]},
            inventory_item_roles={},
            inventory_item_templates={},
            inventory_items={},
            locations={d["id"]: d for d in [LOCATION1]},
            manufacturers={d["id"]: d for d in [MANUFACTURER1]},
            module_bay_templates={},
            module_bays={},
            module_types={},
            modules={},
            platforms={d["id"]: d for d in [PLATFORM1]},
            power_feeds={},
            power_outlet_templates={},
            power_outlets={},
            power_panels={},
            power_port_templates={},
            power_ports={},
            rack_reservations={},
            rack_roles={d["id"]: d for d in [RACK_ROLE1]},
            racks={d["id"]: d for d in [RACK1]},
            rear_port_templates={},
            rear_ports={},
            regions={d["id"]: d for d in [REGION1]},
            site_groups={d["id"]: d for d in [SITE_GROUP1]},
            sites={d["id"]: d for d in [SITE1]},
            virtual_chassis={},
            virtual_device_contexts={},
        ),
        extras=ExtrasM(
            bookmarks={},
            config_contexts={},
            config_templates={},
            content_types={},
            custom_field_choice_sets={},
            custom_fields={},
            custom_links={},
            export_templates={},
            image_attachments={},
            journal_entries={},
            object_changes={},
            reports={},
            saved_filters={},
            scripts={},
            tags={d["id"]: d for d in [TAG1]},
            webhooks={},
        ),
        ipam=IpamM(
            aggregates={d["id"]: d for d in [AGGREGATE1]},
            asn_ranges={d["id"]: d for d in [ASN_RANGE1]},
            asns={d["id"]: d for d in [ASN1, ASN2]},
            fhrp_group_assignments={},
            fhrp_groups={},
            ip_addresses={d["id"]: d for d in [IP_ADDRESS1, IP_ADDRESS2]},
            ip_ranges={},
            l2vpn_terminations={},
            l2vpns={},
            prefixes={d["id"]: d for d in [PREFIX1]},
            rirs={d["id"]: d for d in [RIR1, RIR2]},
            roles={d["id"]: d for d in [ROLE1]},
            route_targets={d["id"]: d for d in [ROUTE_TARGET1]},
            service_templates={},
            services={},
            vlan_groups={d["id"]: d for d in [VLAN_GROUP1]},
            vlans={d["id"]: d for d in [VLAN1, VLAN2]},
            vrfs={d["id"]: d for d in [VRF1]},
        ),
        tenancy=TenancyM(
            contact_assignments={},
            contact_groups={},
            contact_roles={},
            contacts={},
            tenant_groups={d["id"]: d for d in [TENANT_GROUP1]},
            tenants={d["id"]: d for d in [TENANT1]},
        ),
        virtualization=VirtualizationM(
            cluster_groups={d["id"]: d for d in [CLUSTER_GROUP1]},
            cluster_types={d["id"]: d for d in [CLUSTER_TYPE1]},
            clusters={d["id"]: d for d in [CLUSTER1]},
            interfaces={d["id"]: d for d in [VIRTUAL_INTERFACE1]},
            virtual_machines={d["id"]: d for d in [VIRTUAL_MACHINE1]},
        ),
        wireless=WirelessM(
            wireless_lan_groups={},
            wireless_lans={},
            wireless_links={},
        ),
    )
    return tree


def vrf_d(ids: LInt) -> DiDAny:
    """Init simple Netbox ipam vrf object."""
    data = {}
    for id_ in ids:
        vrf = deepcopy(VRF1)
        vrf["id"] = id_
        data[id_] = vrf
    return data
