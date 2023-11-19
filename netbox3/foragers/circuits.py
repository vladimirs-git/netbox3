# pylint: disable=R0902,R0903

"""Circuits Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class CircuitsAF(BaseAF):
    """Circuits Forager."""

    def __init__(self, root: NbTree, api: NbApi):
        """Init CircuitsAF.

        :param root: NbTree object where data from Netbox needs to be saved.
        :param api: NbApi object, connector to Netbox API.
        """
        super().__init__(root, api)
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
