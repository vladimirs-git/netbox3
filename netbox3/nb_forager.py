# pylint: disable=R0801,R0902,R0913,R0914,R0915

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
from netbox3.types_ import LStr, DAny, DiDAny, ODLStr, ODDAny


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
        self.circuits = CircuitsAF(self.root, self.api)
        self.core = CoreAF(self.root, self.api)
        self.dcim = DcimAF(self.root, self.api)
        self.extras = ExtrasAF(self.root, self.api)
        self.ipam = IpamAF(self.root, self.api)
        self.tenancy = TenancyAF(self.root, self.api)
        self.users = UsersAF(self.root, self.api)
        self.virtualization = VirtualizationAF(self.root, self.api)
        self.wireless = WirelessAF(self.root, self.api)

        # model connectors
        # circuits
        self.circuit_terminations = self.circuits.circuit_terminations
        self.circuit_types = self.circuits.circuit_types
        self.circuits_ = self.circuits.circuits  # overlap with self.circuits
        self.provider_accounts = self.circuits.provider_accounts
        self.provider_networks = self.circuits.provider_networks
        self.providers = self.circuits.providers
        # core
        self.data_files = self.core.data_files
        self.data_sources = self.core.data_sources
        self.jobs = self.core.jobs
        # dcim
        self.cable_terminations = self.dcim.cable_terminations
        self.cables = self.dcim.cables
        # connected_device, is not model
        self.console_port_templates = self.dcim.console_port_templates
        self.console_ports = self.dcim.console_ports
        self.console_server_port_templates = self.dcim.console_server_port_templates
        self.console_server_ports = self.dcim.console_server_ports
        self.device_bay_templates = self.dcim.device_bay_templates
        self.device_bays = self.dcim.device_bays
        self.device_roles = self.dcim.device_roles
        self.device_types = self.dcim.device_types
        self.devices = self.dcim.devices
        self.front_port_templates = self.dcim.front_port_templates
        self.front_ports = self.dcim.front_ports
        self.interface_templates = self.dcim.interface_templates
        self.interfaces = self.dcim.interfaces  # overlap with virtualization.interfaces
        self.inventory_item_roles = self.dcim.inventory_item_roles
        self.inventory_item_templates = self.dcim.inventory_item_templates
        self.inventory_items = self.dcim.inventory_items
        self.locations = self.dcim.locations
        self.manufacturers = self.dcim.manufacturers
        self.module_bay_templates = self.dcim.module_bay_templates
        self.module_bays = self.dcim.module_bays
        self.module_types = self.dcim.module_types
        self.modules = self.dcim.modules
        self.platforms = self.dcim.platforms
        self.power_feeds = self.dcim.power_feeds
        self.power_outlet_templates = self.dcim.power_outlet_templates
        self.power_outlets = self.dcim.power_outlets
        self.power_panels = self.dcim.power_panels
        self.power_port_templates = self.dcim.power_port_templates
        self.power_ports = self.dcim.power_ports
        self.rack_reservations = self.dcim.rack_reservations
        self.rack_roles = self.dcim.rack_roles
        self.racks = self.dcim.racks
        self.rear_port_templates = self.dcim.rear_port_templates
        self.rear_ports = self.dcim.rear_ports
        self.regions = self.dcim.regions
        self.site_groups = self.dcim.site_groups
        self.sites = self.dcim.sites
        self.virtual_chassis = self.dcim.virtual_chassis
        self.virtual_device_contexts = self.dcim.virtual_device_contexts
        # extras
        self.bookmarks = self.extras.bookmarks
        self.config_contexts = self.extras.config_contexts
        self.config_templates = self.extras.config_templates
        self.content_types = self.extras.content_types
        self.custom_field_choice_sets = self.extras.custom_field_choice_sets
        self.custom_fields = self.extras.custom_fields
        self.custom_links = self.extras.custom_links
        self.export_templates = self.extras.export_templates
        self.image_attachments = self.extras.image_attachments
        self.journal_entries = self.extras.journal_entries
        self.object_changes = self.extras.object_changes
        self.reports = self.extras.reports
        self.saved_filters = self.extras.saved_filters
        self.scripts = self.extras.scripts
        self.tags = self.extras.tags
        self.webhooks = self.extras.webhooks
        # ipam
        self.aggregates = self.ipam.aggregates
        self.asn_ranges = self.ipam.asn_ranges
        self.asns = self.ipam.asns
        self.fhrp_group_assignments = self.ipam.fhrp_group_assignments
        self.fhrp_groups = self.ipam.fhrp_groups
        self.ip_addresses = self.ipam.ip_addresses
        self.ip_ranges = self.ipam.ip_ranges
        self.l2vpn_terminations = self.ipam.l2vpn_terminations
        self.l2vpns = self.ipam.l2vpns
        self.prefixes = self.ipam.prefixes
        self.rirs = self.ipam.rirs
        self.roles = self.ipam.roles
        self.route_targets = self.ipam.route_targets
        self.service_templates = self.ipam.service_templates
        self.services = self.ipam.services
        self.vlan_groups = self.ipam.vlan_groups
        self.vlans = self.ipam.vlans
        self.vrfs = self.ipam.vrfs
        # tenancy
        self.contact_assignments = self.tenancy.contact_assignments
        self.contact_groups = self.tenancy.contact_groups
        self.contact_roles = self.tenancy.contact_roles
        self.contacts = self.tenancy.contacts
        self.tenant_groups = self.tenancy.tenant_groups
        self.tenants = self.tenancy.tenants
        # users
        self.groups = self.users.groups
        self.permissions = self.users.permissions
        self.tokens = self.users.tokens
        self.users_ = self.users.users  # overlap with self.users
        # virtualization
        self.cluster_groups = self.virtualization.cluster_groups
        self.cluster_types = self.virtualization.cluster_types
        self.clusters = self.virtualization.clusters
        self.interfaces_ = self.virtualization.interfaces  # overlap with dcim.interfaces
        self.virtual_machines = self.virtualization.virtual_machines
        # wireless
        self.wireless_lan_groups = self.wireless.wireless_lan_groups
        self.wireless_lans = self.wireless.wireless_lans
        self.wireless_links = self.wireless.wireless_links

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
