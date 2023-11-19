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
from netbox3.types_ import DAny, LDAny, SeqStr, LStr

# test__validate_concurrent_params
A_1, A_2 = {"a": [1]}, {"a": [2]}
B_1, B_2 = {"b": [1]}, {"b": [2]}
AB_COMBO1 = [{**A_1, **B_1}, {**A_2, **B_1}]
AB_COMBO2 = [{**A_1, **B_1}, {**A_1, **B_2}, {**A_2, **B_1}, {**A_2, **B_2}]


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
    """Connector.url."""
    api = NbApi(**params)
    actual = api.circuits.circuit_terminations.url
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
])
def test__url_base(params, expected):
    """Connector.url_base."""
    api = NbApi(**params)
    actual = api.circuits.circuit_terminations.url_base
    assert actual == expected


# ============================== helper ==============================

@pytest.mark.parametrize("default, params_, expected", [
    ({}, [{}], [{}]),
    ({}, [{"a": "A2"}], [{"a": "A2"}]),
    ({}, [{"a": "A2"}, {"b": "B2"}], [{"a": "A2"}, {"b": "B2"}]),
    ({"a": "A1"}, [{"a": "A2"}], [{"a": "A2"}]),
    ({"a": "A1"}, [{"b": "B2"}], [{"a": "A1", "b": "B2"}]),
    ({"a": "A1", "b": "B1"}, [{"a": "A2"}], [{"a": "A2", "b": "B1"}]),
    ({"a": "A1", "b": "B1"}, [{"a": "A2", "b": "B2"}], [{"a": "A2", "b": "B2"}]),
])
def test__join_params(
        api: NbApi,
        default: DAny,
        params_: LDAny,
        expected: LDAny,
):
    """Connector._join_params()."""
    api.ip_addresses.default = default
    actual = api.ip_addresses._join_params(*params_)
    assert actual == expected


@pytest.mark.parametrize("kwargs, expected", [
    ({}, {}),
    ({"a": 1}, {"a": [1]}),
    ({"a": [1, 1]}, {"a": [1]}),
    ({"a": (1, 2)}, {"a": [1, 2]}),
    ({"a": 1, "b": 3}, {"a": [1], "b": [3]}),
])
def test__lists_wo_dupl(kwargs: DAny, expected: LDAny):
    """Connector._lists_wo_dupl()."""
    actual = base_c._lists_wo_dupl(kwargs=kwargs)
    assert actual == expected


@pytest.mark.parametrize("need_split, params_d, expected", [
    ([], {}, []),
    ([], A_1, [A_1]),
    ([], {"a": [1, 1]}, [{"a": [1, 1]}]),
    ([], {"a": [1, 2]}, [{"a": [1, 2]}]),
    ([], {**A_1, **B_1}, [{**A_1, **B_1}]),
    ([], {"a": [True, True]}, [{"a": [True]}, {"a": [True]}]),
    ([], {"a": [True, False]}, [{"a": [True]}, {"a": [False]}]),
    (["^a"], {}, []),
    (["^a"], A_1, [A_1]),
    (["^a"], {"a": [1, 1]}, [A_1, A_1]),
    (["^a"], {"a": [1, 2]}, [A_1, A_2]),
    (["^a"], {"ab": [1, 2]}, [{"ab": [1]}, {"ab": [2]}]),
    (["^a"], {**A_1, **B_1}, [{**A_1, **B_1}]),
    (["^a"], {**{"a": [1, 2]}, **B_1}, AB_COMBO1),
    (["^a", "^b"], {**{"a": [1, 2]}, **{"b": [1, 2]}}, AB_COMBO2),
    (["^a", "^b"], {**{"a": [1, 2]}, **{"b": [1, 2]}, **{"c": [1, 2], "d": [1]}},
     [{"a": [1], "b": [1], "c": [1, 2], "d": [1]},
      {"a": [1], "b": [2], "c": [1, 2], "d": [1]},
      {"a": [2], "b": [1], "c": [1, 2], "d": [1]},
      {"a": [2], "b": [2], "c": [1, 2], "d": [1]}]),
])
def test__make_combinations(need_split: LStr, params_d: DAny, expected: LDAny):
    """Connector._make_combinations()."""
    actual = base_c._make_combinations(need_split=need_split, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("items, denied, error", [
    ([], [], None),
    ([], ["a"], None),
    ([{}], [], None),
    ([{}], ["a"], None),
    ([{"a": 1}], [], None),
    ([{"a": 1}], ["a"], NbApiError),
    ([{"b": 1}], ["a"], None),
])
def test__check_keys(
        api: NbApi,
        items: LDAny,
        denied: SeqStr,
        error: Any,
):
    """Connector._check_keys()."""
    if error:
        with pytest.raises(error):
            api.ip_addresses._check_keys(items=items, denied=denied)
    else:
        api.ip_addresses._check_keys(items=items, denied=denied)


@pytest.mark.parametrize("params_d, expected", [
    ({"a": "A"}, {"a": "A"}),
    ({"a": ["A", "B"]}, {"a": ["A", "B"]}),
    ({"vrf": "typo"}, {"vrf": "typo"}),
    ({"vrf": "VRF 1"}, {"vrf_id": [1]}),
    ({"vrf": ["VRF 1", "VRF 2"]}, {"vrf_id": [1, 2]}),
    ({"vrf": ["VRF 1", "typo"]}, {"vrf_id": [1]}),
    ({"vrf": ["typo"]}, {"vrf": ["typo"]}),
    ({"present_in_vrf": "VRF 1"}, {"present_in_vrf_id": [1]}),
    ({"present_in_vrf": "VRF 1", "vrf": "VRF 2"}, {"present_in_vrf_id": [1], "vrf_id": [2]}),
])
def test__change_param_name_to_id(
        api: NbApi,
        mock_requests_vrf: Mocker,  # pylint: disable=unused-argument
        params_d: DAny,
        expected: DAny,
):
    """Connector._change_param_name_to_id()."""
    actual = api.ip_addresses._change_param_name_to_id(params_d=params_d)
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
    """Connector._retry_requests()."""
    api = NbApi(**kwargs)
    monkeypatch.setattr(Session, "get", mock_session(status_code, text))
    if error:
        with pytest.raises(error):
            api.ip_addresses._retry_requests(url="")
    else:
        response = api.ip_addresses._retry_requests(url="")
        actual = response.status_code
        assert actual == status_code


# ============================= helpers ==============================

@pytest.mark.parametrize("kwargs, expected", [
    ({}, ValueError),
    ({"host": ""}, ValueError),
    ({"host": "netbox"}, "netbox"),
])
def test__init_host(kwargs, expected: Any):
    """base_c._init_scheme()"""
    if isinstance(expected, str):
        actual = base_c._init_host(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_host(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({}, "https"),
    ({"scheme": ""}, "https"),
    ({"scheme": "https"}, "https"),
    ({"scheme": "http"}, "http"),
    ({"scheme": "typo"}, ValueError),
])
def test__init_scheme(kwargs, expected: Any):
    """base_c._init_scheme()"""
    if isinstance(expected, str):
        actual = base_c._init_scheme(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_scheme(**kwargs)
