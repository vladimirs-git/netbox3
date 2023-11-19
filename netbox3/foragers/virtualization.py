# pylint: disable=R0902,R0903

"""Tenancy Virtualization."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class VirtualizationAF(BaseAF):
    """Virtualization Virtualization."""

    def __init__(self, root: NbTree, api: NbApi):
        """Init VirtualizationAF.

        :param root: NbTree object where data from Netbox needs to be saved.
        :param api: NbApi object, connector to Netbox API.
        """
        super().__init__(root, api)
        self.cluster_groups = self.ClusterGroupsF(self)
        self.cluster_types = self.ClusterTypesF(self)
        self.clusters = self.ClustersF(self)
        self.interfaces = self.InterfacesF(self)
        self.virtual_machines = self.VirtualMachinesF(self)

    class ClusterGroupsF(Forager):
        """ClusterGroupsF."""

    class ClusterTypesF(Forager):
        """ClusterTypesF."""

    class ClustersF(Forager):
        """ClustersF."""

    class InterfacesF(Forager):
        """InterfacesF."""

    class VirtualMachinesF(Forager):
        """VirtualMachinesF."""
