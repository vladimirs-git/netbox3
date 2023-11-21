# pylint: disable=R0801,R0902,R0913,R0914,R0915

"""NbApi, Python wrapper of Netbox REST API."""

from __future__ import annotations

from netbox3.api.circuits import CircuitsAC
from netbox3.api.core import CoreAC
from netbox3.api.dcim import DcimAC
from netbox3.api.extras import ExtrasAC
from netbox3.api.ipam import IpamAC
from netbox3.api.plugins_ca import PluginsAC
from netbox3.api.status import StatusC
from netbox3.api.tenancy import TenancyAC
from netbox3.api.users import UsersAC
from netbox3.api.virtualization import VirtualizationAC
from netbox3.api.wireless import WirelessAC
from netbox3.types_ import ODLStr, ODDAny


class NbApi:
    """NbApi, Python wrapper of Netbox REST API.

    It is a set of connectors to Netbox endpoints.
    Connectors are nested by principle ``{application}.{model}.{method}``,
    where:

    - **application** can be: ``circuits``, ``dcim``, ``ipam``, etc.;
    - **model** can be: ``circuit_terminations``, ``ip_addresses``, etc.;
    - **method** can be: ``create``, ``delete``, ``get``, ``update``.

    For example https://demo.netbox.dev/api/ipam/ip-addresses/
    can be reached by ``NbApi.ipam.ip_addresses.get()`` method.

    Replaces an error-400 response with an empty result.
    For example, when querying some objects by tag, if there are no tag in
    Netbox, the default Netbox API response is error-400 (For what reason do we
    need to handle exceptions in every request?). This tool logs a warning
    message and returns an ok-200 response with an empty list.

    Retries the request multiple times if the Netbox API does not respond or
    responds with a timeout.
    This is useful for scheduled scripts in cron jobs, when the
    connection to Netbox server is not stable (I am a network engineer,
    and my scripts should remain stable even when the network is unstable).

    The parameters for the ``create``, ``delete``, ``update`` methods are
    identical in all models.
    The parameters for the ``get`` method are different for each model.
    Only ``NbApi.ipam.ip_addresses.get()`` is described in this documentation.
    Other models are implemented in a similar manner.
    """

    def __init__(
        self,
        host: str,
        token: str = "",
        scheme: str = "https",
        port: int = 0,  # Not implemented
        verify: bool = True,
        limit: int = 1000,
        url_length: int = 2047,
        # Multithreading
        threads: int = 1,
        interval: float = 0.0,
        # Errors processing
        timeout: int = 60,
        max_retries: int = 0,
        sleep: int = 10,
        # Settings
        default_get: ODDAny = None,
        loners: ODLStr = None,
        **kwargs,
    ):
        """Init NbApi.

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

        :param dict default_get: Set default filtering parameters.

        :param dict loners: Set :ref:`Filtering parameters by multiple values`.

        Application/model connectors:

        :ivar obj circuits: :py:class:`.CircuitsAC` :doc:`CircuitsAC`.
        :ivar obj core: :py:class:`.CoreAC` :doc:`CoreAC`.
        :ivar obj dcim: :py:class:`.DcimAC` :doc:`DcimAC`.
        :ivar obj extras: :py:class:`.ExtrasAC` :doc:`ExtrasAC`.
        :ivar obj ipam: :py:class:`.IpamAC` :doc:`IpamAC`.
        :ivar obj plugins: :py:class:`.PluginsAC` :doc:`PluginsAC`.
        :ivar obj tenancy: :py:class:`.TenancyAC` :doc:`TenancyAC`.
        :ivar obj users: :py:class:`.UsersAC` :doc:`UsersAC`.
        :ivar obj virtualization: :py:class:`.VirtualizationAC` :doc:`VirtualizationAC`.
        :ivar obj wireless: :py:class:`.WirelessAC` :doc:`WirelessAC`.
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

        # applications
        self.circuits = CircuitsAC(**kwargs)
        self.core = CoreAC(**kwargs)
        self.dcim = DcimAC(**kwargs)
        self.extras = ExtrasAC(**kwargs)
        self.ipam = IpamAC(**kwargs)
        self.plugins = PluginsAC(**kwargs)
        self.status = StatusC(**kwargs)  # connector
        self.tenancy = TenancyAC(**kwargs)
        self.users = UsersAC(**kwargs)
        self.virtualization = VirtualizationAC(**kwargs)
        self.wireless = WirelessAC(**kwargs)

        # models
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
        # plugins
        self.installed_plugins = self.plugins.installed_plugins
        # tenancy
        self.contact_assignments = self.tenancy.contact_assignments
        self.contact_groups = self.tenancy.contact_groups
        self.contact_roles = self.tenancy.contact_roles
        self.contacts = self.tenancy.contacts
        self.tenant_groups = self.tenancy.tenant_groups
        self.tenants = self.tenancy.tenants
        # users
        self.config = self.users.config
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
        name = self.__class__.__name__
        return f"<{name}: {self.host}>"

    @property
    def host(self) -> str:
        """Netbox host name."""
        return self.circuits.circuit_terminations.host

    @property
    def url(self) -> str:
        """Netbox base URL."""
        return self.circuits.circuit_terminations.url_base
