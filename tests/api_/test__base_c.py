# pylint: disable=W0212,R0801,W0621

"""Unittests base_c.py."""
from typing import Any

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from netports import NetportsValueError
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
        response.url = kwargs.get("url", "")
        return response

    return mock


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "http", "port": 80},
     "http://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "http", "port": 1},
     "http://netbox:1/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "https", "port": 443},
     "https://netbox/api/circuits/circuit-terminations/"),
    ({"host": "netbox", "scheme": "https", "port": 1},
     "https://netbox:1/api/circuits/circuit-terminations/"),
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
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
    ({"host": "netbox", "scheme": "http", "port": 80}, "http://netbox/api/"),
    ({"host": "netbox", "scheme": "http", "port": 1}, "http://netbox:1/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https", "port": 443}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https", "port": 1}, "https://netbox:1/api/"),
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


def test__loners(api: NbApi):
    """BaseC._loners default."""
    assert api.dcim.devices._loners == ["q", "airflow"]
    assert api.ipam.aggregates._loners == ["q", "prefix"]
    assert api.ipam.prefixes._loners == ["q", "within_include"]
    assert api.ipam.ip_addresses._loners == ["q"]


@pytest.mark.parametrize("loners, expected", [
    ({}, ["q", "prefix"]),
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
def test__check_reserved_keys__ipam_prefixes(api: NbApi, items, expected: Any):
    """BaseC._check_reserved_keys() ipam/prefixes/."""
    if expected is None:
        api.ipam.prefixes._check_reserved_keys(items=items)
    else:
        with pytest.raises(expected):
            api.ipam.prefixes._check_reserved_keys(items=items)


@pytest.mark.parametrize("items, expected", [
    ([], None),
    ([{"url": "dcim/devices/", "interfaces": {}}], NbApiError),
    ([{"url": "dcim/devices/", "id": 1}], None),
])
def test__check_reserved_keys__dcim_devices(api: NbApi, items, expected: Any):
    """BaseC._check_reserved_keys(). dcim/devices/"""
    if expected is None:
        api.dcim.devices._check_reserved_keys(items=items)
    else:
        with pytest.raises(expected):
            api.dcim.devices._check_reserved_keys(items=items)


@pytest.mark.parametrize("params_d, expected", [
    ({"a": ["A"]}, {"a": ["A"]}),
    ({"a": ["A", "B"]}, {"a": ["A", "B"]}),
    ({"vrf": ["null"]}, {"vrf": ["null"]}),
    ({"vrf": ["typo"]}, {"vrf": ["typo"]}),
    ({"vrf": ["VRF 1"]}, {"vrf_id": [1]}),
    ({"vrf": ["VRF 1", "VRF 2"]}, {"vrf_id": [1, 2]}),
    ({"vrf": ["VRF 1", "typo"]}, {"vrf_id": [1]}),
    ({"vrf": ["typo"]}, {"vrf": ["typo"]}),
    ({"or_vrf": ["VRF 1"]}, {"vrf_id": [1]}),
    ({"or_vrf": ["VRF 1", "VRF 2"]}, {"vrf_id": [1, 2]}),
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
    ({"host": "netbox", "strict": True}, 200, "", None),
    ({"host": "netbox", "strict": False}, 200, "", None),
    ({"host": "netbox", "strict": True}, 400, "", None),
    ({"host": "netbox", "strict": False}, 400, "", ConnectionError),
    ({"host": "netbox", "strict": True}, 500, "any", ConnectionError),
    ({"host": "netbox", "strict": False}, 500, "any", ConnectionError),
    ({"host": "netbox", "strict": True}, 403, "Invalid token", ConnectionError),
    ({"host": "netbox", "strict": False}, 403, "Invalid token", ConnectionError),
    ({"host": "netbox", "timeout": 1, "max_retries": 1, "sleep": 1, "strict": True}, 200, "", None),
    ({"host": "netbox", "timeout": 1, "max_retries": 1, "sleep": 1}, 200, "", None),
    # was implemented in old version
    ({"host": "netbox", "timeout": 1, "max_retries": 2, "sleep": 1, "strict": True}, 504, "",
     ConnectionError),
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

@pytest.mark.parametrize("status_code, text, expected", [
    (400, "text", "status_code=400 text='text' url='netbox'"),
    (400, "<title>Page Not Found. text<title>",
     "status_code=400 text='Page Not Found.' url='netbox'"),
])
def test__msg_status_code(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        status_code: int,
        text: str,
        expected: Any,
):
    """BaseC._msg_status_code()."""
    monkeypatch.setattr(Session, "get", mock_session(status_code, text))
    response: Response = api.ipam.ip_addresses._session.get(url="netbox")
    actual = api.ipam.ip_addresses._msg_status_code(response=response)
    assert actual == expected


def test__msg_status_code__none(api: NbApi):
    """BaseC._msg_status_code()."""
    actual = api.ipam.ip_addresses._msg_status_code(response=None)
    assert actual == ""


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
    ({}, 443),
    ({"port": ""}, 443),
    ({"port": 0}, 443),
    ({"port": -1}, NetportsValueError),
    ({"port": 1}, 1),
    ({"port": "1"}, 1),
    ({"scheme": "typo"}, 443),
    ({"scheme": "http"}, 80),
    ({"scheme": "HTTP"}, 80),
    ({"scheme": "https"}, 443),
    ({"scheme": "HTTPs"}, 443),
    ({"scheme": "http", "port": "1"}, 1),
    ({"scheme": "http", "port": 1}, 1),
    ({"scheme": "https", "port": "1"}, 1),
    ({"scheme": "https", "port": 1}, 1),
    ({"scheme": "typo", "port": "1"}, 1),
])
def test__init_port(kwargs, expected: Any):
    """base_c._init_port()"""
    if isinstance(expected, int):
        actual = base_c._init_port(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_port(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({}, ValueError),
    ({"scheme": ""}, ValueError),
    ({"scheme": "typo"}, ValueError),
    ({"scheme": "http"}, "http"),
    ({"scheme": "HTTP"}, "http"),
    ({"scheme": "https"}, "https"),
    ({"scheme": "HTTPs"}, "https"),
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
