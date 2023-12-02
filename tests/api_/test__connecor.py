# pylint: disable=W0212,R0801,W0621

"""Unittests connector.py."""
import json
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch
from requests import Response, Session

from netbox3.nb_api import NbApi
from netbox3.types_ import DAny
from tests.api_.test__base_c import mock_session


@pytest.fixture
def api():
    """Init API"""
    return NbApi(host="netbox")


@pytest.mark.parametrize("data, expected", [
    ({"address": "10.0.0.1/24"}, 201),
    ({}, 400),
])
def test__create(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        data: DAny,
        expected: int,
):
    """Connector._join_params()."""
    monkeypatch.setattr(Session, "post", mock_session(expected))
    response: Response = api.ipam.ip_addresses.create(**data)
    actual = response.status_code
    assert actual == expected


@pytest.mark.parametrize("data, status_code, content", [
    ({"id": 1, "status": "active"}, 201, json.dumps({"id": 1, "status": "active"})),
    ({"id": 9, "status": "active"}, 400, ""),
])
def test__create_d(
        api: NbApi, monkeypatch: MonkeyPatch, data: DAny, status_code: int, content: str
):
    """Connector._join_params()."""
    monkeypatch.setattr(Session, "post", mock_session(status_code, content))
    actual: DAny = api.ipam.ip_addresses.create_d(**data)
    if content:
        assert actual == data
    else:
        assert actual == {}


@pytest.mark.parametrize("data, expected", [
    ({"id": 1, "status": "active"}, 200),
    ({}, ValueError),
])
def test__update(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        data: DAny,
        expected: Any,
):
    """Connector._join_params()."""
    monkeypatch.setattr(Session, "patch", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.ipam.ip_addresses.update(**data)
        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.ipam.ip_addresses.update(**data)


@pytest.mark.parametrize("data, status_code, content", [
    ({"id": 1, "status": "active"}, 200, json.dumps({"id": 1, "status": "active"})),
    ({"id": 9, "status": "active"}, 400, ""),
])
def test__update_d(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        data: DAny,
        status_code: int,
        content: str,
):
    """Connector.update_d()."""
    monkeypatch.setattr(Session, "patch", mock_session(status_code, content))
    actual: DAny = api.ipam.ip_addresses.update_d(**data)
    if content:
        assert actual == data
    else:
        assert actual == {}
