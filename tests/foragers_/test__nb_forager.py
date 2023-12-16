# pylint: disable=E1101,W0212,R0801,R0915,W0621

"""Unittests foragers."""
import inspect
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch, mock_open

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch

from netbox3 import helpers as h, nb_forager, NbApi, nb_tree
from netbox3.nb_cache import NbCache
from netbox3.nb_forager import NbForager
from netbox3.nb_tree import NbTree
from tests import objects


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager without data."""
    return NbForager(host="netbox")


@pytest.fixture
def nbf_r() -> NbForager:
    """Init NbForager with NbForager.root data."""
    nbf_ = NbForager(host="netbox")
    tree: NbTree = objects.full_tree()
    nb_tree.insert_tree(src=tree, dst=nbf_.root)
    return nbf_


@pytest.fixture
def nbf_t() -> NbForager:
    """Init NbForager with NbForager.tree data."""
    nbf_ = NbForager(host="netbox")
    tree: NbTree = objects.full_tree()

    nb_tree.insert_tree(src=tree, dst=nbf_.tree)
    return nbf_


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


def test__init(nbf: NbForager):
    """NbForager.__init__()."""
    actual = list(inspect.signature(type(nbf).__init__).parameters)
    expected = [
        "self",
        "host",
        "token",
        "scheme",
        "port",
        "verify",
        "limit",
        "url_length",
        "threads",
        "interval",
        "timeout",
        "max_retries",
        "sleep",
        "default_get",
        "loners",
        "cache",
        "kwargs",
    ]
    assert actual == expected

    assert nbf.api.host == "netbox"
    assert nbf.api.ipam.aggregates.host == "netbox"
    assert nbf.api.ipam.aggregates.token == ""
    assert nbf.api.ipam.aggregates.scheme == "https"
    assert nbf.api.ipam.aggregates.port == 443
    assert nbf.api.ipam.aggregates.verify is True
    assert nbf.api.ipam.aggregates.limit == 1000
    assert nbf.api.ipam.aggregates.url_length == 2047
    assert nbf.api.ipam.aggregates.threads == 1
    assert nbf.api.ipam.aggregates.interval == 0.0
    assert nbf.api.ipam.aggregates.timeout == 60
    assert nbf.api.ipam.aggregates.max_retries == 0
    assert nbf.api.ipam.aggregates.sleep == 10
    assert nbf.api.ipam.aggregates._default_get == {}
    assert nbf.api.ipam.aggregates._loners == ["q", "prefix"]
    assert nbf.cache == "netbox.pickle"

    params = {
        "host": "netbox",
        "token": "token",
        "scheme": "http",
        "port": "8080",
        "verify": False,
        "limit": 1,
        "url_length": 1,
        # Multithreading
        "threads": 2,
        "interval": 1,
        # Errors processing
        "timeout": 1,
        "max_retries": 1,
        "sleep": 1,
        # Settings
        "default_get": {"any": ["a1"]},
        "loners": {"any": ["a1"]},
        "cache": "1.pickle"
    }
    nbf = NbForager(**params)  # type: ignore
    assert nbf.api.host == "netbox"
    assert nbf.api.ipam.aggregates.host == "netbox"
    assert nbf.api.ipam.aggregates.token == "token"
    assert nbf.api.ipam.aggregates.scheme == "http"
    assert nbf.api.ipam.aggregates.port == 8080
    assert nbf.api.ipam.aggregates.verify is False
    assert nbf.api.ipam.aggregates.limit == 1
    assert nbf.api.ipam.aggregates.url_length == 1
    assert nbf.api.ipam.aggregates.threads == 2
    assert nbf.api.ipam.aggregates.interval == 1.0
    assert nbf.api.ipam.aggregates.timeout == 1
    assert nbf.api.ipam.aggregates.max_retries == 1
    assert nbf.api.ipam.aggregates.sleep == 1
    assert nbf.api.ipam.aggregates._loners == ["a1"]
    assert nbf.cache == "1.pickle"

    api = NbApi(**params)  # type: ignore
    assert api.host == "netbox"
    assert api.ipam.aggregates.host == "netbox"
    assert api.ipam.aggregates.token == "token"
    assert api.ipam.aggregates.scheme == "http"
    assert api.ipam.aggregates.port == 8080
    assert api.ipam.aggregates.verify is False
    assert api.ipam.aggregates.limit == 1
    assert api.ipam.aggregates.url_length == 1
    assert api.ipam.aggregates.threads == 2
    assert api.ipam.aggregates.interval == 1.0
    assert api.ipam.aggregates.timeout == 1
    assert api.ipam.aggregates.max_retries == 1
    assert api.ipam.aggregates.sleep == 1
    assert api.ipam.aggregates._loners == ["a1"]

    diff = set(params).difference(set(api.ipam.aggregates._init_params))
    assert diff == {"cache"}


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

    nbf.circuits.circuit_terminations.root_d.update({1: {}})
    nbf.dcim.device_roles.root_d.update({1: {}, 3: {}})
    nbf.ipam.aggregates.root_d.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.root_d.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert nbf.count() == 10

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.root_d) == 1
    assert f"{nbf!r}" == "<NbForager: circuits=1, dcim=2, ipam=3, tenancy=4>"


def test__clear(nbf: NbForager):
    """NbForager.clear()."""
    nbf.root.ipam.vrfs.update(objects.vrf_d([1]))
    nbf.join_tree()
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == [1]
    assert [d["id"] for d in nbf.tree.ipam.vrfs.values()] == [1]

    nbf.clear()
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == []
    assert [d["id"] for d in nbf.tree.ipam.vrfs.values()] == []

    nbf.root.ipam.vrfs.update(objects.vrf_d([1]))
    assert [d["id"] for d in nbf.root.ipam.vrfs.values()] == [1]
    assert [d["id"] for d in nbf.ipam.vrfs.root_d.values()] == [1]
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
    assert [d["id"] for d in nbf.ipam.vrfs.root_d.values()] == [1, 2]
    assert copy_.count() == 3
    assert [d["id"] for d in copy_.root.ipam.vrfs.values()] == [1, 3, 4]
    assert [d["id"] for d in copy_.ipam.vrfs.root_d.values()] == [1, 3, 4]


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


def test__get_status(nbf: NbForager):
    """NbForager.get_status()."""
    with requests_mock.Mocker() as mock:
        mock.get("https://netbox/api/status/", json={"netbox-version": "3.6.5"})

        nbf.get_status()
        actual = nbf.status
        assert actual == {"netbox-version": "3.6.5"}


def test__join_tree(nbf_r: NbForager):
    """NbForager.join_tree()."""
    assert nbf_r.tree.ipam.aggregates == {}
    assert nbf_r.tree.ipam.prefixes == {}
    assert nbf_r.tree.ipam.ip_addresses == {}

    tree: NbTree = nbf_r.join_tree(extra=False)

    aggregate = tree.ipam.aggregates[1]
    assert aggregate["tenant"]["tags"][0]["name"] == "TAG1"
    assert aggregate.get("sub_prefixes") is None
    prefix = tree.ipam.prefixes[1]
    assert prefix["tenant"]["tags"][0]["name"] == "TAG1"
    assert prefix.get("sub_prefixes") is None
    ip_address = tree.ipam.ip_addresses[1]
    assert ip_address["tenant"]["tags"][0]["name"] == "TAG1"
    assert ip_address.get("super_prefix") is None
    device = tree.dcim.devices[1]
    assert device.get("interfaces") is None

    tree = nbf_r.join_tree(extra=True)

    aggregate = tree.ipam.aggregates[1]
    assert aggregate["tenant"]["tags"][0]["name"] == "TAG1"
    assert aggregate["sub_prefixes"][0]["prefix"] == "10.0.0.0/24"
    prefix = tree.ipam.prefixes[1]
    assert prefix["tenant"]["tags"][0]["name"] == "TAG1"
    assert prefix["sub_prefixes"][0]["prefix"] == "10.0.0.0/31"
    ip_address = tree.ipam.ip_addresses[1]
    assert ip_address["tenant"]["tags"][0]["name"] == "TAG1"
    assert ip_address["super_prefix"]["prefix"] == "10.0.0.0/24"
    device = tree.dcim.devices[1]
    assert device["interfaces"]["GigabitEthernet1/0/1"]["name"] == "GigabitEthernet1/0/1"


@pytest.mark.parametrize("version, expected", [
    ("", "0.0.0"),
    ("3.6.5", "3.6.5"),
])
def test__version(nbf: NbForager, version, expected):
    """NbForager.version()."""
    nbf.status = {"netbox-version": version}
    actual = nbf.version()
    assert actual == expected


# =========================== data methods ===========================

def test__devices_primary_ip4(nbf_r: NbForager):
    """NbForager.devices_primary_ip4()."""
    actual = nbf_r._devices_primary_ip4()
    assert actual == ["10.1.1.1/24", "10.2.2.2/24", "10.3.3.3/24"]

    nbf_r.root.dcim.devices[1]["primary_ip4"] = None
    actual = nbf_r._devices_primary_ip4()
    assert actual == ["10.2.2.2/24", "10.3.3.3/24"]


def test__set_addresses_mask_32(nbf_r: NbForager):
    """NbForager.set_addresses_mask_32()."""
    actual = [d["address"] for d in nbf_r.root.ipam.ip_addresses.values()]
    assert actual == ["10.0.0.1/24", "1.0.0.1/24", "10.0.0.3/24"]

    nbf_r._set_ipam_ip_addresses_mask_32()
    actual = [d["address"] for d in nbf_r.root.ipam.ip_addresses.values()]
    assert actual == ["10.0.0.1/32", "1.0.0.1/32", "10.0.0.3/32"]


def test__print_warnings(nbf_r: NbForager, caplog):
    """NbForager.print_warnings()."""
    nbf_r._print_warnings()
    actual = [record.levelname == "WARNING" for record in caplog.records]
    assert actual == []

    nbf_r.root.ipam.ip_addresses[1]["warnings"] = ["warning"]  # pylint: disable=E1101
    nbf_r._print_warnings()
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
