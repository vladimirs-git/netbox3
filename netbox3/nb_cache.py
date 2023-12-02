"""NbCache, Read/write objects from/to the cache pickle file."""

from __future__ import annotations

import logging
import os
import pickle
import re
from pathlib import Path
from typing import Tuple

from netbox3.nb_tree import ONbTree, NbTree
from netbox3.types_ import DAny, ODAny


class NbCache:
    """NbCache, Read/write objects from/to the cache pickle file."""

    def __init__(
        self,
        tree: ONbTree = None,
        status: ODAny = None,
        cache: str = "",
        **kwargs,
    ):
        """Init NbCache.

        :param tree: NbTree object to be cached.
        :param status: Netbox status data with metadata.
        :param cache: Path to the pickle file.
        """
        _ = kwargs  # noqa
        self.tree: NbTree = tree or NbTree()
        self.status: DAny = dict(status or {})
        self.cache = str(cache)

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.cache}>"

    # =========================== method =============================

    def is_cache(self) -> bool:
        """Check if a pickle file is present on disk.

        :return: True if the pickle file is present, False otherwise.
        """
        path = Path(self.cache)
        return path.is_file()

    def read_cache(self) -> Tuple[NbTree, DAny]:
        """Read cached data from a pickle file.

        :return: NbTree object and status data.
        """
        if not self.cache:
            raise ValueError("Path to the pickle file is not specified.")
        cached = self._read_cache()
        tree_d = cached.get("tree") or {}
        tree = NbTree(**tree_d)
        status = dict(cached.get("status") or {})

        msg = f"Cache loaded from path={self.cache}."
        logging.debug(msg)
        return tree, status

    def write_cache(self) -> None:
        """Write cache to a pickle file.

        :return: None. Update a pickle file.
        """
        if not self.cache:
            raise ValueError("Path to the pickle file is not specified.")
        try:
            self._create_dir()
            self._create_file()
        except PermissionError as ex:
            error = f"{type(ex).__name__}: {ex}"
            path = (re.findall(r"(\'.+\')$", str(ex)) or [self.cache])[0]
            cmd = f'"sudo chmod o+rw {path}"'
            msg = f"{error}. Please change permissions by command: {cmd}."
            logging.error(msg)
            raise type(ex)(*ex.args)

        msg = f"Cache saved to path={self.cache}."
        logging.debug(msg)

    # ====================== helpers ======================

    def _create_dir(self) -> None:
        """Create directory for cache if cache file is specified.

        :return: None. Create directory.
        """
        if not self.cache:
            return
        path = Path(self.cache)
        root = path.resolve().parent
        if not root.is_dir():
            root.mkdir(parents=True, exist_ok=True)

    def _create_file(self) -> None:
        """Create pickl file for cache with write permissions 666.

        :return: None. Update pickle file.
        """
        os.umask(0)
        descriptor = os.open(
            path=self.cache,
            flags=(os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
            mode=0o666,
        )
        with open(descriptor, "wb") as fh:
            data = {
                "tree": self.tree.model_dump(),
                "status": self.status,
            }
            pickle.dump(data, fh)

    def _read_cache(self) -> dict:
        """Read cached data from a pickle file.

        :return: The dictionary data from a pickle file.
        """
        path = Path(self.cache)
        try:
            with path.open(mode="rb") as fh:
                data: DAny = dict(pickle.load(fh))
                return data
        except FileNotFoundError as ex:
            if hasattr(ex, "args") and isinstance(ex.args, tuple):
                msgs = [s for s in ex.args if isinstance(s, str)]
                for attr in ["filename", "filename2"]:
                    if hasattr(ex, attr) and getattr(ex, attr):
                        msgs.append(f"{ex.filename}")
                msg = "To create *.pickle file need to execute netbox3 without --cache parameter."
                msgs.append(msg)
                msg = ". ".join(msgs)
                raise FileNotFoundError(msg) from ex
            raise FileNotFoundError(*ex.args) from ex
