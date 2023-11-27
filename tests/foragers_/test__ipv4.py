# pylint: disable=W0212,R0801,W0621

"""Unittests ipv4.py."""
import pytest

from netbox3.foragers.ipv4 import IPv4


def test__init():
    """IPv4.__init__()."""
    ipv4 = IPv4("10.0.0.1/24")
    assert ipv4.ip == "10.0.0.1"
    assert ipv4.ipv4 == "10.0.0.1/24"
    assert ipv4.net == "10.0.0.0/24"
    assert ipv4.prefixlen == 24


@pytest.mark.parametrize("subnet, supernet, expected", [
    ("10.0.0.0/24", "10.0.0.0/23", True),
    ("10.0.0.1/24", "10.0.0.0/23", True),
    ("10.0.0.0/24", "10.0.0.0/24", True),
    ("10.0.0.1/24", "10.0.0.0/24", True),
    ("10.0.0.0/24", "10.0.0.0/25", False),
    ("10.0.0.1/24", "10.0.0.0/25", False),
    ("10.0.0.0/32", "10.0.0.0/32", True),
    ("10.0.0.1/32", "10.0.0.0/32", False),

])
def test__contains__(subnet, supernet, expected):
    """IPv4.__contains__()."""
    actual = IPv4(subnet) in IPv4(supernet)
    assert actual == expected
