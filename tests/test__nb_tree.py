# pylint: disable=E0237,E1101,W0212

"""Unittests nb_tree.py."""
from typing import Any

import pytest

from netbox3 import nb_tree
from netbox3.nb_tree import NbTree
from tests import objects


def test__insert_tree():
    """models.tree.insert_tree()"""
    src = NbTree()
    src.ipam.vrfs.update(objects.vrf_d([1]))
    dst = NbTree()

    nb_tree.insert_tree(src=src, dst=dst)
    assert src.ipam.vrfs[1]["id"] == 1
    assert dst.ipam.vrfs[1]["id"] == 1

    src.ipam.vrfs[1]["id"] = 2
    assert src.ipam.vrfs[1]["id"] == 2
    assert dst.ipam.vrfs[1]["id"] == 2


def test__count():
    """NbTree.count()"""
    tree = NbTree()
    tree.circuits.circuit_terminations.update({1: {}})
    tree.circuits.circuit_types.update({1: {}})
    tree.dcim.device_roles.update({1: {}})
    tree.dcim.device_types.update({1: {}, 2: {}})
    tree.ipam.aggregates.update({1: {}})
    tree.ipam.asn_ranges.update({1: {}, 2: {}, 3: {}})
    tree.tenancy.tenant_groups.update({1: {}})
    tree.tenancy.tenants.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert tree.circuits.count() == 2
    assert tree.dcim.count() == 3
    assert tree.ipam.count() == 4
    assert tree.tenancy.count() == 5
    assert tree.count() == 14


def test__apps():
    """NbTree.apps()"""
    tree = NbTree()
    actual = tree.apps()
    expected = [
        "circuits",
        "core",
        "dcim",
        "extras",
        "ipam",
        "tenancy",
        "users",
        "virtualization",
        "wireless",
    ]
    assert actual == expected


def test__models():
    """NbTree.models()"""
    tree = NbTree()
    actual = tree.circuits.models()
    expected = [
        "circuit_terminations",
        "circuit_types",
        "circuits",
        "provider_accounts",
        "provider_networks",
        "providers",
    ]
    assert actual == expected


@pytest.mark.parametrize("child, expected, exp_object", [
    # url
    ({"url": "/dcim/cables/1"}, 1, None),
    ({"url": "/circuits/circuit-terminations/1"}, 1, None),
    ({"url": "/circuits/circuit-terminations/1/"}, 1, None),
    ({"url": "/"}, AttributeError, None),
    ({"url": "/typo/ip_addresses/1"}, AttributeError, None),
    ({"url": "/ipam/typo/1"}, AttributeError, None),
    ({"url": "/ipam/1"}, AttributeError, None),
    ({"url": "/ipam/ip_addresses/typo"}, ValueError, None),
    ({"id": 9, "url": "/ipam/ip_addresses/9"}, None, None),
    ({"id": 9, "url": ""}, None, None),
    ({"id": 9}, None, None),
    # object
    ({"object_id": 1, "object": {"url": "/dcim/cables/1"}}, None, 1),
    ({"object_id": 1, "object": "typo"}, None, None),
])
def test__get_child(child: Any, expected: Any, exp_object):
    """nb_tree._get_child() for dict"""
    tree = objects.full_tree()
    if isinstance(exp_object, int):
        assert child["object"].get("id") is None

    if isinstance(expected, (int, type(None))):
        child_full = nb_tree._get_child(child=child, tree=tree)
        actual = child_full.get("id")
        assert actual == expected

        if isinstance(exp_object, int):
            actual = child["object"].get("id")
            assert actual == exp_object

    else:
        with pytest.raises(expected):
            nb_tree._get_child(child=child, tree=tree)


# noinspection DuplicatedCode
def test__grow_tree__usual():
    """nb_tree.grow_tree() usual dependency"""
    # set up simplified objects
    root = NbTree()
    circuit = {k: v for k, v in objects.CIRCUIT1.items() if k in ["id", "url", "cid", "tenant"]}
    root.circuits.circuits = {d["id"]: d for d in [circuit]}
    tenant = {k: v for k, v in objects.TENANT1.items() if k in ["id", "url", "name", "tags"]}
    root.tenancy.tenants = {d["id"]: d for d in [tenant]}
    tag = {k: v for k, v in objects.TAG1.items() if k in ["id", "url", "name", "color"]}
    root.extras.tags = {d["id"]: d for d in [tag]}

    tree = nb_tree.grow_tree(tree=root)

    assert tree.circuits.circuits[1]["tenant"]["tags"][0]["color"] == "aa1409"
    assert tree.tenancy.tenants[1]["tags"][0]["color"] == "aa1409"
    assert root.circuits.circuits[1]["tenant"].get("tags") is None
    assert root.tenancy.tenants[1]["tags"][0].get("color") is None


# noinspection DuplicatedCode
def test__grow_tree__cable():
    """nb_tree.grow_tree() cable dependency"""
    # set up simplified objects
    root = NbTree()
    cable = {k: v for k, v in objects.CABLE2.items() if k in
             ["id", "url", "display", "a_terminations"]}
    root.dcim.cables = {d["id"]: d for d in [cable]}
    interface = {k: v for k, v in objects.INTERFACE2.items() if
                 k in ["id", "url", "device", "cable", "link_peers", "link_peers_type"]}
    root.dcim.interfaces = {d["id"]: d for d in [interface]}
    device = {k: v for k, v in objects.DEVICE1.items() if k in ["id", "url", "name", "tags"]}
    root.dcim.devices = {d["id"]: d for d in [device]}
    tag = {k: v for k, v in objects.TAG1.items() if k in ["id", "url", "color"]}
    root.extras.tags = {d["id"]: d for d in [tag]}

    tree = nb_tree.grow_tree(tree=root)

    # cable
    cable = tree.dcim.cables[2]
    assert cable["a_terminations"][0]["object_id"] == 2
    assert cable["a_terminations"][0]["object_type"] == "dcim.interface"
    assert cable["a_terminations"][0]["object"]["cable"]["display"] == "#2"
    # interface
    interface = tree.dcim.interfaces[2]
    assert interface["device"]["name"] == "DEVICE1"
    assert interface["device"]["tags"][0]["color"] == "aa1409"
    assert interface["cable"]["display"] == "#2"
    assert interface["cable"]["a_terminations"][0]["object"]["id"] == 2
    assert interface["link_peers_type"] == "dcim.interface"
    assert interface["link_peers"][0]["a_terminations"][0]["object"]["cable"]["id"] == 2
    # device
    device = tree.dcim.devices[1]
    assert device["tags"][0]["color"] == "aa1409"
    # root
    assert root.dcim.cables[2]["a_terminations"][0]["object"]["cable"] == 2
    assert root.dcim.interfaces[2]["cable"].get("a_terminations") is None


# noinspection DuplicatedCode
def test__grow_tree__circuit_terminations():
    """nb_tree.grow_tree() circuit_terminations dependency"""
    # set up simplified objects
    root = NbTree()
    circuit = {k: v for k, v in objects.CIRCUIT1.items() if k in
               ["id", "url", "cid", "termination_a"]}
    root.circuits.circuits = {d["id"]: d for d in [circuit]}
    term = {k: v for k, v in objects.TERMINATION1.items() if k in
            ["id", "url", "display", "circuit", "cable", "link_peers", "link_peers_type"]}
    root.circuits.circuit_terminations = {d["id"]: d for d in [term]}
    cable = {k: v for k, v in objects.CABLE1.items() if k in
             ["id", "url", "display", "a_terminations"]}
    root.dcim.cables = {d["id"]: d for d in [cable]}
    interface = {k: v for k, v in objects.INTERFACE1.items() if
                 k in ["id", "url", "name", "device", "cable", "link_peers", "link_peers_type"]}
    root.dcim.interfaces = {d["id"]: d for d in [interface]}
    device = {k: v for k, v in objects.DEVICE1.items() if k in ["id", "url", "name", "tags"]}
    root.dcim.devices = {d["id"]: d for d in [device]}
    tag = {k: v for k, v in objects.TAG1.items() if k in ["id", "url", "color"]}
    root.extras.tags = {d["id"]: d for d in [tag]}

    tree = nb_tree.grow_tree(tree=root)

    # circuit
    circuit = tree.circuits.circuits[1]
    assert circuit["cid"] == "CID1"
    assert circuit["termination_a"]["circuit"]["termination_a"]["circuit"]["id"] == 1
    # circuit_terminations
    term = tree.circuits.circuit_terminations[1]
    assert term["display"] == "CID1: Termination A"
    assert term["circuit"]["cid"] == "CID1"
    assert term["circuit"]["termination_a"]["circuit"]["cid"] == "CID1"
    assert term["link_peers_type"] == "dcim.interface"
    assert term["link_peers"][0]["name"] == "GigabitEthernet1/0/1"
    assert term["link_peers"][0]["device"]["tags"][0]["color"] == "aa1409"
    # interface
    interface = tree.dcim.interfaces[1]
    assert interface["name"] == "GigabitEthernet1/0/1"
    assert interface["device"]["tags"][0]["color"] == "aa1409"
    assert interface["cable"]["a_terminations"][0]["object_type"] == "circuits.circuittermination"
    assert interface["cable"]["a_terminations"][0]["object"]["display"] == "CID1: Termination A"
    assert interface["link_peers_type"] == "circuits.circuittermination"
    assert interface["link_peers"][0]["display"] == "CID1: Termination A"
    assert interface["link_peers"][0]["link_peers_type"] == "dcim.interface"
    assert interface["link_peers"][0]["link_peers"][0]["name"] == "GigabitEthernet1/0/1"
    assert interface["link_peers"][0]["link_peers"][0]["device"]["tags"][0]["color"] == "aa1409"
    # device
    device = tree.dcim.devices[1]
    assert device["tags"][0]["color"] == "aa1409"
    # root
    assert root.dcim.cables[1]["a_terminations"][0]["object"]["cable"] == 1
    assert root.dcim.interfaces[1]["cable"].get("a_terminations") is None


@pytest.mark.parametrize("urls, expected, errors", [
    ([], [], []),
    (["/api/ipam/vrfs/1"], [], []),
    (["/api/ipam/vrfs/9"], ["/api/ipam/vrfs/9"], []),
    (["/api/typo/vrfs/1"], [], [True]),
    (["/api/ipam/typo/1"], [], [True]),
])
def test__missed_urls(
        caplog,
        urls, expected, errors,
):
    """nb_tree.missed_urls()"""
    tree = objects.full_tree()
    actual = nb_tree.missed_urls(urls=urls, tree=tree)
    assert actual == expected
    logs = [record.levelname == "ERROR" for record in caplog.records]
    assert logs == errors
