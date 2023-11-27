# pylint: disable=W0212,R0801,W0621

"""Unittests base_c.py."""
from typing import Any

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from requests import Response, Session
from requests_mock import Mocker

from netbox3.api import base_c
from netbox3.exceptions import NbApiError
from netbox3.nb_api import NbApi
from netbox3.nb_forager import NbForager
from netbox3.types_ import DAny, LDAny


@pytest.fixture
def api():
    """Init API"""
    return NbApi(host="netbox")


@pytest.fixture
def mock_requests_vrf():
    """Mock Session."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://netbox/api/ipam/vrfs/?limit=1000&offset=0",
            json={"results": [{"id": 1, "name": "VRF 1"}, {"id": 2, "name": "VRF 2"}]},
        )
        yield mock


def mock_session(status_code: int, content: str = ""):
    """Mock Session, set Response status_code and text."""

    def mock(*args, **kwargs):
        _ = args, kwargs  # noqa
        response = Response()
        response.status_code = status_code
        response._content = content.encode()
        return response

    return mock


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/circuits/circuit-terminations/"),
])
def test__url(params, expected):
    """BaseC.url."""
    api = NbApi(**params)
    actual = api.circuits.circuit_terminations.url
    assert actual == expected

    nbf = NbForager(**params)
    actual = nbf.api.circuits.circuit_terminations.url
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
])
def test__url_base(params, expected):
    """BaseC.url_base."""
    api = NbApi(**params)
    actual = api.circuits.circuit_terminations.url_base
    assert actual == expected

    nbf = NbForager(**params)
    actual = nbf.api.circuits.circuit_terminations.url_base
    assert actual == expected


# ============================== helper ==============================

@pytest.mark.parametrize("default_get, expected", [
    ({}, {}),
    ({"ipam/prefixes/": {"family": 4}}, {"family": [4]}),
    ({"ipam/prefixes/": {"family": [4, 6]}}, {"family": [4, 6]}),
])
def test__init_default_get(default_get, expected):
    """BaseC._init_default_get()."""
    api = NbApi(host="netbox", default_get=default_get)
    actual = api.ipam.prefixes._default_get
    assert actual == expected

    api.ipam.prefixes.default_get = default_get
    actual = api.ipam.prefixes._init_default_get()
    assert actual == expected

    nbf = NbForager(host="netbox", default_get=default_get)
    actual = nbf.api.ipam.prefixes._default_get
    assert actual == expected


@pytest.mark.parametrize("loners, expected", [
    ({}, ["^q$", "^prefix$"]),
    ({"any": ["a1"], "ipam/aggregates/": ["a2"], "ipam/prefixes/": ["a3"]}, ["a1", "a2"]),
])
def test__init_loners(loners, expected):
    """BaseC._init_loners()."""
    api = NbApi(host="netbox", loners=loners)
    actual = api.ipam.aggregates._loners
    assert actual == expected

    api.ipam.aggregates.loners = loners
    actual = api.ipam.aggregates._init_loners()
    assert actual == expected

    nbf = NbForager(host="netbox", loners=loners)
    actual = nbf.api.ipam.aggregates._loners
    assert actual == expected


@pytest.mark.parametrize("items, expected", [
    ([], None),
    ([{"url": "ipam/prefixes/", "aggregate": {}}], NbApiError),
    ([{"url": "ipam/prefixes/", "id": 1}], None),
])
def test__check_keys(api: NbApi, items, expected: Any):
    """BaseC._check_keys()."""
    if expected is None:
        api.ipam.ip_addresses._check_keys(items=items)
    else:
        with pytest.raises(expected):
            api.ipam.ip_addresses._check_keys(items=items)


@pytest.mark.parametrize("params_d, expected", [
    ({"a": ["A"]}, {"a": ["A"]}),
    ({"a": ["A", "B"]}, {"a": ["A", "B"]}),
    ({"vrf": ["null"]}, {"vrf": ["null"]}),
    ({"vrf": ["typo"]}, {"vrf": ["typo"]}),
    ({"vrf": ["VRF 1"]}, {"vrf_id": [1]}),
    ({"vrf": ["VRF 1", "VRF 2"]}, {"vrf_id": [1, 2]}),
    ({"vrf": ["VRF 1", "typo"]}, {"vrf_id": [1]}),
    ({"vrf": ["typo"]}, {"vrf": ["typo"]}),
    ({"present_in_vrf": ["null"]}, {"present_in_vrf": ["null"]}),
    ({"present_in_vrf": ["VRF 1"]}, {"present_in_vrf_id": [1]}),
    ({"present_in_vrf": ["VRF 1"], "vrf": ["VRF 2"]},
     {"present_in_vrf_id": [1], "vrf_id": [2]}),
])
def test__change_params_name_to_id(
        api: NbApi,
        mock_requests_vrf: Mocker,  # pylint: disable=unused-argument
        params_d: DAny,
        expected: DAny,
):
    """BaseC._change_params_name_to_id()."""
    actual = api.ipam.ip_addresses._change_params_name_to_id(params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("kwargs, status_code, text, error", [
    ({"host": "netbox"}, 200, "", None),
    ({"host": "netbox"}, 400, "", None),
    ({"host": "netbox"}, 500, "any", ConnectionError),
    ({"host": "netbox"}, 403, "Invalid token", ConnectionError),
    ({"host": "netbox", "timeout": 1, "max_retries": 1, "sleep": 1}, 200, "", None),
    # was implemented in old version
    ({"host": "netbox", "timeout": 1, "max_retries": 2, "sleep": 1}, 504, "", ConnectionError),
])
def test__retry_requests(
        monkeypatch: MonkeyPatch,
        kwargs: DAny,
        status_code: int,
        text: str,
        error: Any,
):
    """BaseC._retry_requests()."""
    api = NbApi(**kwargs)
    monkeypatch.setattr(Session, "get", mock_session(status_code, text))
    if error:
        with pytest.raises(error):
            api.ipam.ip_addresses._retry_requests(url="")
    else:
        response = api.ipam.ip_addresses._retry_requests(url="")
        actual = response.status_code
        assert actual == status_code


# ============================= helpers ==============================


@pytest.mark.parametrize("kwargs, expected", [
    ({}, ValueError),
    ({"host": ""}, ValueError),
    ({"host": "netbox"}, "netbox"),
])
def test__init_host(kwargs, expected: Any):
    """base_c._init_host()"""
    if isinstance(expected, str):
        actual = base_c._init_host(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_host(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({}, ValueError),
    ({"scheme": ""}, ValueError),
    ({"scheme": "typo"}, ValueError),
    ({"scheme": "https"}, "https"),
    ({"scheme": "http"}, "http"),
])
def test__init_scheme(kwargs, expected: Any):
    """base_c._init_scheme()"""
    if isinstance(expected, str):
        actual = base_c._init_scheme(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_scheme(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({}, {}),
    ({"a": 1}, {"a": [1]}),
    ({"a": [1, 1]}, {"a": [1]}),
    ({"a": (1, 2)}, {"a": [1, 2]}),
    ({"a": 1, "b": 3}, {"a": [1], "b": [3]}),
])
def test__lists_wo_dupl(kwargs: DAny, expected: LDAny):
    """base_c._lists_wo_dupl()."""
    actual = base_c._lists_wo_dupl(kwargs=kwargs)
    assert actual == expected
