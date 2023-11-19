# pylint: disable=R0902,R0903

"""Virtualization connectors."""

from netbox3.api.connector import Connector


class VirtualizationAC:
    """Virtualization connectors."""

    def __init__(self, **kwargs):
        """Init VirtualizationAC."""
        self.cluster_groups = self.ClusterGroupsC(**kwargs)
        self.cluster_types = self.ClusterTypesC(**kwargs)
        self.clusters = self.ClustersC(**kwargs)
        self.interfaces = self.InterfacesC(**kwargs)
        self.virtual_machines = self.VirtualMachinesC(**kwargs)

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.cluster_groups.host}>"

    class ClusterGroupsC(Connector):
        """ClusterGroupsC."""

        path = "virtualization/cluster-groups/"

    class ClusterTypesC(Connector):
        """ClusterTypesC."""

        path = "virtualization/cluster-types/"

    class ClustersC(Connector):
        """ClustersC."""

        path = "virtualization/clusters/"

    class InterfacesC(Connector):
        """InterfacesC."""

        path = "virtualization/interfaces/"

    class VirtualMachinesC(Connector):
        """VirtualMachinesC."""

        path = "virtualization/virtual-machines/"
