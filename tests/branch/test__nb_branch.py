# pylint: disable=protected-access

"""Unittests nb_branch.py."""
from typing import Any

import pytest

from netbox3.branch.nb_branch import NbBranch
from netbox3.types_ import LStr
from tests import params__nb_branch as p


@pytest.mark.parametrize("keys, data, strict, expected", p.DICT)
def test__dict(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.dict()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, dict):
        actual = branch.dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.dict(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.INT)
def test__int(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.int()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, int):
        actual = branch.int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.int(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.LIST)
def test__list(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.list()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, list):
        actual = branch.list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.list(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STR)
def test__str(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.str()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.str(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_DICT)
def test__strict_dict(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.strict_dict()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, dict):
        actual = branch.strict_dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.strict_dict(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_INT)
def test__strict_int(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.strict_int()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, int):
        actual = branch.strict_int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.strict_int(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_LIST)
def test__strict_list(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.strict_list()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, list):
        actual = branch.strict_list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.strict_list(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_STR)
def test__strict_str(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbBranch.strict_str()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, str):
        actual = branch.strict_str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.strict_str(*keys)


@pytest.mark.parametrize("data, strict, expected", p.TAGS)
def test__tags(data: dict, strict: bool, expected: Any):
    """NbValue.tags()."""
    branch = NbBranch(data=data, strict=strict)
    if isinstance(expected, list):
        actual = branch.tags()
        assert actual == expected
    else:
        with pytest.raises(expected):
            branch.tags()
