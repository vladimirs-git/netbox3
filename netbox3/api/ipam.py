# pylint: disable=R0902,R0903

"""IPAM connectors."""
from netbox3.api.connector import Connector
from netbox3.api.ip_addresses import IpAddressesC


class IpamAC:
    """IPAM connectors."""

    def __init__(self, **kwargs):
        """Init IpamAC."""
        self.aggregates = self.AggregatesC(**kwargs)
        self.asn_ranges = self.AsnRangesC(**kwargs)
        self.asns = self.AsnsC(**kwargs)
        self.fhrp_group_assignments = self.FhrpGroupAssignmentsC(**kwargs)
        self.fhrp_groups = self.FhrpGroupsC(**kwargs)
        self.ip_addresses = IpAddressesC(**kwargs)
        self.ip_ranges = self.IpRangesC(**kwargs)
        self.l2vpn_terminations = self.L2vpnTerminationsC(**kwargs)
        self.l2vpns = self.L2vpnsC(**kwargs)
        self.prefixes = self.PrefixesC(**kwargs)
        self.rirs = self.RirsC(**kwargs)
        self.roles = self.RolesC(**kwargs)
        self.route_targets = self.RouteTargetsC(**kwargs)
        self.service_templates = self.ServiceTemplatesC(**kwargs)
        self.services = self.ServicesC(**kwargs)
        self.vlan_groups = self.VlanGroupsC(**kwargs)
        self.vlans = self.VlansC(**kwargs)
        self.vrfs = self.VrfsC(**kwargs)

    class AggregatesC(Connector):
        """AggregatesC."""

        path = "ipam/aggregates/"

    class AsnRangesC(Connector):
        """AsnRangesC."""

        path = "ipam/asn-ranges/"

    class AsnsC(Connector):
        """AsnsC."""

        path = "ipam/asns/"

    class FhrpGroupAssignmentsC(Connector):
        """FhrpGroupAssignmentsC."""

        path = "ipam/fhrp-group-assignments/"

    class FhrpGroupsC(Connector):
        """FhrpGroupsC."""

        path = "ipam/fhrp-groups/"

    class IpRangesC(Connector):
        """IpRangesC."""

        path = "ipam/ip-ranges/"

    class L2vpnTerminationsC(Connector):
        """L2vpnTerminationsC."""

        path = "ipam/l2vpn-terminations/"

    class L2vpnsC(Connector):
        """L2vpnsC."""

        path = "ipam/l2vpns/"

    class PrefixesC(Connector):
        """PrefixesC."""

        path = "ipam/prefixes/"

    class RirsC(Connector):
        """RirsC."""

        path = "ipam/rirs/"

    class RolesC(Connector):
        """RolesC."""

        path = "ipam/roles/"

    class RouteTargetsC(Connector):
        """RouteTargetsC."""

        path = "ipam/route-targets/"

    class ServiceTemplatesC(Connector):
        """ServiceTemplatesC."""

        path = "ipam/service-templates/"

    class ServicesC(Connector):
        """ServicesC."""

        path = "ipam/services/"

    class VlanGroupsC(Connector):
        """VlanGroupsC."""

        path = "ipam/vlan-groups/"

    class VlansC(Connector):
        """VlansC."""

        path = "ipam/vlans/"

    class VrfsC(Connector):
        """VrfsC."""

        path = "ipam/vrfs/"
