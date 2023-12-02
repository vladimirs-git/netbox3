# pylint: disable=E1101,W0212,R0801,W0621

"""Unittests forager.py."""
from typing import Any, Tuple

import pytest
import requests_mock
from requests_mock import Mocker

from netbox3 import nb_tree
from netbox3.nb_forager import NbForager
from netbox3.types_ import LT2StrDAny
from tests.objects import full_tree


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager without data."""
    return NbForager(host="netbox")


@pytest.fixture
def nbf_r() -> NbForager:
    """Init NbForager with NbForager.root data."""
    nbf_ = NbForager(host="netbox")
    nb_tree.insert_tree(src=full_tree(), dst=nbf_.root)
    return nbf_


@pytest.fixture
def nbf_t() -> NbForager:
    """Init NbForager."""
    nbf_ = NbForager(host="netbox")
    nb_tree.insert_tree(src=full_tree(), dst=nbf_.tree)
    return nbf_


FIND = [
    ({}, [1, 2, 3]),
    ({"id": 1}, [1]),
    ({"id": 9}, []),
    ({"id": [1, 2, 9]}, [1, 2]),  # list
    ({"id": (1, 2, 9)}, [1, 2]),  # tuple
    ({"id": {1, 2, 9}}, [1, 2]),  # set
    ({"name": "DEVICE1"}, [1]),
    ({"name": ["DEVICE1", "DEVICE2", "typo"]}, [1, 2]),
    ({"serial": "SERIAL1"}, [1, 3]),
    ({"name": "DEVICE1", "serial": "SERIAL1"}, [1]),
    ({"name": "DEVICE1", "serial": "SERIAL2"}, []),
    ({"name": ["DEVICE1", "DEVICE3"], "serial": ["SERIAL1", "typo"]}, [1, 3]),
    ({"name": ["DEVICE1", "DEVICE2"], "serial": ["SERIAL1", "SERIAL2"]}, [1, 2]),
    ({"name": ["DEVICE1", "DEVICE3"], "serial": ["SERIAL1", "SERIAL2"]}, [1, 3]),
    # "__"
    ({"device_type__name": "MODEL1"}, [1, 2]),
    ({"device_type__name": "MODEL3"}, [3]),
    ({"device_type__name_typo": "MODEL3"}, []),
    ({"device_type__name": ["MODEL1", "MODEL3"], "serial": ["SERIAL1"]}, [1, 3]),
    ({"device_type__name": ["MODEL1", "MODEL3"], "serial": ["SERIAL2"]}, [2]),
    ({"device_type__name": ["MODEL1", "MODEL3"], "serial": ["SERIAL1", "SERIAL2"]}, [1, 2, 3]),
    # tags
    ({"tags__name": "TAG1"}, [1, 2]),
    ({"tags__name": ["TAG3"]}, [3]),
    ({"tags__name__typo": "TAG3"}, ValueError),
]


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


def test__count(nbf: NbForager):
    """Forager.count()."""
    nbf.circuits.circuit_terminations.root_d.update({1: {}})
    nbf.dcim.device_roles.root_d.update({1: {}, 2: {}})
    nbf.ipam.aggregates.root_d.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.root_d.update({1: {}, 2: {}, 3: {}, 4: {}})

    assert nbf.circuits.circuit_terminations.count() == 1
    assert nbf.circuits.circuit_types.count() == 0
    assert nbf.dcim.device_roles.count() == 2
    assert nbf.dcim.device_types.count() == 0
    assert nbf.ipam.aggregates.count() == 3
    assert nbf.ipam.asn_ranges.count() == 0
    assert nbf.tenancy.tenant_groups.count() == 4
    assert nbf.tenancy.tenants.count() == 0

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.root_d) == 1
    assert f"{nbf.circuits.circuit_terminations!r}" == "<CircuitTerminationsF: 1>"


@pytest.mark.parametrize("path, expected", [
    ("circuits/circuit-terminations", "CircuitTerminationsC"),
    ("circuits/circuit_terminations", "CircuitTerminationsC"),
    ("circuits/circuits", "CircuitsC"),
    ("typo/circuits", AttributeError),
    ("circuits/typo", AttributeError),
    ("circuits", ValueError),
])
def test__get_connector(nbf: NbForager, path, expected: Any):
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
def test__get_root_data(nbf: NbForager, path, expected: Any):
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


@pytest.mark.parametrize("params, expected", FIND)
def test__find_root(nbf_r: NbForager, params, expected: Any):
    """Forager.find_root().

    NbForager.tree and NbForager.root has 3 devices: DEVICE1, DEVICE2, DEVICE3.
    DEVICE1 has: tags=TAG1, device_role=DEVICE ROLE1, serial=SERIAL1
    DEVICE2 has: tags=TAG1, device_role=DEVICE ROLE1, serial=SERIAL2
    DEVICE3 has: tags=TAG3, device_role=DEVICE ROLE3, serial=SERIAL1
    """
    if isinstance(expected, list):
        results = nbf_r.dcim.devices.find_root(**params)
        actual = [d["id"] for d in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf_r.dcim.devices.find_root(**params)


@pytest.mark.parametrize("params, expected", FIND)
def test__find_tree(nbf_t: NbForager, params, expected):
    """Forager.find_tree()."""
    if isinstance(expected, list):
        results = nbf_t.dcim.devices.find_tree(**params)
        actual = [d["id"] for d in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf_t.dcim.devices.find_tree(**params)


@pytest.mark.parametrize("params, expected", [
    # 1 param
    ({}, [1, 2, 3, 4, 5]),
    ({"role": "role1"}, [1, 4]),
    ({"role": "role2"}, [5]),
    ({"role": "role3"}, [3]),
    ({"role": "role4"}, []),
    ({"site": "site1"}, [1]),
    ({"site": "site2"}, [4, 5]),
    ({"site": "site3"}, [3]),
    ({"site": "site4"}, []),
    ({"env": "ENV1"}, [1, 4]),
    ({"env": "ENV2"}, [5]),
    ({"env": "ENV3"}, [3]),
    ({"env": "ENV4"}, []),
    # 2 params
    ({"role": "role1", "site": "site1"}, [1]),
    ({"role": "role1", "site": "site2"}, [4]),
    ({"role": "role1", "site": "site3"}, []),
    ({"role": "role2", "site": "site1"}, []),
    ({"role": "role2", "site": "site2"}, [5]),
    ({"role": "role2", "site": "site3"}, []),
    ({"role": "role3", "site": "site1"}, []),
    ({"role": "role3", "site": "site2"}, []),
    ({"role": "role3", "site": "site3"}, [3]),
    ({"role": "role1", "env": "ENV1"}, [1, 4]),
    ({"role": "role1", "env": "ENV2"}, []),
    ({"role": "role1", "env": "ENV3"}, []),
    ({"role": "role2", "env": "ENV1"}, []),
    ({"role": "role2", "env": "ENV2"}, [5]),
    ({"role": "role2", "env": "ENV3"}, []),
    ({"role": "role3", "env": "ENV1"}, []),
    ({"role": "role3", "env": "ENV2"}, []),
    ({"role": "role3", "env": "ENV3"}, [3]),
    ({"site": "site1", "env": "ENV1"}, [1]),
    ({"site": "site1", "env": "ENV2"}, []),
    ({"site": "site1", "env": "ENV3"}, []),
    ({"site": "site2", "env": "ENV1"}, [4]),
    ({"site": "site2", "env": "ENV2"}, [5]),
    ({"site": "site2", "env": "ENV3"}, []),
    # 3 params
    ({"role": "role1", "site": "site1", "env": "ENV1"}, [1]),
    ({"role": "role1", "site": "site1", "env": "ENV2"}, []),
    ({"role": "role1", "site": "site1", "env": "ENV3"}, []),
    ({"role": "role1", "site": "site2", "env": "ENV1"}, [4]),
    ({"role": "role1", "site": "site2", "env": "ENV2"}, []),
    ({"role": "role1", "site": "site2", "env": "ENV3"}, []),
    ({"role": "role2", "site": "site1", "env": "ENV1"}, []),
    ({"role": "role2", "site": "site1", "env": "ENV2"}, []),
    ({"role": "role2", "site": "site1", "env": "ENV3"}, []),
    ({"role": "role2", "site": "site2", "env": "ENV1"}, []),
    ({"role": "role2", "site": "site2", "env": "ENV2"}, [5]),
    ({"role": "role2", "site": "site2", "env": "ENV3"}, []),
])
def test__find_rse(nbf_t: NbForager, params, expected: Any):
    """Forager.find_rse()."""
    if isinstance(expected, list):
        results = nbf_t.ipam.prefixes.find_rse(**params)
        actual = [d["id"] for d in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf_t.ipam.prefixes.find_rse(**params)
