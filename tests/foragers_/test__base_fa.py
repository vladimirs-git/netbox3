# pylint: disable=W0212,R0801,W0621

"""Unittests base_fa.py."""

import pytest

from netbox3.nb_forager import NbForager


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager."""
    return NbForager(host="netbox")


def test__init(nbf):
    """BaseAF.__init__()."""
    assert nbf.circuits.app == "circuits"
    assert nbf.dcim.app == "dcim"
    assert nbf.extras.app == "extras"
    assert nbf.ipam.app == "ipam"
    assert nbf.tenancy.app == "tenancy"
    assert nbf.virtualization.app == "virtualization"


def test__count(nbf):
    """BaseAF.count()."""
    nbf.circuits.circuit_terminations.data.update({1: {}})
    nbf.circuits.circuit_types.data.update({1: {}})
    nbf.dcim.device_roles.data.update({1: {}})
    nbf.dcim.device_types.data.update({1: {}, 2: {}})
    nbf.ipam.aggregates.data.update({1: {}})
    nbf.ipam.asn_ranges.data.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.data.update({1: {}})
    nbf.tenancy.tenants.data.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert nbf.circuits.count() == 2
    assert nbf.dcim.count() == 3
    assert nbf.ipam.count() == 4
    assert nbf.tenancy.count() == 5

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.data) == 1
    assert f"{nbf.circuits!r}" == "<CircuitsAF: 2>"
