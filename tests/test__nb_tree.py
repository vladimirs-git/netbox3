# pylint: disable=E1101,W0212

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


@pytest.mark.parametrize("data, expected", [
    ({"id": 9, "url": "/circuits/circuit-terminations/1"}, 1),
    ({"id": 9, "url": "/circuits/circuit-terminations/1/"}, 1),
    ({"id": 9, "url": "/typo/ip_addresses/1"}, AttributeError),
    ({"id": 9, "url": "/ipam/typo/1"}, AttributeError),
    ({"id": 9, "url": "/ipam/1"}, ValueError),
    ({"id": 9, "url": "/ipam/ip_addresses/typo"}, ValueError),
    ({"id": 9, "url": "/ipam/ip_addresses/8"}, 9),
    ({"id": 9}, 9),
    (1, 9),
    ("value", 9),
])
def test__join_data(data: Any, expected: Any):
    """nb_tree._join_data() for dict"""
    tree = objects.full_tree()
    if isinstance(expected, int):
        nb_tree._join_data(data=data, tree=tree)
        if isinstance(data, dict):
            actual = data.get("id")
            assert actual == expected
    else:
        with pytest.raises(expected):
            nb_tree._join_data(data=data, tree=tree)


@pytest.mark.parametrize("data, expected", [
    ([{"id": 9, "url": "/circuits/circuits/1"}, {"id": 9, "url": "/ipam/ip_addresses/2"}], [1, 2]),
    ([{"id": 9}], [9]),
    (["text"], []),
])
def test__join_data_list(data, expected):
    """nb_tree._join_data() for list"""
    tree = objects.full_tree()
    nb_tree._join_data(data=data, tree=tree)
    if expected:
        for idx, expected_ in enumerate(expected):
            actual = data[idx].get("id")
            assert actual == expected_


def test__grow_tree():
    """nb_tree.grow_tree()"""
    tree = objects.full_tree()
    result = nb_tree.grow_tree(tree=tree)
    c_terms = tree.circuits.circuit_terminations
    c_circuits = tree.circuits.circuits
    assert c_terms[1]["tags"][0].get("slug") is None
    assert c_terms[1]["site"].get("slug") is None
    assert c_terms[1]["circuit"].get("provider") is None
    assert c_terms[1]["link_peers"][0]["device"].get("serial") is None
    assert c_circuits[1]["termination_a"].get("term_side") is None
    assert c_circuits[1]["termination_z"].get("term_side") is None
    assert c_circuits[1]["termination_a"]["site"].get("tags") is None

    c_terms = result.circuits.circuit_terminations
    c_circuits = result.circuits.circuits
    assert c_terms[1]["circuit"]["tags"][0]["slug"] == "tag1"
    assert c_terms[1]["site"]["tags"][0]["slug"] == "tag1"
    assert c_terms[1]["tags"][0]["slug"] == "tag1"
    assert c_terms[1]["site"]["slug"] == "site1"
    assert c_terms[1]["circuit"]["provider"]["tags"][0]["slug"] == "tag1"
    assert c_terms[1]["link_peers"][0]["device"]["tags"][0]["slug"] == "tag1"
    assert c_circuits[1]["termination_a"]["term_side"] == "A"
    assert c_circuits[1]["termination_z"]["term_side"] == "Z"
    assert c_circuits[1]["termination_a"]["site"]["tags"][0]["slug"] == "tag1"


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
