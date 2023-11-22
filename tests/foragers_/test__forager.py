# pylint: disable=W0212,R0801,W0621

"""Unittests forager.py."""
from typing import Any, Tuple

import pytest
import requests_mock
from requests_mock import Mocker

from netbox3.nb_forager import NbForager
from netbox3.types_ import LT2StrDAny


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager."""
    return NbForager(host="netbox")


@pytest.fixture
def prepare_connector_results(nbf: NbForager) -> Tuple[NbForager, LT2StrDAny]:
    """Fixture to prepare common connector_results test data."""
    nbf.api.circuits.circuit_terminations._results = [{"url": "circuit/circuit-terminations/1"}]
    nbf.api.ipam.vrfs._results = [{"url": "ipam/vrfs/1"}]
    path_params = [("circuits/circuit-terminations", {"id": [1, 2]}), ("ipam/vrfs", {"id": [1, 2]})]
    return nbf, path_params


def test__interval():
    """Forager._interval()."""
    nbf = NbForager(host="netbox", interval=0.5)
    assert nbf.ipam.vrfs.interval == 0.5
    assert nbf.api.ipam.vrfs.interval == 0.5


def test__threads():
    """Forager._interval()."""
    nbf = NbForager(host="netbox", threads=2)
    assert nbf.ipam.vrfs.threads == 2
    assert nbf.api.ipam.vrfs.threads == 2


def test__count(nbf):
    """Forager.count()."""
    nbf.circuits.circuit_terminations.data.update({1: {}})
    nbf.dcim.device_roles.data.update({1: {}, 2: {}})
    nbf.ipam.aggregates.data.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.data.update({1: {}, 2: {}, 3: {}, 4: {}})

    assert nbf.circuits.circuit_terminations.count() == 1
    assert nbf.circuits.circuit_types.count() == 0
    assert nbf.dcim.device_roles.count() == 2
    assert nbf.dcim.device_types.count() == 0
    assert nbf.ipam.aggregates.count() == 3
    assert nbf.ipam.asn_ranges.count() == 0
    assert nbf.tenancy.tenant_groups.count() == 4
    assert nbf.tenancy.tenants.count() == 0

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.data) == 1
    assert f"{nbf.circuits.circuit_terminations!r}" == "<CircuitTerminationsF: 1>"


@pytest.mark.parametrize("path, expected", [
    ("circuits/circuit-terminations", "CircuitTerminationsC"),
    ("circuits/circuit_terminations", "CircuitTerminationsC"),
    ("circuits/circuits", "CircuitsC"),
    ("typo/circuits", AttributeError),
    ("circuits/typo", AttributeError),
    ("circuits", ValueError),
])
def test__get_connector(nbf, path, expected: Any):
    """Forager._get_connector()."""
    if isinstance(expected, str):
        connector = nbf.ipam.vrfs._get_connector(path)
        actual = connector.__class__.__name__
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf.ipam.vrfs._get_connector(path)


def test__clear_connector_results(prepare_connector_results):
    """Forager._clear_connector_results()."""
    nbf, path_params = prepare_connector_results
    nbf.ipam.vrfs._clear_connector_results(path_params=path_params)
    assert nbf.api.circuits.circuit_terminations._results == []
    assert nbf.api.ipam.vrfs._results == []


def test__pop_connector_results(prepare_connector_results):
    """Forager._pop_connector_results()."""
    nbf, path_params = prepare_connector_results
    actual = nbf.ipam.vrfs._pop_connector_results(path_params=path_params)
    assert actual == [{"url": "circuit/circuit-terminations/1"}, {"url": "ipam/vrfs/1"}]
    assert nbf.api.circuits.circuit_terminations._results == []
    assert nbf.api.ipam.vrfs._results == []


@pytest.mark.parametrize("path, expected", [
    ("circuits/circuit-terminations", "A"),
    ("circuits/circuit_terminations", "A"),
    ("circuits/circuits", "B"),
    ("typo/circuits", AttributeError),
    ("circuits/typo", AttributeError),
    ("circuits", ValueError),
])
def test__get_root_data(nbf, path, expected: Any):
    """Forager._get_root_data()."""
    nbf.root.circuits.circuit_terminations[1] = {"name": "A"}
    nbf.root.circuits.circuits[1] = {"name": "B"}
    if isinstance(expected, str):
        data = nbf.ipam.vrfs._get_root_data(path)
        actual = data[1]["name"]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf.ipam.vrfs._get_connector(path)


@pytest.fixture
def mock_requests_vrfs():
    """Mock Session."""
    rt1 = {"id": 1, "name": "65000:1", "url": "/ipam/route-targets/1"}
    rt2 = {"id": 2, "name": "65000:2", "url": "/ipam/route-targets/2"}
    vrf1 = {"id": 1, "name": "VRF1", "url": "ipam/vrfs/1", "import_targets": [rt1, rt2]}
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://netbox/api/ipam/vrfs/?limit=1000&offset=0",
            json={"results": [vrf1]},
        )
        mock.get(
            "https://netbox/api/ipam/route-targets/?id=1&limit=1000&offset=0",
            json={"results": [rt1]},
        )
        mock.get(
            "https://netbox/api/ipam/route-targets/?id=2&limit=1000&offset=0",
            json={"results": [rt2]},
        )
        yield mock


@pytest.mark.skip(reason="Has blocking effect")
def test__get(mock_requests_vrfs: Mocker):  # pylint: disable=unused-argument
    """Forager.get().

    url_length=1 is required to check slice params and to
    mock 3 requests: ipam/vrfs, ipam/route-targets/?id=1, ipam/route-targets/?id=2.
    """
    nbf = NbForager(host="netbox", url_length=1, threads=2)
    nbf.ipam.vrfs.get()
