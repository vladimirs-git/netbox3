# pylint: disable=W0212,R0801,W0621

"""Unittests nb_pai.py."""
import inspect

import pytest
import requests_mock
from requests_mock import Mocker

from netbox3 import helpers as h
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


@pytest.fixture
def api():
    """Init API"""
    return NbApi(host="netbox")


@pytest.fixture
def mock_requests_status():
    """Mock request for vrf searching."""
    with requests_mock.Mocker() as mock:
        mock.get("https://netbox/api/status/", json={"netbox-version": "3.6.5"})
        yield mock


def test__app_model(api: NbApi):
    """NbApi has the same models as NbTree object"""
    tree = NbTree()
    for app in tree.apps():
        app_o = getattr(api, app)
        actual = h.attr_name(obj=app_o)
        assert actual == app

        actual = app_o.__class__.__name__
        expected = "".join([f"{s.capitalize()}" for s in app.split("_")]) + "AC"
        assert actual == expected

        for model in getattr(tree, app).models():
            model_o = getattr(app_o, model)
            actual = h.attr_name(model_o)
            assert actual == model

            actual = model_o.__class__.__name__
            expected = "".join([f"{s.capitalize()}" for s in model.split("_")]) + "C"
            assert actual == expected


def test__init__(api: NbApi):
    """NbApi.__init__()."""
    actual = list(inspect.signature(type(api).__init__).parameters)
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
        "kwargs",
    ]
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
])
def test__url(params, expected):
    """NbApi.url."""
    api = NbApi(**params)
    actual = api.url
    assert actual == expected


def test__version(
        api: NbApi,
        mock_requests_status: Mocker,  # pylint: disable=unused-argument
):
    """NbApi.version()."""
    actual = api.version()
    assert actual == "3.6.5"
