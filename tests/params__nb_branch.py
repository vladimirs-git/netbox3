"""Params base.py."""
from copy import deepcopy

from netbox3.exceptions import NbBranchError

PREFIX = "10.0.0.0/24"
NAME = "name"
IP0 = "1.1.1.1"
IP32 = "1.1.1.1/32"

# ====================== universal get methods =======================

# test__dict
DICT = [
    (["a"], {"a": None}, True, NbBranchError),
    (["a"], {"a": None}, False, {}),
    (["a"], {"a": 1}, True, NbBranchError),
    (["a"], {"a": 1}, False, {}),
    (["a"], {"a": {}}, True, {}),
    (["a"], {"a": {}}, False, {}),
    (["a"], {"a": {"k": "A"}}, True, {"k": "A"}),
    (["a"], {"a": {"k": "A"}}, False, {"k": "A"}),
    (["a", "b"], {"a": {"b": {"k": "B"}}}, True, {"k": "B"}),
    (["a", "b"], {"a": {"b": {"k": "B"}}}, False, {"k": "B"}),
    (["a", "b", "c"], {"a": {"b": {"c": {"k": "C"}}}}, True, {"k": "C"}),
    (["a", "b", "c"], {"a": {"b": {"c": {"k": "C"}}}}, False, {"k": "C"}),
]

# test__int
INT = [
    (["id"], {"id": "1"}, True, 1),
    (["id"], {"id": "1"}, False, 1),
    (["id"], {"id": 0}, True, 0),
    (["id"], {"id": 0}, False, 0),
    (["id"], {"id": "0"}, True, 0),
    (["id"], {"id": "0"}, False, 0),
    (["a", "b"], {"a": {"b": 2}}, True, 2),
    (["a", "b"], {"a": {"b": 2}}, False, 2),
    (["a", "b"], {"a": {"b": None}}, True, NbBranchError),
    (["a", "b"], {"a": {"b": None}}, False, 0),
    (["a", "b"], {"a": {"b": "2"}}, True, 2),
    (["a", "b"], {"a": {"b": "2"}}, False, 2),
    (["a", "b", "c"], {"a": {"b": {"c": 3}}}, True, 3),
    (["a", "b", "c"], {"a": {"b": {"c": "3"}}}, True, 3),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbBranchError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, 0),
    (["id"], None, True, NbBranchError),
    (["id"], None, False, 0),
]

# test__list
LIST = [
    (["a"], {"a": None}, True, NbBranchError),
    (["a"], {"a": None}, False, []),
    (["a"], {"a": 1}, True, NbBranchError),
    (["a"], {"a": 1}, False, []),
    (["a"], {"a": ["A"]}, True, ["A"]),
    (["a"], {"a": ["A"]}, False, ["A"]),
    (["a"], {"a": [""]}, True, [""]),
    (["a"], {"a": [""]}, False, [""]),
    (["a", "b"], {"a": {"b": ["B"]}}, True, ["B"]),
    (["a", "b"], {"a": {"b": ["B"]}}, False, ["B"]),
    (["a", "b"], {"a": {"b": None}}, True, NbBranchError),
    (["a", "b"], {"a": {"b": None}}, False, []),
    (["a", "b", "c"], {"a": {"b": {"c": ["C"]}}}, True, ["C"]),
    (["a", "b", "c"], {"a": {"b": {"c": ["C"]}}}, False, ["C"]),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbBranchError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, []),
]

# test__str
STR = [
    (["a"], {"a": None}, True, NbBranchError),
    (["a"], {"a": None}, False, ""),
    (["a"], {"a": 1}, True, NbBranchError),
    (["a"], {"a": 1}, False, ""),
    (["a"], {"a": "A"}, True, "A"),
    (["a"], {"a": "A"}, False, "A"),
    (["a"], {"a": ""}, True, ""),
    (["a"], {"a": ""}, False, ""),
    (["a", "b"], {"a": {"b": "B"}}, True, "B"),
    (["a", "b"], {"a": {"b": "B"}}, False, "B"),
    (["a", "b"], {"a": {"b": None}}, True, NbBranchError),
    (["a", "b"], {"a": {"b": None}}, False, ""),
    (["a", "b", "c"], {"a": {"b": {"c": "C"}}}, True, "C"),
    (["a", "b", "c"], {"a": {"b": {"c": "C"}}}, False, "C"),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbBranchError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, ""),
]

# test__strict_dict
STRICT_DICT = [
    (["a"], {"a": {"k": "v"}}, True, {"k": "v"}),
    (["a"], {"a": {"k": "v"}}, False, {"k": "v"}),
    (["a"], {"a": 0}, True, NbBranchError),
    (["a"], {"a": 0}, False, NbBranchError),
    (["a"], {"url": "https://"}, True, NbBranchError),
    (["a"], {"url": "https://"}, False, NbBranchError),
]

# test__strict_int
STRICT_INT = [
    (["a"], {"a": 1}, True, 1),
    (["a"], {"a": 1}, False, 1),
    (["a"], {"a": 0}, True, NbBranchError),
    (["a"], {"a": 0}, False, NbBranchError),
    (["a"], {"url": "https://"}, True, NbBranchError),
    (["a"], {"url": "https://"}, False, NbBranchError),
]

# test__strict_list
STRICT_LIST = [
    (["a"], {"a": ["A"]}, True, ["A"]),
    (["a"], {"a": ["A"]}, False, ["A"]),
    (["a"], {"a": []}, True, NbBranchError),
    (["a"], {"a": []}, False, NbBranchError),
    (["a"], {"url": "https://"}, True, NbBranchError),
    (["a"], {"url": "https://"}, False, NbBranchError),
]

# test__strict_str
STRICT_STR = [
    (["a"], {"a": "A"}, True, "A"),
    (["a"], {"a": "A"}, False, "A"),
    (["a"], {"a": ""}, True, NbBranchError),
    (["a"], {"a": ""}, False, NbBranchError),
    (["a"], {"url": "https://"}, True, NbBranchError),
    (["a"], {"url": "https://"}, False, NbBranchError),
]

# ============================= methods ==============================

# test__id_
ID_ = [
    (["id"], {"id": "1"}, True, 1),
    (["id"], {"id": "1"}, False, 1),
    (["id"], {"id": 0}, True, 0),
    (["id"], {"id": 0}, False, 0),
    (["id"], {"id": "0"}, True, 0),
    (["id"], {"id": "0"}, False, 0),
    (["id"], None, True, NbBranchError),
    (["id"], None, False, 0),
]

# test__address
ADDRESS = [
    ({"address": PREFIX}, True, PREFIX),
    ({"address": PREFIX}, False, PREFIX),
    ({"address": "10.0.0.1"}, True, NbBranchError),
    ({"address": "10.0.0.1"}, False, "10.0.0.1"),
    ({"address": None}, True, NbBranchError),
    ({"address": None}, False, ""),
    ({"address": 1}, True, NbBranchError),
    ({"address": 1}, False, ""),
    (None, True, NbBranchError),
    (None, False, ""),
]

# test__group_name
GROUP_NAME = [
    ({"group": {"name": NAME}}, True, NAME),
    ({"group": {"name": NAME}}, False, NAME),
    ({"group": {"name": ""}}, True, NbBranchError),
    ({"group": {"name": ""}}, False, ""),
    ({"group": None}, True, NbBranchError),
    ({"group": None}, False, ""),
    (None, True, NbBranchError),
    (None, False, ""),
]

# test__name
NAME_ = [
    ({"name": NAME}, True, NAME),
    ({"name": NAME}, False, NAME),
    ({"name": ""}, True, NbBranchError),
    ({"name": ""}, False, ""),
    (None, True, NbBranchError),
    (None, False, ""),
]

# test__assigned_device
ASSIGNED_DEVICE = [
    ({"assigned_object": {"device": {"name": NAME}}}, True, NAME),
    ({"assigned_object": {"device": {"name": NAME}}}, False, NAME),
    ({"assigned_object": {"device": None}}, True, NbBranchError),
    ({"assigned_object": {"device": None}}, False, ""),
    ({"assigned_object": None}, True, NbBranchError),
    ({"assigned_object": None}, False, ""),
    (None, True, NbBranchError),
    (None, False, ""),
]

# test__address
PREFIX_ = [
    ({"prefix": PREFIX}, True, PREFIX),
    ({"prefix": PREFIX}, False, PREFIX),
    ({"prefix": "10.0.0.0"}, True, NbBranchError),
    ({"prefix": "10.0.0.0"}, False, "10.0.0.0"),
    ({"prefix": None}, True, NbBranchError),
    ({"prefix": None}, False, ""),
    (None, True, NbBranchError),
    (None, False, ""),
]

# test__primary_ip4_address
PRIMARY_IP4 = [
    ({"primary_ip4": {"address": IP32}}, True, IP32),
    ({"primary_ip4": {"address": IP32}}, False, IP32),
    ({"primary_ip4": {"address": IP0}}, True, IP0),
    ({"primary_ip4": {"address": IP0}}, False, IP0),
    ({"primary_ip4": {"address": f"{IP0}_32"}}, True, NbBranchError),
    ({"primary_ip4": {"address": f"{IP0}_32"}}, False, f"{IP0}_32"),
    ({"primary_ip4": {"address": ""}}, True, NbBranchError),
    ({"primary_ip4": {"address": ""}}, False, ""),
    ({"primary_ip4": {"address": None}}, True, NbBranchError),
    ({"primary_ip4": {"address": None}}, False, ""),
    ({"primary_ip4": None}, True, NbBranchError),
    ({"primary_ip4": None}, False, ""),
]

# test__site_name
SITE_NAME = [
    ({"site": {"name": NAME}}, True, True, NAME.upper()),
    ({"site": {"name": NAME}}, True, False, NAME.lower()),
    ({"site": {"name": NAME}}, False, True, NAME.upper()),
    ({"site": {"name": NAME}}, False, False, NAME.lower()),
    ({"site": {"name": ""}}, True, True, NbBranchError),
    ({"site": {"name": ""}}, True, False, NbBranchError),
    ({"site": {"name": ""}}, False, True, ""),
    ({"site": {"name": ""}}, False, False, ""),
    ({"site": None}, True, False, NbBranchError),
    ({"site": None}, False, False, ""),
    (None, True, False, NbBranchError),
    (None, False, False, ""),
]

# test__vid
GET_VID = [
    ({"vid": "1"}, True, 1),
    ({"vid": "1"}, False, 1),
    ({"vid": 0}, True, 0),
    ({"vid": 0}, False, 0),
    ({"vid": "0"}, True, 0),
    ({"vid": "0"}, False, 0),
    (None, True, NbBranchError),
    (None, False, 0),
]

# test__vlan
GET_VLAN = [
    ({"vlan": {"vid": 1}}, True, 1),
    ({"vlan": {"vid": 1}}, False, 1),
    ({"vlan": {"vid": "1"}}, True, 1),
    ({"vlan": {"vid": "1"}}, False, 1),
    ({"vlan": {"vid": 0}}, True, 0),
    ({"vlan": {"vid": 0}}, False, 0),
    ({"vlan": {"vid": "0"}}, True, 0),
    ({"vlan": {"vid": "0"}}, False, 0),
    ({"vlan": {"vid": None}}, True, NbBranchError),
    ({"vlan": {"vid": None}}, False, 0),
    ({"vlan": None}, True, NbBranchError),
    ({"vlan": None}, False, 0),
    (None, True, NbBranchError),
    (None, False, 0),
]

# test__tags
TAGS = [
    ({"tags": [{"slug": NAME}, {"slug": "tag2"}]}, True, [NAME, "tag2"]),
    ({"tags": [{"slug": NAME}, {"slug": "tag2"}]}, False, [NAME, "tag2"]),
    ({"tags": [{"slug": None}]}, True, NbBranchError),
    ({"tags": [{"slug": None}]}, False, []),
    ({"tags": [None]}, True, NbBranchError),
    ({"tags": [None]}, False, []),
    ({"tags": []}, True, []),
    ({"tags": []}, False, []),
    ({"tags": None}, True, NbBranchError),
    ({"tags": None}, False, []),
    (None, True, NbBranchError),
    (None, False, []),
]

# test__url
URL = [
    ({"url": NAME}, True, NAME),
    ({"url": NAME}, False, NAME),
    ({"url": ""}, True, NbBranchError),
    ({"url": ""}, False, ""),
    (None, True, NbBranchError),
    (None, False, ""),
]

# test__platform_slug
PLATFORM_D = {
    "url": "/api/dcim/devices/",
    "primary_ip4": {"address": "10.0.0.1/24"},
    "platform": {"slug": "platform1"},
}
PLATFORM_D_WO_URL = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_URL["url"]
PLATFORM_D_W_INVALID_ADDRESS = deepcopy(PLATFORM_D)
PLATFORM_D_W_INVALID_ADDRESS["primary_ip4"]["address"] = "typo"
PLATFORM_D_WO_ADDRESS = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_ADDRESS["primary_ip4"]["address"]
PLATFORM_D_WO_PRIMARY_IP4 = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_PRIMARY_IP4["primary_ip4"]
PLATFORM_D_WO_SLUG = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_SLUG["platform"]["slug"]
PLATFORM_D_WO_PLATFORM = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_PLATFORM["platform"]

PLATFORM_SLUG = [
    (PLATFORM_D, "platform1"),
    ({}, NbBranchError),
    (PLATFORM_D_WO_URL, NbBranchError),
    (PLATFORM_D_W_INVALID_ADDRESS, NbBranchError),
    (PLATFORM_D_WO_ADDRESS, NbBranchError),
    (PLATFORM_D_WO_PRIMARY_IP4, NbBranchError),
    (PLATFORM_D_WO_SLUG, NbBranchError),
    (PLATFORM_D_WO_PLATFORM, NbBranchError),
]

# test__hosts_in_cf_firewalls
NAME1 = "a-b-c-d"
NAME2 = "A-B-C-D"
HOSTS_IN_CF_FIREWALLS = [
    ({"custom_fields": {"firewalls": f"{NAME1} {NAME2}"}}, True, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": f"{NAME1},{NAME2}"}}, True, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": f"{NAME1}, {NAME2}"}}, True, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": f"{NAME1}, {NAME2}"}}, False, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": ""}}, True, set()),
    ({"custom_fields": {"firewalls": ""}}, False, set()),
    ({"custom_fields": None}, True, set()),
    ({"custom_fields": None}, False, set()),
    (None, True, set()),
    (None, False, set()),
]

# test__hosts_in_aggr_descr
TAG = "noc_aggregates_belonging"
HOSTS_IN_AGGR_DESCR = [
    ({"description": f"\t{NAME1},{NAME2} a", "tags": [{"slug": TAG}]}, True, {NAME1, NAME2}),
    ({"description": f"a:{NAME1}, {NAME2}.a", "tags": [{"slug": TAG}]}, True, {NAME1, NAME2}),
    ({"description": f"{NAME1} {NAME2} a", "tags": [{"slug": TAG}]}, True, {NAME1, NAME2}),
    ({"description": f"{NAME1} {NAME2} a", "tags": [{"slug": TAG}]}, False, {NAME1, NAME2}),
    ({"description": "a", "tags": [{"slug": TAG}]}, True, set()),
    ({"description": "a", "tags": [{"slug": TAG}]}, False, set()),
    ({"description": "", "tags": [{"slug": TAG}]}, True, set()),
    ({"description": "", "tags": [{"slug": TAG}]}, False, set()),
    ({"description": "", "tags": [None]}, True, NbBranchError),
    ({"description": "", "tags": [None]}, False, set()),
]

# test__firewalls__in_aggregate
TAG = "noc_aggregates_belonging"
FIREWALLS__IN_AGGREGATE = [
    ({"custom_fields": {"firewalls": NAME1}}, True, {NAME1}),
    ({"description": NAME1, "tags": [{"slug": TAG}]}, True, {NAME1}),
    (
        {"custom_fields": {"firewalls": NAME1}, "description": NAME2, "tags": [{"slug": TAG}]},
        True,
        {NAME1},
    ),
    (
        {"custom_fields": {"firewalls": "a"}, "description": "a", "tags": [{"slug": TAG}]},
        True,
        set(),
    ),
]

# test__is_ipam
IS_IPAM = [
    ({"url": "/api/ipam/prefixes/"}, True, "prefixes", True),
    ({"url": "/api/ipam/prefixes/"}, False, "prefixes", True),
    ({"url": "/api/ipam/prefixes/"}, True, "aggregates", False),
    ({"url": "/api/ipam/prefixes/"}, False, "aggregates", False),
    ({"url": "/api/ipam/aggregates/"}, True, "aggregates", True),
    ({"url": "/api/ipam/aggregates/"}, False, "aggregates", True),
    ({"url": "/api/ipam/ip-addresses/"}, True, "ip-addresses", True),
    ({"url": "/api/ipam/ip-addresses/"}, False, "ip-addresses", True),
    ({"url": None}, True, "prefixes", NbBranchError),
    ({"url": None}, False, "prefixes", False),
]

# test__is_dcim
IS_DCIM = [
    ({"url": "/api/dcim/devices/"}, True, "devices", True),
    ({"url": "/api/dcim/devices/"}, False, "devices", True),
    ({"url": "/api/dcim/devices/"}, True, "aggregates", False),
    ({"url": "/api/dcim/devices/"}, False, "aggregates", False),
    ({"url": None}, True, "devices", NbBranchError),
    ({"url": None}, False, "devices", False),
]

# test__is_vrf
IS_VRF = [
    ({"vrf": NAME}, True, True),
    ({"vrf": NAME}, False, True),
    ({"vrf": ""}, True, False),
    ({"vrf": ""}, False, False),
]

# test__is_prefix
IS_PREFIX = [
    (PREFIX, True),
    (IP32, True),
    (IP0, False),
    ("", False),
]
