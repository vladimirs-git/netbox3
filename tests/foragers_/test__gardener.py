# pylint: disable=W0212,W0621

"""Unittests foragers."""

import pytest

from netbox3 import nb_tree
from netbox3.api.base_c import BaseC
from netbox3.foragers.joiner import Joiner
from netbox3.foragers.ipv4 import IPv4
from netbox3.nb_tree import NbTree
from tests import objects


@pytest.fixture
def joiner() -> Joiner:
    """Init Joiner with root data."""
    tree: NbTree = objects.full_tree()
    tree = nb_tree.join_tree(tree)
    joiner_ = Joiner(tree=tree)
    return joiner_


def test__join_dcim_devices(joiner: Joiner):
    """Joiner.join_dcim_devices()."""
    joiner.join_dcim_devices()

    device = joiner.tree.dcim.devices[1]
    models = BaseC._reserved_keys["dcim/devices/"]
    for model in models:
        isinstance(device[model], dict)

    assert device["interfaces"]["GigabitEthernet1/0/1"]["name"] == "GigabitEthernet1/0/1"
    assert device["console_ports"]["CONSOLE PORT1"]["name"] == "CONSOLE PORT1"


def test__join_virtualization_virtual_machines(joiner: Joiner):
    """Joiner.join_virtualization_virtual_machines()."""
    joiner.join_virtualization_virtual_machines()

    machine = joiner.tree.virtualization.virtual_machines[1]
    models = BaseC._reserved_keys["virtualization/virtual-machines/"]
    for model in models:
        isinstance(machine[model], dict)

    assert machine["interfaces"]["INTERFACE1"]["name"] == "INTERFACE1"


def test__join_ipam_ipv4(joiner: Joiner):
    """Joiner.join_ipam_ipv4()."""
    joiner.join_ipam_ipv4()

    aggregate = joiner.tree.ipam.aggregates[1]
    assert aggregate["prefix"] == "10.0.0.0/16"
    assert aggregate["ipv4"] == IPv4("10.0.0.0/16")
    assert aggregate["aggregate"] == {}
    assert aggregate["super_prefix"] == {}
    assert [d["prefix"] for d in aggregate["sub_prefixes"]] == ["10.0.0.0/24"]
    assert aggregate["ip_addresses"] == []

    prefix = joiner.tree.ipam.prefixes[1]
    assert prefix["prefix"] == "10.0.0.0/24"
    assert prefix["ipv4"] == IPv4("10.0.0.0/24")
    assert prefix["aggregate"]["prefix"] == "10.0.0.0/16"
    assert prefix["super_prefix"] == {}
    assert [d["prefix"] for d in prefix["sub_prefixes"]] == ["10.0.0.0/31"]
    assert [d["address"] for d in prefix["ip_addresses"]] == ["10.0.0.1/24"]

    prefix = joiner.tree.ipam.prefixes[4]
    assert prefix["prefix"] == "10.0.0.0/31"
    assert prefix["ipv4"] == IPv4("10.0.0.0/31")
    assert prefix["aggregate"]["prefix"] == "10.0.0.0/16"
    assert prefix["super_prefix"]["prefix"] == "10.0.0.0/24"
    assert [d["prefix"] for d in prefix["sub_prefixes"]] == ["10.0.0.0/32"]
    assert prefix["ip_addresses"] == []

    prefix = joiner.tree.ipam.prefixes[5]
    assert prefix["prefix"] == "10.0.0.0/32"
    assert prefix["ipv4"] == IPv4("10.0.0.0/32")
    assert prefix["aggregate"]["prefix"] == "10.0.0.0/16"
    assert prefix["super_prefix"]["prefix"] == "10.0.0.0/31"
    assert prefix["sub_prefixes"] == []
    assert prefix["ip_addresses"] == []

    ip_address = joiner.tree.ipam.ip_addresses[1]
    assert ip_address["address"] == "10.0.0.1/24"
    assert ip_address["ipv4"] == IPv4("10.0.0.1/24")
    assert ip_address["aggregate"]["prefix"] == "10.0.0.0/16"
    assert ip_address["super_prefix"]["prefix"] == "10.0.0.0/24"
    assert ip_address["sub_prefixes"] == []
    assert ip_address["ip_addresses"] == []


@pytest.mark.parametrize("model, network", [
    ("aggregates", "10.0.0.0/16"),
    ("prefixes", "10.0.0.0/24"),
    ("ip_addresses", "10.0.0.1/24"),
])
def test__init_ipam_keys(joiner: Joiner, model, network):
    """Joiner._init_ipam_keys()."""
    data = getattr(joiner.tree.ipam, model)[1]
    assert data.get("ipv4") is None
    assert data.get("aggregate") is None
    assert data.get("super_prefix") is None
    assert data.get("super_prefix") is None
    assert data.get("ip_addresses") is None

    joiner._init_ipam_keys()
    assert data["ipv4"] == IPv4(network)
    assert data.get("aggregate") == {}
    assert data.get("super_prefix") == {}
    assert data.get("sub_prefixes") == []
    assert data.get("ip_addresses") == []


def test__join_ipam_aggregates(joiner: Joiner):
    """Joiner._join_ipam_aggregates()."""
    joiner._init_ipam_keys()
    joiner._join_ipam_aggregates()

    for idx, network, sub_prefixes in [
        (1, "10.0.0.0/16", ["10.0.0.0/24"]),
        (2, "1.0.0.0/16", ["1.0.0.0/24"]),
    ]:
        data = joiner.tree.ipam.aggregates[idx]
        assert data["ipv4"] == IPv4(network)
        assert data["aggregate"] == {}
        assert data["super_prefix"] == {}
        assert [d["prefix"] for d in data["sub_prefixes"]] == sub_prefixes
        assert data["ip_addresses"] == []

    for idx, prefix, aggregate in [
        (1, "10.0.0.0/24", "10.0.0.0/16"),
        (2, "1.0.0.0/24", "1.0.0.0/16"),
        (3, "10.0.0.0/24", None),
        (4, "10.0.0.0/31", "10.0.0.0/16"),
        (5, "10.0.0.0/32", "10.0.0.0/16"),
    ]:
        data = joiner.tree.ipam.prefixes[idx]
        assert data["prefix"] == prefix
        assert data["aggregate"].get("prefix") == aggregate


def test__extra__join_ipam_ip_addresses(joiner: Joiner):
    """Joiner._join_ipam_ip_addresses()."""
    joiner._init_ipam_keys()
    joiner._join_ipam_aggregates()
    joiner._join_ipam_prefixes()
    joiner._join_ipam_ip_addresses()

    for idx, network, aggregate, super_prefix, vrf in [
        (1, "10.0.0.1/24", "10.0.0.0/16", "10.0.0.0/24", False),
        (2, "1.0.0.1/24", "1.0.0.0/16", "1.0.0.0/24", False),
        (3, "10.0.0.3/24", None, None, True),
    ]:
        data = joiner.tree.ipam.ip_addresses[idx]
        assert data["ipv4"] == IPv4(network)
        assert data["aggregate"].get("prefix") == aggregate
        assert data["super_prefix"].get("prefix") == super_prefix
        assert [d["prefix"] for d in data["sub_prefixes"]] == []
        assert data["ip_addresses"] == []
        assert bool(data["vrf"]) is vrf


def test__join_ipam_prefixes(joiner: Joiner):
    """Joiner._join_ipam_prefixes()."""
    joiner._init_ipam_keys()
    joiner._join_ipam_aggregates()
    joiner._join_ipam_prefixes()

    for idx, network, aggregate, super_prefix, sub_prefixes, vrf in [
        (1, "10.0.0.0/24", "10.0.0.0/16", None, ["10.0.0.0/31"], False),
        (2, "1.0.0.0/24", "1.0.0.0/16", None, [], False),
        (3, "10.0.0.0/24", None, None, [], True),
        (4, "10.0.0.0/31", "10.0.0.0/16", "10.0.0.0/24", ["10.0.0.0/32"], False),
        (5, "10.0.0.0/32", "10.0.0.0/16", "10.0.0.0/31", [], False),
    ]:
        data = joiner.tree.ipam.prefixes[idx]
        assert data["ipv4"] == IPv4(network)
        assert data["aggregate"].get("prefix") == aggregate
        assert data["super_prefix"].get("prefix") == super_prefix
        assert [d["prefix"] for d in data["sub_prefixes"]] == sub_prefixes
        assert data["ip_addresses"] == []
        assert bool(data["vrf"]) is vrf


# ============================= helpers ==============================

def test__get_aggregates_ip4(joiner: Joiner):
    """Joiner._get_aggregates_ip4()."""
    joiner._init_ipam_keys()
    unsorted = [d["prefix"] for d in joiner.tree.ipam.aggregates.values()]
    assert unsorted == ["10.0.0.0/16", "1.0.0.0/16"]

    aggregates = joiner._get_aggregates_ip4()
    actual = [d["prefix"] for d in aggregates]
    assert actual == ["1.0.0.0/16", "10.0.0.0/16"]


def test__get_ip_addresses_ip4(joiner: Joiner):
    """Joiner._get_ip_addresses_ip4()."""
    joiner._init_ipam_keys()
    unsorted = [d["address"] for d in joiner.tree.ipam.ip_addresses.values()]
    assert unsorted == ["10.0.0.1/24", "1.0.0.1/24", "10.0.0.3/24"]

    ip_addresses = joiner._get_ip_addresses_ip4()
    actual = [d["address"] for d in ip_addresses]
    assert actual == ["1.0.0.1/24", "10.0.0.1/24"]


def test__get_prefixes_ip4(joiner: Joiner):
    """Joiner._get_prefixes_ip4()."""
    joiner._init_ipam_keys()
    unsorted = [d["prefix"] for d in joiner.tree.ipam.prefixes.values()]
    assert unsorted == ["10.0.0.0/24", "1.0.0.0/24", "10.0.0.0/24", "10.0.0.0/31", "10.0.0.0/32"]

    prefixes = joiner._get_prefixes_ip4()
    actual = [d["prefix"] for d in prefixes]
    assert actual == ["1.0.0.0/24", "10.0.0.0/24", "10.0.0.0/31", "10.0.0.0/32"]


def test__get_prefixes_ip4_d(joiner: Joiner):
    """Joiner._get_prefixes_ip4_d()."""
    joiner._init_ipam_keys()
    unsorted = [d["prefix"] for d in joiner.tree.ipam.prefixes.values()]
    assert unsorted == ["10.0.0.0/24", "1.0.0.0/24", "10.0.0.0/24", "10.0.0.0/31", "10.0.0.0/32"]

    prefixes_d = joiner._get_prefixes_ip4_d()
    actual = {k: [d["prefix"] for d in ld] for k, ld in prefixes_d.items()}
    assert actual == {0: ["1.0.0.0/24", "10.0.0.0/24"], 1: ["10.0.0.0/31"], 2: ["10.0.0.0/32"]}
