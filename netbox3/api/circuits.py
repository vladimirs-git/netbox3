# pylint: disable=R0902,R0903

"""Circuits connectors."""

from netbox3.api.base_ca import BaseAC
from netbox3.api.connector import Connector


class CircuitsAC(BaseAC):
    """Circuits connectors."""

    def __init__(self, **kwargs):
        """Init CircuitsAC."""
        self.circuit_terminations = self.CircuitTerminationsC(**kwargs)
        self.circuit_types = self.CircuitTypesC(**kwargs)
        self.circuits = self.CircuitsC(**kwargs)
        self.provider_accounts = self.ProviderAccountsC(**kwargs)
        self.provider_networks = self.ProviderNetworksC(**kwargs)
        self.providers = self.ProvidersC(**kwargs)

    class CircuitTerminationsC(Connector):
        """CircuitTerminationsC."""

        path = "circuits/circuit-terminations/"

    class CircuitTypesC(Connector):
        """CircuitTypesC."""

        path = "circuits/circuit-types/"

    class CircuitsC(Connector):
        """CircuitsC."""

        path = "circuits/circuits/"

    class ProviderAccountsC(Connector):
        """ProviderAccountsC."""

        path = "circuits/provider-accounts/"

    class ProviderNetworksC(Connector):
        """ProviderNetworksC."""

        path = "circuits/provider-networks/"

    class ProvidersC(Connector):
        """ProvidersC."""

        path = "circuits/providers/"
