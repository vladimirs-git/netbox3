# pylint: disable=W0212,R0801,W0621

"""Unittests helpers.py."""
from typing import Any

import pytest

from netbox3 import helpers as h, NbForager

IP1 = "10.0.0.1/24"
IP2 = "10.0.0.2/24"
IP3 = "10.0.0.3/24"
IP4 = "10.0.0.4/24"


# =========================== app model id ===========================


def test__attr_name():
    """helpers.attr_name()"""
    nbf = NbForager(host="netbox")
    actual = h.attr_name(nbf)
    assert actual == "nb_forager"
    actual = h.attr_name(nbf.ipam)
    assert actual == "ipam"


def test__attr_names():
    """helpers.attr_names()"""
    nbf = NbForager(host="netbox")
    actual = h.attr_names(nbf.wireless)
    expected = ["wireless_lan_groups", "wireless_lans", "wireless_links"]
    assert actual == expected


@pytest.mark.parametrize("urls, expected", [
    ([], []),
    (["a/b/c/d/1"], ["a/b/c/d?id=1"]),
    (["a/b/c/d/2", "a/b/c/d/1"], ["a/b/c/d?id=1&id=2"]),
    (["a/b/c/D/3", "a/b/c/d/2", "a/b/c/d/1"], ["a/b/c/D?id=3", "a/b/c/d?id=1&id=2"]),
    (["a/b/c/d/2", "a/b/c/d/1", "a/b/c/D/3"], ["a/b/c/D?id=3", "a/b/c/d?id=1&id=2"]),
])
def test__join_urls(urls, expected):
    """helpers.join_urls()"""
    actual = h.join_urls(urls=urls)
    assert actual == expected


@pytest.mark.parametrize("model, expected", [
    ("", ""),
    ("prefixes", "prefixes"),
    ("ip-addresses", "ip_addresses"),
    ("ip_addresses", "ip_addresses"),
])
def test__model_to_attr(model, expected):
    """helpers.model_to_attr()"""
    actual = h.model_to_attr(model)
    assert actual == expected

@pytest.mark.parametrize("model, expected", [
    ("", ""),
    ("prefixes", "prefixes"),
    ("ip_addresses", "ip-addresses"),
    ("ip_addresses", "ip-addresses"),
])
def test__attr_to_model(model, expected):
    """helpers.attr_to_model()"""
    actual = h.attr_to_model(model)
    assert actual == expected


@pytest.mark.parametrize("nb_objects, expected", [
    ([], []),
    ([{"url": "a"}], ["a"]),
    ([{"tags": ["a"]}], []),
    ([{"tags": [{"a": "a"}]}], []),
    ([{"tags": [{"url": "a"}]}], ["a"]),
    ([{"tags": {"a": "a"}}], []),
    ([{"tags": {"url": "a"}}], ["a"]),
    ([{"url": "a", "tags": [{"url": "b"}, {"url": "c"}]}], ["a", "b", "c"]),
    ([{"tags": [{"url": "a"}, {"url": "a"}]}], ["a"]),
])
def test__nested_urls(nb_objects, expected):
    """helpers.nested_urls()"""
    actual = h.nested_urls(nb_objects=nb_objects)
    assert actual == expected


@pytest.mark.parametrize("path, expected", [
    ("", ValueError),
    ("typo", ValueError),
    ("app/model", ("app", "model")),
    ("/app/model/", ("app", "model")),
    ("app/model_group", ("app", "model_group")),
    ("app/model-group", ("app", "model_group")),
])
def test__path_to_attrs(path, expected: Any):
    """helpers.path_to_attrs()"""
    if isinstance(expected, tuple):
        actual = h.path_to_attrs(path)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.path_to_attrs(path)


@pytest.mark.parametrize("word, expected", [
    ("", ""),
    ("Text", "text"),
    ("TextText", "text_text"),
    ("TextTextText", "text_text_text"),
])
def test__replace_upper(word, expected):
    """helpers.replace_upper()"""
    actual = h.replace_upper(word)
    assert actual == expected


@pytest.mark.parametrize("url, expected", [
    ("", ("", "", "")),
    ("typo", ("", "", "")),
    ("https://domain.com", ("", "", "")),
    ("https://domain.com/api", ("", "", "")),
    ("https://domain.com/api/app", ("", "", "")),
    ("https://domain.com/api/app/model/model/1", ("", "", "")),
    ("https://domain.com/api/app/model/1/1", ("", "", "")),
    ("https://domain.com/api/app/model", ("app", "model", "")),
    ("https://domain.com/api/app/model/", ("app", "model", "")),
    ("https://domain.com/api/app/model/1", ("app", "model", "1")),
    ("https://domain.com/api/app/model/1/", ("app", "model", "1")),
    ("https://domain.com/api/app/model-group/1", ("app", "model-group", "1")),
    ("https://domain.com/api/app/model/1?key=value", ("app", "model", "1")),
    ("https://domain.com/api/app/model-group/1/", ("app", "model-group", "1")),
])
def test__split_url(url, expected):
    """helpers.split_url()"""
    actual = h.split_url(url=url)
    assert actual == expected


@pytest.mark.parametrize("url, expected", [
    ("", ValueError),
    ("typo", ValueError),
    ("https://domain.com/api/ipam/vrf", "ipam/vrf/"),
    ("https://domain.com/api/ipam/vrf/1?key=value", "ipam/vrf/"),
])
def test__url_to_path(url, expected):
    """helpers.url_to_path()"""
    if isinstance(expected, str):
        actual = h.url_to_path(url=url)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.url_to_path(url=url)


# ============================== params ==============================

@pytest.mark.parametrize("params_ld, default, expected", [
    ([], {}, []),
    ([{}], {}, []),
    ([{"a": ["A2"]}], {}, [{"a": ["A2"]}]),
    ([{"a": ["A2"]}, {"b": ["B2"]}], {}, [{"a": ["A2"]}, {"b": ["B2"]}]),
    ([{"a": ["A2"]}], {"a": ["A1"]}, [{"a": ["A2"]}]),
    ([{"b": ["B2"]}], {"a": ["A1"]}, [{"a": ["A1"], "b": ["B2"]}]),
    ([{"a": ["A2"]}], {"a": ["A1"], "b": ["B1"]}, [{"a": ["A2"], "b": ["B1"]}]),
    ([{"a": ["A2"], "b": ["B2"]}],
     {"a": ["A1"], "b": ["B1"]}, [{"a": ["A2"], "b": ["B2"]}]),
])
def test__join_params(params_ld, default, expected):
    """helpers.join_params()."""
    actual = h.join_params(params_ld=params_ld, default_get=default)
    assert actual == expected


@pytest.mark.parametrize("need_split, params_d, expected", [
    ([], {}, []),

    ([], {"a": [1]}, [{"a": [1]}]),
    ([], {"a": [1, 1]}, [{"a": [1, 1]}]),
    ([], {"a": [1, 2]}, [{"a": [1, 2]}]),
    ([], {"a": [1], "b": [1]}, [{"a": [1], "b": [1]}]),
    ([], {"or_a": [1, 2]}, [{"or_a": [1]}, {"or_a": [2]}]),
    (["a"], {}, []),
    (["a"], {"a": [1, 1]}, [{"a": [1]}, {"a": [1]}]),
    (["a"], {"a": [1, 2]}, [{"a": [1]}, {"a": [2]}]),
    (["a"], {"a": [1], "b": [1]}, [{"a": [1], "b": [1]}]),
    (["a"], {"a": [1, 2], "b": [1]}, [{"a": [1], "b": [1]}, {"a": [2], "b": [1]}]),
    (["a", "b"], {"a": [1, 2], "b": [1, 2]},
     [{"a": [1], "b": [1]}, {"a": [1], "b": [2]}, {"a": [2], "b": [1]}, {"a": [2], "b": [2]}]),
    (["a", "b"], {"a": [1, 2], "b": [1, 2], "c": [1, 2], "d": [1]},
     [{"a": [1], "b": [1], "c": [1, 2], "d": [1]},
      {"a": [1], "b": [2], "c": [1, 2], "d": [1]},
      {"a": [2], "b": [1], "c": [1, 2], "d": [1]},
      {"a": [2], "b": [2], "c": [1, 2], "d": [1]}]),
])
def test__make_combinations(need_split, params_d, expected):
    """helpers.make_combinations()."""
    actual = h.make_combinations(need_split=need_split, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("need_split, params_d, expected", [
    ([], {}, set()),
    ([], {"or_a": [1, 2], "b": [1, 2]}, {"or_a"}),
    (["a"], {"a": [1, 2], "b": [1, 2]}, {"a"}),
])
def test__get_keys_need_split(need_split, params_d, expected):
    """helpers._get_keys_need_split()."""
    actual = h._get_keys_need_split(need_split=need_split, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("params_ld, expected", [
    ([], []),
    ([{"a_or": [1]}], [{"a_or": [1]}]),
    ([{"or_a": [1]}], [{"a": [1]}]),
    ([{"or_a": [1]}, {"or_a": [2]}, {"a_or": [3]}], [{"a": [1]}, {"a": [2]}, {"a_or": [3]}]),
])
def test__change_params_or(params_ld, expected):
    """helpers.change_params_or()."""
    actual = h.change_params_or(params_ld=params_ld)
    assert actual == expected


@pytest.mark.parametrize("max_len, values, expected", [
    (2047, [], [(0, 1)]),
    (2047, [IP1], [(0, 1)]),
    (1, [IP1], [(0, 1)]),
    (1, [IP1, IP2], [(0, 1), (1, 2)]),
    (1, [IP1, IP2, IP3], [(0, 1), (1, 2), (2, 3)]),
    (130, [IP1, IP2, IP3], [(0, 2), (2, 3)]),
    (130, [IP1, IP2, IP3, IP4], [(0, 2), (2, 4)]),
    (145, [IP1, IP2, IP3, IP4], [(0, 3), (3, 4)]),
])
def test__generate_slices(max_len, values, expected):
    """helpers.generate_slices()."""
    actual = h.generate_slices(
        url="https://domain.com",
        max_len=max_len,
        key="address",
        values=values,
        params=[("family", 4), ("status", "active"), ("offset", 1000), ("limit", 1000)],
    )
    assert actual == expected


@pytest.mark.parametrize("url, max_len, key, params_d, expected", [
    ("https://domain.com", 2047, "address", {"address": [IP1, IP2], "family": 4},
     [{"address": [IP1, IP2], "family": 4}]),
    ("https://domain.com", 50, "address", {"address": [IP1, IP2], "family": 4},
     [{"address": IP1, "family": 4}, {"address": IP2, "family": 4}]),
    ("https://domain.com", 50, "prefix", {"prefix": [IP1, IP2], "family": 4},
     [{"prefix": IP1, "family": 4}, {"prefix": IP2, "family": 4}]),
])
def test__slice_params_d(url, max_len, key, params_d, expected):
    """helpers.slice_params_d()."""
    actual = h.slice_params_d(url=url, max_len=max_len, key=key, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("url, max_len, keys, params, expected", [
    ("https://domain.com", 2047, ["address"], [], [{}]),
    ("https://domain.com", 2047, ["address"], [{}], [{}]),  # no need slice
    ("https://domain.com", 50, [], [{"address": [IP1, IP2], "family": [4]}],
     [{"address": [IP1, IP2], "family": [4]}]),  # need slice

    ("https://domain.com", 50, ["prefix"], [{"address": [IP1, IP2], "family": [4]}],
     [{"address": [IP1, IP2], "family": [4]}]),  # no need slice
    ("https://domain.com", 50, ["address"], [{"address": [IP1, IP2], "family": [4]}],
     [{"address": IP1, "family": [4]}, {"address": IP2, "family": [4]}]),  # need slice
])
def test__slice_params_ld(url, max_len, keys, params, expected):
    """helpers.slice_params_ld()."""
    actual = h.slice_params_ld(url=url, max_len=max_len, keys=keys, params_ld=params)
    assert actual == expected


@pytest.mark.parametrize("values, expected", [
    ("", [""]),
    (0, [0]),
    ([], []),
    ([""], [""]),
    ([0], [0]),
    ([1, 2, 1], [1, 2]),
])
def test__validate_values(values, expected):
    """helpers._validate_values()."""
    actual = h._validate_values(values=values)
    assert actual == expected


@pytest.mark.parametrize("params_d, expected", [
    ({}, ""),
    ({"a": [1]}, "a"),
    ({"a": "1"}, "a"),
    ({"a": [100, 200], "b": ["0001", "0002"]}, "b"),
])
def test__get_key_of_longest_value(params_d, expected):
    """helpers.get_key_of_longest_value()."""
    actual = h.get_key_of_longest_value(params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("count, limit, params_d, expected", [
    (10, 10, {}, [{"limit": 10, "offset": 0}]),
    (10, 10, {"a": 1}, [{"a": 1, "limit": 10, "offset": 0}]),
    (20, 10, {}, [{"limit": 10, "offset": 0}, {"limit": 10, "offset": 10}]),
    (0, 10, {}, ValueError),
    (10, 0, {}, ValueError),
])
def test__generate_offsets(count: int, limit: int, params_d, expected: Any):
    """helpers.generate_offsets()."""
    if isinstance(expected, list):
        actual = h.generate_offsets(count, limit, params_d)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.generate_offsets(count, limit, params_d)
