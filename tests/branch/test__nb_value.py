# pylint: disable=protected-access

"""Unittests nb_branch.py."""
from typing import Any

import pytest

from netbox3.branch.nb_value import NbValue
from netbox3.types_ import LStr
from tests import params__nb_branch as p


@pytest.mark.parametrize("keys, data, strict, expected", p.ID_)
def test__id_(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbValue.id_()."""
    _ = keys  # noqa
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, int):
        actual = branch.id_()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.id_()


@pytest.mark.parametrize("data, strict, expected", p.ADDRESS)
def test__address(data: dict, strict: bool, expected: Any):
    """NbValue.address()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.address()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.address()


@pytest.mark.parametrize("data, strict, expected", p.GROUP_NAME)
def test__group_name(data: dict, strict: bool, expected: Any):
    """NbValue.group_name()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.group_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.group_name()


@pytest.mark.parametrize("data, strict, expected", p.NAME_)
def test__name(data: dict, strict: bool, expected: Any):
    """NbValue.name()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.name()


@pytest.mark.parametrize("data, strict, expected", p.ASSIGNED_DEVICE)
def test__assigned_device(data: dict, strict: bool, expected: Any):
    """NbValue.assigned_device()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.assigned_device()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.assigned_device()


@pytest.mark.parametrize("data, strict, expected", p.PREFIX_)
def test__prefix(data: dict, strict: bool, expected: Any):
    """NbValue.prefix()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.prefix()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.prefix()


@pytest.mark.parametrize("data, strict, expected", p.PRIMARY_IP4)
def test__primary_ip4(data: dict, strict: bool, expected: Any):
    """NbValue.primary_ip4()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.primary_ip4()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.primary_ip4()


@pytest.mark.parametrize("data, strict, expected", p.PRIMARY_IP)
def test__primary_ip(data: dict, strict: bool, expected: Any):
    """NbValue.primary_ip()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.primary_ip()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.primary_ip()


@pytest.mark.parametrize("data, strict, upper, expected", p.SITE_NAME)
def test__site_name(data: dict, strict: bool, upper: bool, expected: Any):
    """NbValue.site_name()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.site_name(upper=upper)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.site_name()


@pytest.mark.parametrize("data, strict, expected", p.GET_VID)
def test__vid(data: dict, strict: bool, expected: Any):
    """NbValue.vid()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, int):
        actual = branch.vid()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.vid()


@pytest.mark.parametrize("data, strict, expected", p.GET_VLAN)
def test__vlan(data: dict, strict: bool, expected: Any):
    """NbValue.vlan()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, int):
        actual = branch.vlan()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.vlan()


@pytest.mark.parametrize("data, strict, expected", p.URL)
def test__url(data: dict, strict: bool, expected: Any):
    """NbValue.url()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.url()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.url()


# ============================== is ==================================


@pytest.mark.parametrize("data, strict, ipam, expected", p.IS_IPAM)
def test__is_ipam(data: dict, strict: bool, ipam: str, expected: Any):
    """NbValue.is_ipam()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = branch.is_ipam(ipam)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.is_ipam(ipam)


@pytest.mark.parametrize("data, strict, dcim, expected", p.IS_DCIM)
def test__is_dcim(data: dict, strict: bool, dcim: str, expected: Any):
    """NbValue.is_dcim()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = branch.is_dcim(dcim)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.is_dcim(dcim)


@pytest.mark.parametrize("data, strict, expected", p.IS_VRF)
def test__is_vrf(data: dict, strict: bool, expected: Any):
    """NbValue.is_vrf()."""
    branch = NbValue(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = branch.is_vrf()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.is_vrf()


# ============================= helpers ==============================


@pytest.mark.parametrize("subnet, expected", p.IS_PREFIX)
def test__is_prefix(subnet: str, expected: Any):
    """NbValue.is_prefix()."""
    branch = NbValue(data={})
    if isinstance(expected, bool):
        actual = branch._is_prefix(subnet)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch._is_prefix(subnet)
