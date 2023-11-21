# pylint: disable=W0212,R0801,W0621

"""Unittests param_path.py."""
import pytest

from netbox3.api import param_path
from netbox3.api.param_path import ParamPath


def test__param_map():
    """ParamMap()."""
    obj = ParamPath(param="name", path="app/name")
    assert obj.param == "name"
    assert obj.param_id == "name_id"
    assert obj.path == "app/name"
    assert obj.key == "name"


def test__data():
    """param_map.data()."""
    data = param_path.data(path="dcim/sites/")
    assert data["circuit"].key == "cid"
    assert data["group"].path == "dcim/site-groups/"
    assert data.get("role") is None

    data = param_path.data(path="ipam/ip-addresses/")
    assert data["circuit"].key == "cid"
    assert data.get("group") is None
    assert data["role"].path == "ipam/roles/"


@pytest.mark.parametrize("params_d, expected", [
    ({}, {}),
    ({"a": [1]}, {}),
    ({"vrf": ["null"]}, {}),
    ({"vrf": ["a"]}, {"vrf": ["a"]}),
    ({"vrf": ["a", "null"]}, {"vrf": ["a", "null"]}),
    ({"present_in_vrf": ["a"]}, {"present_in_vrf": ["a"]}),
    ({"present_in_vrf": ["null"]}, {}),
])
def test__need_change(params_d, expected):
    """param_map.need_change()."""
    mapping = param_path.data(path="ipam/vrfs/")
    actual = param_path.need_change(params_d=params_d, mapping=mapping)
    assert actual == expected