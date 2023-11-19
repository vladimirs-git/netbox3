# pylint: disable=W0212,R0801,W0621

"""Unittests foragers."""
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch, mock_open

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from requests_mock import Mocker

from netbox3 import helpers as h, nb_forager
from netbox3.nb_cache import NbCache
from netbox3.nb_forager import NbForager
from netbox3.nb_tree import NbTree, insert_tree
from tests import objects


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager with root data."""
    return NbForager(host="netbox")


@pytest.fixture
def mock_requests_status():
    """Mock request for vrf searching."""


def test__app_model(nbf: NbForager):
    """NbForager has the same models as NbTree object"""
    tree = NbTree()
    for app in tree.apps():
        app_o = getattr(nbf, app)
        actual = h.attr_name(app_o)
        assert actual == app

        actual = app_o.__class__.__name__
        expected = "".join([f"{s.capitalize()}" for s in app.split("_")]) + "AF"
        assert actual == expected

        for model in getattr(tree, app).models():
            model_o = getattr(app_o, model)
            actual = h.attr_name(model_o)
            assert actual == model

            actual = model_o.__class__.__name__
            expected = "".join([f"{s.capitalize()}" for s in model.split("_")]) + "F"
            assert actual == expected


def test__host(nbf: NbForager):
    """NbForager.host."""
    assert nbf.host == "netbox"
    assert nbf.api.host == "netbox"
    assert nbf.api.ipam.vrfs.host == "netbox"


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
])
def test__url(params, expected):
    """NbForager.url."""
    nbf = NbForager(**params)
    assert nbf.url == expected
    assert nbf.api.url == expected


def test__count(nbf: NbForager):
    """NbForager.count()."""
    assert nbf.count() == 0

    nbf.circuits.circuit_terminations.data.update({1: {}})
    nbf.dcim.device_roles.data.update({1: {}, 3: {}})
    nbf.ipam.aggregates.data.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.data.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert nbf.count() == 10

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.data) == 1
    assert f"{nbf!r}" == "<NbForager: circuits=1, dcim=2, ipam=3, tenancy=4>"


def test__clear(nbf: NbForager):
    """NbForager.clear()."""
    nbf.root.ipam.vrfs.update(objects.vrf_d([1]))
    nbf.grow_tree()
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == [1]
    assert [d["id"] for d in nbf.tree.ipam.vrfs.values()] == [1]

    nbf.clear()
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == []
    assert [d["id"] for d in nbf.tree.ipam.vrfs.values()] == []

    nbf.root.ipam.vrfs.update(objects.vrf_d([1]))
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == [1]
    assert [d["id"] for d in nbf.ipam.vrfs.data.values()] == [1]
    assert [d["id"] for d in nbf.tree.ipam.vrfs.values()] == []


def test__copy(nbf: NbForager):
    """NbForager.copy()."""
    nbf.root.ipam.vrfs.update(objects.vrf_d([1]))

    copy_ = nbf.copy()
    assert nbf.count() == 1
    assert copy_.count() == 1

    nbf.root.ipam.vrfs.update(objects.vrf_d([2]))
    copy_.root.ipam.vrfs.update(objects.vrf_d([3, 4]))
    assert nbf.count() == 2
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == [1, 2]
    assert [d["id"] for d in nbf.ipam.vrfs.data.values()] == [1, 2]
    assert copy_.count() == 3
    assert [d["id"] for d in copy_.root.ipam.vrfs.values()] == [1, 3, 4]
    assert [d["id"] for d in copy_.ipam.vrfs.data.values()] == [1, 3, 4]


def test__read_cache(nbf: NbForager):
    """NbForager.read_cache()."""
    tree = NbTree()
    tree.ipam.vrfs.update(objects.vrf_d([1]))  # pylint: disable=E1101
    meta = {"write_time": "2000-12-31 23:59:59"}
    return_value = {"tree": tree.model_dump(), "status": {"meta": meta}}
    patch("pathlib.Path.open", mock_open()).start()
    patch("pickle.load", return_value=return_value).start()
    assert nbf.root.ipam.vrfs == {}

    nbf.read_cache()
    assert nbf.root.ipam.vrfs[1]["id"] == 1
    assert nbf.status["meta"] == meta


def test__write_cache(nbf: NbForager, monkeypatch: MonkeyPatch):
    """NbForager.write_cache()."""
    monkeypatch.setattr(Path, "open", Mock())
    monkeypatch.setattr(NbCache, "_create_dir", Mock())
    monkeypatch.setattr(NbCache, "_create_file", Mock())
    nbf.write_cache()


def test__grow_tree(nbf: NbForager):
    """NbForager.grow_tree()."""
    nbf.root.ipam.vrfs.update({1: objects.VRF1})
    nbf.root.tenancy.tenants.update({1: objects.TENANT1})
    assert nbf.tree.ipam.vrfs == {}

    result: NbTree = nbf.grow_tree()
    assert result.ipam.vrfs[1]["tenant"]["tags"][0]["name"] == "TAG1"
    assert nbf.tree.ipam.vrfs[1]["tenant"]["tags"][0]["name"] == "TAG1"


def test__get_status(
        nbf: NbForager,
        mock_requests_status: Mocker,  # pylint: disable=unused-argument
):
    """NbForager.get_status()."""
    with requests_mock.Mocker() as mock:
        mock.get("https://netbox/api/status/", json={"netbox-version": "3.6.5"})

        nbf.get_status()
        actual = nbf.status
        assert actual == {"netbox-version": "3.6.5"}


@pytest.mark.parametrize("version, expected", [
    ("", "0.0.0"),
    ("3.6.5", "3.6.5")
])
def test__version(nbf: NbForager, version, expected):
    """NbForager.version()."""
    nbf.status = {"netbox-version": version}
    actual = nbf.version()
    assert actual == expected


def test__devices_primary_ip4(nbf: NbForager):
    """NbForager.devices_primary_ip4()."""
    tree = objects.full_tree()
    insert_tree(src=tree, dst=nbf.root)
    actual = nbf._devices_primary_ip4()
    assert actual == ["10.1.1.1/24", "10.2.2.2/24"]

    nbf.root.dcim.devices[1]["primary_ip4"] = None
    actual = nbf._devices_primary_ip4()
    assert actual == ["10.2.2.2/24"]


def test__set_addresses_mask_32(nbf: NbForager):
    """NbForager.set_addresses_mask_32()."""
    tree = objects.full_tree()
    insert_tree(src=tree, dst=nbf.root)

    actual = [d["address"] for d in nbf.root.ipam.ip_addresses.values()]
    assert actual == ["10.0.0.1/24", "1.0.0.1/24"]

    nbf._set_ipam_ip_addresses_mask_32()
    actual = [d["address"] for d in nbf.root.ipam.ip_addresses.values()]
    assert actual == ["10.0.0.1/32", "1.0.0.1/32"]


def test__print_warnings(nbf: NbForager, caplog):
    """NbForager.print_warnings()."""
    nbf._print_warnings()
    actual = [record.levelname == "WARNING" for record in caplog.records]
    assert actual == []

    tree = objects.full_tree()
    tree.ipam.ip_addresses[1]["warnings"] = ["warning"]  # pylint: disable=E1101
    insert_tree(src=tree, dst=nbf.root)

    nbf._print_warnings()
    actual = [record.levelname == "WARNING" for record in caplog.records]
    assert actual == [True]


@pytest.mark.parametrize("kwargs, expected", [
    ({"cache": "", "name": None, "host": None}, "NbCache.pickle"),
    ({"cache": "", "name": None, "host": "host"}, "host.pickle"),
    ({"cache": "", "name": "name", "host": None}, "name.pickle"),
    ({"cache": "", "name": "name", "host": "host"}, "name.host.pickle"),
    ({"cache": "/sub/dir", "name": None, "host": None}, r"\sub\dir\NbCache.pickle"),
    ({"cache": "/sub/dir", "name": None, "host": "host"}, r"\sub\dir\host.pickle"),
    ({"cache": "/sub/dir", "name": "name", "host": None}, r"\sub\dir\name.pickle"),
    ({"cache": "/sub/dir", "name": "name", "host": "host"}, r"\sub\dir\name.host.pickle"),
])
def test__make_cache_path(kwargs, expected):
    """nb_foragers.make_cache_path()."""
    actual = nb_forager.make_cache_path(**kwargs)
    assert actual == expected
