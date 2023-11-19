# pylint: disable=protected-access

"""Unittests nb_branch.py."""
from typing import Any

import pytest

from netbox3.branch.nb_custom import NbCustom
from tests import params__nb_branch as p


@pytest.mark.parametrize("data, strict, expected", p.HOSTS_IN_CF_FIREWALLS)
def test__hosts_in_cf_firewalls(data: dict, strict: bool, expected: Any):
    """NbCustom._hosts_in_cf_firewalls()."""
    branch = NbCustom(data=data, strict=strict)
    if isinstance(expected, set):
        actual = branch._hosts_in_cf_firewalls()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch._hosts_in_cf_firewalls()


@pytest.mark.parametrize("data, strict, expected", p.HOSTS_IN_AGGR_DESCR)
def test__hosts_in_aggr_descr(data: dict, strict: bool, expected: Any):
    """NbCustom._hosts_in_aggr_descr()."""
    branch = NbCustom(data=data, strict=strict)
    if isinstance(expected, set):
        actual = branch._hosts_in_aggr_descr()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch._hosts_in_aggr_descr()


@pytest.mark.parametrize("data, strict, expected", p.FIREWALLS__IN_AGGREGATE)
def test__firewalls__in_aggregate(data: dict, strict: bool, expected: Any):
    """NbCustom.firewalls__in_aggregate()."""
    branch = NbCustom(data=data, strict=strict)
    if isinstance(expected, set):
        actual = branch.firewalls__in_aggregate()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.firewalls__in_aggregate()
