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
from netbox3.branch.nb_branch import NbBranch
from netbox3.types_ import ODLStr, ODDAny, DAny


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

        # application connectors
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

    def version(self) -> str:
        """Get Netbox version.

        :return: Netbox version, if version >= 3, otherwise empty string.
        """
        status_d: DAny = self.status.get()
        version = NbBranch(status_d).str("netbox-version")
        return version
