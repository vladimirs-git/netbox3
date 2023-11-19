# pylint: disable=W0212,R0801,W0621

"""Unittests cache.py."""
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch, mock_open

import pytest
from _pytest.monkeypatch import MonkeyPatch

from netbox3.nb_cache import NbCache
from netbox3.nb_tree import NbTree
from tests import objects


@pytest.fixture
def tree_meta():
    """Init NbTree and NbMeta objects."""
    tree = NbTree()
    tree.ipam.vrfs.update(objects.vrf_d([1]))  # pylint: disable=E1101

    status = {
        "host": "netbox",
        "url": "https://netbox/api/",
        "write_time": "2000-12-31 23:59:59",
    }
    return tree, status


def test__read_cache(tree_meta):
    """Cache.read_cache()."""
    tree, meta = tree_meta
    assert tree.ipam.vrfs[1]["id"] == 1

    return_value = {
        "tree": tree.model_dump(),
        "status": {"meta": meta},
    }
    patch("pathlib.Path.open", mock_open()).start()

    with patch("pickle.load", return_value=return_value).start():
        cache = NbCache(cache="test")
        tree, status = cache.read_cache()
        assert tree.ipam.vrfs[1]["id"] == 1  # pylint: disable=E1101
        assert status["meta"] == meta

    with pytest.raises(ValueError):
        NbCache().read_cache()


def test__write_cache(tree_meta, monkeypatch: MonkeyPatch):
    """Cache.write_cache()."""
    monkeypatch.setattr(Path, "open", Mock())
    monkeypatch.setattr(NbCache, "_create_dir", Mock())
    monkeypatch.setattr(NbCache, "_create_file", Mock())

    tree, meta = tree_meta
    cache = NbCache(tree=tree, status={"meta": meta}, cache="test")
    cache.write_cache()

    with pytest.raises(ValueError):
        NbCache().write_cache()
