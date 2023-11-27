# pylint: disable=R0902,R0903

"""Circuits Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class CircuitsAF(BaseAF):
    """Circuits Forager."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init CircuitsAF.

        :param api: NbApi object, connector to Netbox API.
        :param root: NbTree object where raw data from Netbox needs to be saved.
        :param tree: NbTree object where transformed data from Netbox needs to be saved.
        """
        super().__init__(api, root, tree)
        self.circuit_terminations = self.CircuitTerminationsF(self)
        self.circuit_types = self.CircuitTypesF(self)
        self.circuits = self.CircuitsF(self)
        self.provider_accounts = self.ProviderAccountsF(self)
        self.provider_networks = self.ProviderNetworksF(self)
        self.providers = self.ProvidersF(self)

    class CircuitTerminationsF(Forager):
        """CircuitTerminationsF."""

    class CircuitTypesF(Forager):
        """CircuitTypesF."""

    class CircuitsF(Forager):
        """CircuitsF."""

    class ProviderAccountsF(Forager):
        """ProviderAccountsF."""

    class ProviderNetworksF(Forager):
        """ProviderNetworksF."""

    class ProvidersF(Forager):
        """ProvidersF."""
