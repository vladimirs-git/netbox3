# pylint: disable=R0801,R0902,R0913,R0914,R0915

"""NbForager."""

from __future__ import annotations

import copy
import logging
from datetime import datetime
from operator import itemgetter
from pathlib import Path

from vhelpers import vstr, vlist

from netbox3 import nb_tree
from netbox3.branch.nb_value import NbValue
from netbox3.foragers.circuits import CircuitsAF
from netbox3.foragers.core import CoreAF
from netbox3.foragers.dcim import DcimAF
from netbox3.foragers.extras import ExtrasAF
from netbox3.foragers.ipam import IpamAF
from netbox3.foragers.ipv4 import IPv4
from netbox3.foragers.tenancy import TenancyAF
from netbox3.foragers.users import UsersAF
from netbox3.foragers.virtualization import VirtualizationAF
from netbox3.foragers.wireless import WirelessAF
from netbox3.messages import Messages
from netbox3.nb_api import NbApi
from netbox3.nb_cache import NbCache
from netbox3.nb_tree import NbTree
from netbox3.types_ import LStr, DAny, DiDAny, ODLStr, ODDAny, LDAny, DiLDAny, LInt


class NbForager:
    """Forages data from Netbox for further processing.

    - Requests data from Netbox (using NbApi) and save in the NbForager.root object,
    - Join objects within itself as a multidimensional dictionary in NbForager.tree object,
    - Read/write objects from/to the cache pickle file,
    """

    def __init__(
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
        max_retries: int = 0,
        sleep: int = 10,
        # Settings
        default_get: ODDAny = None,
        loners: ODLStr = None,
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

        :param int threads: Threads count. <=1 is loop mode, >=2 is threading mode.
            Default id `1`.

        :param float interval: Wait this time between the threading requests (seconds).
            Default is `0`. Useful to optimize session spikes and achieve
            script stability in Docker with limited resources.

        :param int timeout: Session timeout (seconds). Default is `60`.

        :param int max_retries: Retries the request multiple times if the Netbox API
            does not respond or responds with a timeout. Default is `0`.

        :param int sleep: Interval (seconds) before the next retry after
            session timeout reached. Default is `10`.

        :param dict default_get: Set default filtering parameters.

        :param dict loners: Set :ref:`Filtering parameters in an OR manner`.

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
            "default_get": default_get,
            "loners": loners,
            **kwargs,
        }
        # data
        self.root: NbTree = NbTree()  # original data
        self.tree: NbTree = NbTree()  # data with joined objects within itself
        self.status: DAny = {}  # updated Netbox status data

        self.api = NbApi(**kwargs)
        self.cache: str = make_cache_path(cache, **kwargs)
        self.msgs = Messages(name=self.api.host)

        # application foragers
        self.circuits = CircuitsAF(self.api, self.root, self.tree)
        self.core = CoreAF(self.api, self.root, self.tree)
        self.dcim = DcimAF(self.api, self.root, self.tree)
        self.extras = ExtrasAF(self.api, self.root, self.tree)
        self.ipam = IpamAF(self.api, self.root, self.tree)
        self.tenancy = TenancyAF(self.api, self.root, self.tree)
        self.users = UsersAF(self.api, self.root, self.tree)
        self.virtualization = VirtualizationAF(self.api, self.root, self.tree)
        self.wireless = WirelessAF(self.api, self.root, self.tree)

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
        nb_tree.insert_tree(src=self.root, dst=nbf.root)
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
        tree = nb_tree.grow_tree(self.root)
        nb_tree.insert_tree(src=tree, dst=self.tree)

        self._extra__ipv4()
        self._extra__ipam_aggregates()
        self._extra__ipam_prefixes()
        self._extra__ipam_ip_addresses()
        self._extra__update_sub_prefixes()
        return self.tree

    def read_cache(self) -> None:
        """Read cached data from a pickle file.

        Save data to the NbForager.root and NbForager.status.

        :return: None. Update self object.
        """
        cache = NbCache(cache=self.cache)
        tree, status = cache.read_cache()
        nb_tree.insert_tree(src=tree, dst=self.root)
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

    # ============================= helpers ==============================

    def _get_ip_addresses_ip4(self) -> LDAny:
        """Return ipam.ip_addresses family=4 sorted by IPv4."""
        ip_addresses = self.ipam.ip_addresses.find_tree(family__value=4, vrf=None)
        return sorted(ip_addresses, key=itemgetter("ipv4"))

    def _get_aggregates_ip4(self) -> LDAny:
        """Return ipam.aggregates family=4 sorted by IPv4."""
        aggregates = self.ipam.aggregates.find_tree(family__value=4)
        return sorted(aggregates, key=itemgetter("ipv4"))

    def _get_prefixes_ip4(self) -> LDAny:
        """Return ipam.prefixes family=4 sorted by IPv4."""
        prefixes = self.ipam.prefixes.find_tree(family__value=4, vrf=None)
        return sorted(prefixes, key=itemgetter("ipv4"))

    def _get_prefixes_ip4_d(self) -> DiLDAny:
        """Split prefixes by depth.

        :return: A dictionary of prefixes where the key represents the depth
            and the value represents a list of prefixes at that depth.
        """
        prefixes: LDAny = self._get_prefixes_ip4()
        prefixes_d: DiLDAny = {d["_depth"]: [] for d in prefixes}
        for prefix in prefixes:
            depth = int(prefix["_depth"])
            prefixes_d[depth].append(prefix)
        return prefixes_d

    def _extra__ipv4(self) -> None:
        for model, key, strict in [
            ("aggregates", "prefix", True),
            ("prefixes", "prefix", True),
            ("ip_addresses", "address", False),
        ]:
            objects: DiDAny = getattr(self.tree.ipam, model)
            for data in objects.values():
                snet = data[key]
                data["ipv4"] = IPv4(snet, strict=strict)
                data["aggregate"] = {}
                data["super_prefix"] = {}
                data["sub_prefixes"] = []
                data["ip_addresses"] = []

    def _extra__ipam_aggregates(self) -> None:
        """Add prefixes to tree.ipam.aggregates.sub_prefixes."""
        aggregates: LDAny = self._get_aggregates_ip4()
        prefixes_d: DiLDAny = self._get_prefixes_ip4_d()
        for aggregate in aggregates:
            for depth, prefixes in prefixes_d.items():
                for prefix in prefixes:
                    _aggregate = aggregate["prefix"]
                    _prefix = prefix["prefix"]
                    if prefix["ipv4"] in aggregate["ipv4"]:
                        prefix["aggregate"] = aggregate
                        if depth == 0:
                            aggregate["sub_prefixes"].append(prefix)

    def _extra__ipam_prefixes(self) -> None:
        """Add prefixes to tree.ipam.prefixes.sub_prefixes, super_prefix"""
        super_prefixes = []
        prefixes_d: DiLDAny = self._get_prefixes_ip4_d()
        for depth, sub_prefixes in enumerate(prefixes_d.values()):
            if not depth:
                super_prefixes = sub_prefixes
                continue
            for super_prefix in super_prefixes:
                if super_prefix["ipv4"].prefixlen == 32:
                    continue
                for sub_prefix in sub_prefixes:
                    if sub_prefix["ipv4"] in (super_prefix["ipv4"]):
                        super_prefix["sub_prefixes"].append(sub_prefix)
                        sub_prefix["super_prefix"] = super_prefix
            super_prefixes = sub_prefixes

    def _extra__ipam_ip_addresses(self) -> None:
        """Add prefixes to tree.ipam.ip-addresses.super_prefix."""
        ip_addresses: LDAny = self._get_ip_addresses_ip4()
        prefixes_d: DiLDAny = self._get_prefixes_ip4_d()
        depths: LInt = list(prefixes_d)
        depths.reverse()

        added_addresses: LDAny = []
        for depth in depths:
            ip_addresses_ = ip_addresses.copy()
            prefixes: LDAny = prefixes_d.get(depth, [])
            for ip_address in ip_addresses_:
                for prefix in prefixes:
                    if ip_address["ipv4"] not in prefix["ipv4"]:
                        continue
                    if ip_address in added_addresses:
                        continue
                    ip_address["aggregate"] = prefix["aggregate"]
                    ip_address["super_prefix"] = prefix
                    prefix["ip_addresses"].append(ip_address)
                    added_addresses.append(ip_address)
            ip_addresses = [d for d in ip_addresses if d not in added_addresses]

    def _extra__update_sub_prefixes(self) -> None:
        """Update sub_prefixes in ipam.aggregates and ipam.prefixes.

        Remove duplicates, remove objects with improper depth, sort by IPv4.
        """
        aggregates = self._get_aggregates_ip4()
        for aggregate in aggregates:
            sub_prefixes = vlist.no_dupl(aggregate["sub_prefixes"])
            sub_prefixes = [d for d in sub_prefixes if not d["super_prefix"]]
            aggregate["sub_prefixes"] = sorted(sub_prefixes, key=itemgetter("ipv4"))

        prefixes = self._get_prefixes_ip4()
        for prefix in prefixes:
            sub_prefixes = vlist.no_dupl(prefix["sub_prefixes"])
            prefix["sub_prefixes"] = sorted(sub_prefixes, key=itemgetter("ipv4"))
            ip_addresses = vlist.no_dupl(prefix["ip_addresses"])
            prefix["ip_addresses"] = sorted(ip_addresses, key=itemgetter("ipv4"))

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
