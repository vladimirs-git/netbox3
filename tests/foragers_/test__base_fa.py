# pylint: disable=W0212,R0801,W0621

"""Unittests base_fa.py."""
import pytest

from netbox3 import NbForager


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager without data."""
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
    nbf.circuits.circuit_terminations.root_d.update({1: {}})
    nbf.circuits.circuit_types.root_d.update({1: {}})
    nbf.dcim.device_roles.root_d.update({1: {}})
    nbf.dcim.device_types.root_d.update({1: {}, 2: {}})
    nbf.ipam.aggregates.root_d.update({1: {}})
    nbf.ipam.asn_ranges.root_d.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.root_d.update({1: {}})
    nbf.tenancy.tenants.root_d.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert nbf.circuits.count() == 2
    assert nbf.dcim.count() == 3
    assert nbf.ipam.count() == 4
    assert nbf.tenancy.count() == 5

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.root_d) == 1
    assert f"{nbf.circuits!r}" == "<CircuitsAF: 2>"
