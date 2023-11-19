# pylint: disable=R0801
# pylint: disable=R0902,R0913

"""NbForager."""

from __future__ import annotations

import copy
import logging
from datetime import datetime
from pathlib import Path

from vhelpers import vstr

from netbox3 import nb_tree
from netbox3.branch.nb_value import NbValue
from netbox3.foragers.circuits import CircuitsAF
from netbox3.foragers.core import CoreAF
from netbox3.foragers.dcim import DcimAF
from netbox3.foragers.extras import ExtrasAF
from netbox3.foragers.ipam import IpamAF
from netbox3.foragers.tenancy import TenancyAF
from netbox3.foragers.users import UsersAF
from netbox3.foragers.virtualization import VirtualizationAF
from netbox3.foragers.wireless import WirelessAF
from netbox3.messages import Messages
from netbox3.nb_api import NbApi
from netbox3.nb_cache import NbCache
from netbox3.nb_tree import NbTree, insert_tree
from netbox3.types_ import LStr, DAny, DiDAny


class NbForager:
    """Forages data from Netbox for further processing.

    - Requests data from Netbox (using NbApi) and save in the NbForager.root object,
    - Join objects within itself as a multidimensional dictionary in NbForager.tree object,
    - Read/write objects from/to the cache pickle file,
    """

    def __init__(  # pylint: disable=R0914
            self,
            host: str,
            token: str = "",
            scheme: str = "https",
            port: int = 0,
            verify: bool = True,
            limit: int = 1000,
            url_length: int = 2047,
            threads: int = 1,
            interval: float = 0.0,
            # Errors processing
            timeout: int = 60,
            max_retries: int = 1,
            sleep: int = 10,
            cache: str = "",
            **kwargs,
    ):
        """Init NbForager.

        :param cache: Path to cache. If the value ends with .pickle,
            it is the path to a file; otherwise, it is the path to a directory.
            The default value is NbCache.{hostname}.pickle.

        NbApi parameters:

        :param str host: Netbox host name.

        :param str token: Netbox token.

        :param str scheme: Access method: `https` or `http`. Default is `https`.

        :param int port: ``Not implemented`` TCP port. Default is `443`.

        :param bool verify: Transport Layer Security.
            `True` - A TLS certificate required,
            `False` - Requests will accept any TLS certificate.
            Default is `True`.

        :param int limit: Split the query to multiple requests
            if the count of objects exceeds this value. Default is `1000`.

        :param int url_length: Split the query to multiple requests
            if the URL length exceeds maximum length due to a long list of
            GET parameters. Default is `2047`.

        :param int threads: Threads count.
            `1` - Loop mode.
            `2 or higher` -  Threading mode.
            Default is `1`.

        :param float interval: Wait this time between requests (seconds).
            Default is `0`. Useful to optimize session spikes and achieve
            script stability in Docker with limited resources.

        :param int timeout: Session timeout (seconds). Default is `60`.

        :param int max_retries: Retries the request multiple times if
            the Netbox API does not respond or responds with a timeout.
            Default is `0`.

        :param int sleep: Interval (seconds) before the next retry after
            session timeout reached. Default is `10`.

        Data attributes:

        :ivar obj root: :py:class:`NbTree` object that holds raw Netbox objects.
            It is data source for the tree.
        :ivar obj tree: :py:class:`NbTree` object that holds joined Netbox
            objects.
        :ivar dict status: Result from Netbox status endpoint. Netbox version.

        Application/model foragers:

        :ivar obj circuits: :py:class:`.CircuitsAF` :doc:`CircuitsAF`.
        :ivar obj core: :py:class:`.CoreAF` :doc:`CoreAF`.
        :ivar obj dcim: :py:class:`.DcimAF` :doc:`DcimAF`.
        :ivar obj extras: :py:class:`.ExtrasAF` :doc:`ExtrasAF`.
        :ivar obj ipam: :py:class:`.IpamAF` :doc:`IpamAF`.
        :ivar obj tenancy: :py:class:`.TenancyAF` :doc:`TenancyAF`.
        :ivar obj users: :py:class:`.UsersAF` :doc:`UsersAF`.
        :ivar obj virtualization: :py:class:`.VirtualizationAF` :doc:`VirtualizationAF`.
        :ivar obj wireless: :py:class:`.WirelessAF` :doc:`WirelessAF`.
        """
        kwargs = {
            "host": host,
            "token": token,
            "scheme": scheme,
            "port": port,
            "verify": verify,
            "limit": limit,
            "url_length": url_length,
            "threads": threads,
            "interval": interval,
            "timeout": timeout,
            "max_retries": max_retries,
            "sleep": sleep,
            **kwargs,
        }
        # data
        self.root: NbTree = NbTree()  # original data
        self.tree: NbTree = NbTree()  # data with joined objects within itself
        self.status: DAny = {}  # updated Netbox status data

        self.api = NbApi(**kwargs)
        # foragers
        self.circuits = CircuitsAF(self.root, self.api)
        self.core = CoreAF(self.root, self.api)
        self.dcim = DcimAF(self.root, self.api)
        self.extras = ExtrasAF(self.root, self.api)
        self.ipam = IpamAF(self.root, self.api)
        self.tenancy = TenancyAF(self.root, self.api)
        self.users = UsersAF(self.root, self.api)
        self.virtualization = VirtualizationAF(self.root, self.api)
        self.wireless = WirelessAF(self.root, self.api)

        self.cache: str = make_cache_path(cache, **kwargs)
        self.msgs = Messages(name=self.api.host)

    def __repr__(self) -> str:
        """__repr__."""
        attrs = list(NbTree().model_dump())
        params_d = {s: getattr(self, s).count() for s in attrs}
        params = vstr.repr_info(**params_d)
        name = self.__class__.__name__
        return f"<{name}: {params}>"

    def __copy__(self) -> NbForager:
        """Copy NbForager.root and tree objects.

        :return: Copy of NbForager object.
        """
        connector = self.api.circuits.circuits
        params_d = {s: getattr(connector, s) for s in getattr(connector, "_init_params")}
        nbf = NbForager(**params_d)
        insert_tree(src=self.root, dst=nbf.root)
        return nbf

    @property
    def host(self) -> str:
        """Netbox host name."""
        return self.api.host

    @property
    def url(self) -> str:
        """Netbox URL."""
        return self.api.url

    # =========================== method =============================

    def clear(self) -> None:
        """Clear objects by resetting the NbForager.root and NbForager.tree.

        :return: None. Update self object.
        """
        for app in self.root.apps():
            for model in getattr(self.root, app).models():
                data: dict = getattr(getattr(self.root, app), model)
                data.clear()
        self.tree = NbTree()

    def copy(self) -> NbForager:
        """Copy data in the NbForager.root and NbForager.tree.

        :return: Copy of NbForager object.

        :rtype: NbForager
        """
        return copy.copy(self)

    def count(self) -> int:
        """Count of the Netbox objects in the NbForager.root object.

        :return: Count of the Netbox objects.

        :rtype: int
        """
        counts = []
        for app in self.root.apps():
            count = getattr(self, app).count()
            counts.append(count)
        return sum(counts)

    def get_status(self) -> None:
        """Retrieve status from the Netbox, save data to the NbForager.status.

        :return: None. Update self object.
        """
        status = self.api.status.get()
        if not isinstance(status, dict):
            status = {}
        self.status = status

    def grow_tree(self) -> NbTree:
        """Join Netbox objects in NbForager.tree within itself.

        The Netbox objects are represented as a multidimensional dictionary.

        :return: NbTree object with the joined Netbox objects.

        :rtype: NbTree
        """
        self.tree = nb_tree.grow_tree(self.root)
        return self.tree

    def read_cache(self) -> None:
        """Read cached data from a pickle file.

        Save data to the NbForager.root and NbForager.status.

        :return: None. Update self object.
        """
        cache = NbCache(cache=self.cache)
        tree, status = cache.read_cache()
        insert_tree(src=tree, dst=self.root)
        self.status = status

    def write_cache(self) -> None:
        """Write NbForager.root nad NbForager.status to a pickle file.

        :return: None. Update a pickle file.
        """
        status: DAny = self.status.copy()
        status["meta"] = {
            "host": self.api.host,
            "url": self.api.url,
            "write_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }

        cache = NbCache(tree=self.root, status=status, cache=self.cache)
        cache.write_cache()

    def version(self) -> str:
        """Get Netbox version from the NbForager.status.

        Before getting the version, you need to update the NbForager.status by
        using the get_status() or read_cache() method.

        :return: Netbox version if version >= 3, otherwise empty string.
        """
        return str(self.status.get("netbox-version") or "0.0.0")

    # =========================== data methods ===========================

    def _devices_primary_ip4(self) -> LStr:
        """Return the primary IPv4 addresses of Netbox devices with these settings.

        :return: primary_ip4 addresses of devices.
        """
        ip4s: LStr = []
        for device in self.root.dcim.devices.values():  # pylint: disable=E1101
            if ip4 := NbValue(device).primary_ip4():
                ip4s.append(ip4)
        return ip4s

    def _set_ipam_ip_addresses_mask_32(self) -> None:
        """Change mask to /32 for all Netbox ip-addresses.

        :return: None. Update self object.
        """
        for data in self.root.ipam.ip_addresses.values():  # pylint: disable=E1101
            if data["address"].find("/") >= 0:
                ip_ = data["address"].split("/")[0]
                data["address"] = ip_ + "/32"

    def _print_warnings(self) -> None:
        """Print WARNINGS if found some errors/warnings in data processing."""
        for app in self.root.apps():
            for model in getattr(self.root, app).models():
                nb_objects: DiDAny = getattr(getattr(self.root, app), model)
                for nb_object in nb_objects.values():
                    if warnings := nb_object.get("warnings") or []:
                        for warning in warnings:
                            logging.warning(warning)


# noinspection PyIncorrectDocstring
def make_cache_path(cache: str = "", **kwargs) -> str:
    """Make path to pickle file.

    :param cache: Path to pickle file.
    :param name: Parent object name.
    :param host: Netbox host name.

    :return: Path to cache pickle file.
    """
    if cache.endswith(".pickle"):
        return cache
    name = str(kwargs.get("name") or "")
    host = str(kwargs.get("host") or "")
    if not (name or host):
        name = NbCache().__class__.__name__
    file_items = [name, host, "pickle"]
    file_items = [s for s in file_items if s]
    name = ".".join(file_items)
    path = Path(cache, name)
    return str(path)
