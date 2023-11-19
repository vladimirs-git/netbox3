# pylint: disable=R0902,R0903

"""DCIM Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class DcimAF(BaseAF):
    """DCIM Forager."""

    def __init__(self, root: NbTree, api: NbApi):
        """Init DcimAF.

        :param root: NbTree object where data from Netbox needs to be saved.
        :param api: NbApi object, connector to Netbox API.
        """
        super().__init__(root, api)
        self.cable_terminations = self.CableTerminationsF(self)
        self.cables = self.CablesF(self)
        # connected_device, is not model
        self.console_port_templates = self.ConsolePortTemplatesF(self)
        self.console_ports = self.ConsolePortsF(self)
        self.console_server_port_templates = self.ConsoleServerPortTemplatesF(self)
        self.console_server_ports = self.ConsoleServerPortsF(self)
        self.device_bay_templates = self.DeviceBayTemplatesF(self)
        self.device_bays = self.DeviceBaysF(self)
        self.device_roles = self.DeviceRolesF(self)
        self.device_types = self.DeviceTypesF(self)
        self.devices = self.DevicesF(self)
        self.front_port_templates = self.FrontPortTemplatesF(self)
        self.front_ports = self.FrontPortsF(self)
        self.interface_templates = self.InterfaceTemplatesF(self)
        self.interfaces = self.InterfacesF(self)
        self.inventory_item_roles = self.InventoryItemRolesF(self)
        self.inventory_item_templates = self.InventoryItemTemplatesF(self)
        self.inventory_items = self.InventoryItemsF(self)
        self.locations = self.LocationsF(self)
        self.manufacturers = self.ManufacturersF(self)
        self.module_bay_templates = self.ModuleBayTemplatesF(self)
        self.module_bays = self.ModuleBaysF(self)
        self.module_types = self.ModuleTypesF(self)
        self.modules = self.ModulesF(self)
        self.platforms = self.PlatformsF(self)
        self.power_feeds = self.PowerFeedsF(self)
        self.power_outlet_templates = self.PowerOutletTemplatesF(self)
        self.power_outlets = self.PowerOutletsF(self)
        self.power_panels = self.PowerPanelsF(self)
        self.power_port_templates = self.PowerPortTemplatesF(self)
        self.power_ports = self.PowerPortsF(self)
        self.rack_reservations = self.RackReservationsF(self)
        self.rack_roles = self.RackRolesF(self)
        self.racks = self.RacksF(self)
        self.rear_port_templates = self.RearPortTemplatesF(self)
        self.rear_ports = self.RearPortsF(self)
        self.regions = self.RegionsF(self)
        self.site_groups = self.SiteGroupsF(self)
        self.sites = self.SitesF(self)
        self.virtual_chassis = self.VirtualChassisF(self)
        self.virtual_device_contexts = self.VirtualDeviceContextsF(self)

    class CableTerminationsF(Forager):
        """CableTerminationsF."""

    class CablesF(Forager):
        """CablesF."""

    class ConsolePortTemplatesF(Forager):
        """ConsolePortTemplatesF."""

    class ConsolePortsF(Forager):
        """ConsolePortsF."""

    class ConsoleServerPortTemplatesF(Forager):
        """ConsoleServerPortTemplatesF."""

    class ConsoleServerPortsF(Forager):
        """ConsoleServerPortsF."""

    class DeviceBayTemplatesF(Forager):
        """DeviceBayTemplatesF."""

    class DeviceBaysF(Forager):
        """DeviceBaysF."""

    class DeviceRolesF(Forager):
        """DeviceRolesF."""

    class DeviceTypesF(Forager):
        """DeviceTypesF."""

    class DevicesF(Forager):
        """DevicesF."""

    class FrontPortTemplatesF(Forager):
        """FrontPortTemplatesF."""

    class FrontPortsF(Forager):
        """FrontPortsF."""

    class InterfaceTemplatesF(Forager):
        """InterfaceTemplatesF."""

    class InterfacesF(Forager):
        """InterfacesF."""

    class InventoryItemRolesF(Forager):
        """InventoryItemRolesF."""

    class InventoryItemTemplatesF(Forager):
        """InventoryItemTemplatesF."""

    class InventoryItemsF(Forager):
        """InventoryItemsF."""

    class LocationsF(Forager):
        """LocationsF."""

    class ManufacturersF(Forager):
        """ManufacturersF."""

    class ModuleBayTemplatesF(Forager):
        """ModuleBayTemplatesF."""

    class ModuleBaysF(Forager):
        """ModuleBaysF."""

    class ModuleTypesF(Forager):
        """ModuleTypesF."""

    class ModulesF(Forager):
        """ModulesF."""

    class PlatformsF(Forager):
        """PlatformsF."""

    class PowerFeedsF(Forager):
        """PowerFeedsF."""

    class PowerOutletTemplatesF(Forager):
        """PowerOutletTemplatesF."""

    class PowerOutletsF(Forager):
        """PowerOutletsF."""

    class PowerPanelsF(Forager):
        """PowerPanelsF."""

    class PowerPortTemplatesF(Forager):
        """PowerPortTemplatesF."""

    class PowerPortsF(Forager):
        """PowerPortsF."""

    class RackReservationsF(Forager):
        """RackReservationsF."""

    class RackRolesF(Forager):
        """RackRolesF."""

    class RacksF(Forager):
        """RacksF."""

    class RearPortTemplatesF(Forager):
        """RearPortTemplatesF."""

    class RearPortsF(Forager):
        """RearPortsF."""

    class RegionsF(Forager):
        """RegionsF."""

    class SiteGroupsF(Forager):
        """SiteGroupsF."""

    class SitesF(Forager):
        """SitesF."""

    class VirtualChassisF(Forager):
        """VirtualChassisF."""

    class VirtualDeviceContextsF(Forager):
        """VirtualDeviceContextsF."""
