# pylint: disable=R0902,R0903

"""DCIM connectors."""

from netbox3.api.connector import Connector


class DcimAC:
    """DCIM connectors."""

    def __init__(self, **kwargs):
        """Init DcimAC."""
        self.cable_terminations = self.CableTerminationsC(**kwargs)
        self.cables = self.CablesC(**kwargs)
        self.connected_device = self.ConnectedDeviceC(**kwargs)
        self.console_port_templates = self.ConsolePortTemplatesC(**kwargs)
        self.console_ports = self.ConsolePortsC(**kwargs)
        self.console_server_port_templates = self.ConsoleServerPortTemplatesC(**kwargs)
        self.console_server_ports = self.ConsoleServerPortsC(**kwargs)
        self.device_bay_templates = self.DeviceBayTemplatesC(**kwargs)
        self.device_bays = self.DeviceBaysC(**kwargs)
        self.device_roles = self.DeviceRolesC(**kwargs)
        self.device_types = self.DeviceTypesC(**kwargs)
        self.devices = self.DevicesC(**kwargs)
        self.front_port_templates = self.FrontPortTemplatesC(**kwargs)
        self.front_ports = self.FrontPortsC(**kwargs)
        self.interface_templates = self.InterfaceTemplatesC(**kwargs)
        self.interfaces = self.InterfacesC(**kwargs)
        self.inventory_item_roles = self.InventoryItemRolesC(**kwargs)
        self.inventory_item_templates = self.InventoryItemTemplatesC(**kwargs)
        self.inventory_items = self.InventoryItemsC(**kwargs)
        self.locations = self.LocationsC(**kwargs)
        self.manufacturers = self.ManufacturersC(**kwargs)
        self.module_bay_templates = self.ModuleBayTemplatesC(**kwargs)
        self.module_bays = self.ModuleBaysC(**kwargs)
        self.module_types = self.ModuleTypesC(**kwargs)
        self.modules = self.ModulesC(**kwargs)
        self.platforms = self.PlatformsC(**kwargs)
        self.power_feeds = self.PowerFeedsC(**kwargs)
        self.power_outlet_templates = self.PowerOutletTemplatesC(**kwargs)
        self.power_outlets = self.PowerOutletsC(**kwargs)
        self.power_panels = self.PowerPanelsC(**kwargs)
        self.power_port_templates = self.PowerPortTemplatesC(**kwargs)
        self.power_ports = self.PowerPortsC(**kwargs)
        self.rack_reservations = self.RackReservationsC(**kwargs)
        self.rack_roles = self.RackRolesC(**kwargs)
        self.racks = self.RacksC(**kwargs)
        self.rear_port_templates = self.RearPortTemplatesC(**kwargs)
        self.rear_ports = self.RearPortsC(**kwargs)
        self.regions = self.RegionsC(**kwargs)
        self.site_groups = self.SiteGroupsC(**kwargs)
        self.sites = self.SitesC(**kwargs)
        self.virtual_chassis = self.VirtualChassisC(**kwargs)
        self.virtual_device_contexts = self.VirtualDeviceContextsC(**kwargs)

    class CableTerminationsC(Connector):
        """CableTerminationsC."""

        path = "dcim/cable-terminations/"

    class CablesC(Connector):
        """CablesC."""

        path = "dcim/cables/"

    class ConnectedDeviceC(Connector):
        """ConnectedDeviceC."""

        path = "dcim/connected-device/"

    class ConsolePortTemplatesC(Connector):
        """ConsolePortTemplatesC."""

        path = "dcim/console-port-templates/"

    class ConsolePortsC(Connector):
        """ConsolePortsC."""

        path = "dcim/console-ports/"

    class ConsoleServerPortTemplatesC(Connector):
        """ConsoleServerPortTemplatesC."""

        path = "dcim/console-server-port-templates/"

    class ConsoleServerPortsC(Connector):
        """ConsoleServerPortsC."""

        path = "dcim/console-server-ports/"

    class DeviceBayTemplatesC(Connector):
        """DeviceBayTemplatesC."""

        path = "dcim/device-bay-templates/"

    class DeviceBaysC(Connector):
        """DeviceBaysC."""

        path = "dcim/device-bays/"

    class DeviceRolesC(Connector):
        """DeviceRolesC."""

        path = "dcim/device-roles/"

    class DeviceTypesC(Connector):
        """DeviceTypesC."""

        path = "dcim/device-types/"

    class DevicesC(Connector):
        """DevicesC."""

        path = "dcim/devices/"

    class FrontPortTemplatesC(Connector):
        """FrontPortTemplatesC."""

        path = "dcim/front-port-templates/"

    class FrontPortsC(Connector):
        """FrontPortsC."""

        path = "dcim/front-ports/"

    class InterfaceTemplatesC(Connector):
        """InterfaceTemplatesC."""

        path = "dcim/interface-templates/"

    class InterfacesC(Connector):
        """InterfacesC."""

        path = "dcim/interfaces/"

    class InventoryItemRolesC(Connector):
        """InventoryItemRolesC."""

        path = "dcim/inventory-item-roles/"

    class InventoryItemTemplatesC(Connector):
        """InventoryItemTemplatesC."""

        path = "dcim/inventory-item-templates/"

    class InventoryItemsC(Connector):
        """InventoryItemsC."""

        path = "dcim/inventory-items/"

    class LocationsC(Connector):
        """LocationsC."""

        path = "dcim/locations/"

    class ManufacturersC(Connector):
        """ManufacturersC."""

        path = "dcim/manufacturers/"

    class ModuleBayTemplatesC(Connector):
        """ModuleBayTemplatesC."""

        path = "dcim/module-bay-templates/"

    class ModuleBaysC(Connector):
        """ModuleBaysC."""

        path = "dcim/module-bays/"

    class ModuleTypesC(Connector):
        """ModuleTypesC."""

        path = "dcim/module-types/"

    class ModulesC(Connector):
        """ModulesC."""

        path = "dcim/modules/"

    class PlatformsC(Connector):
        """PlatformsC."""

        path = "dcim/platforms/"

    class PowerFeedsC(Connector):
        """PowerFeedsC."""

        path = "dcim/power-feeds/"

    class PowerOutletTemplatesC(Connector):
        """PowerOutletTemplatesC."""

        path = "dcim/power-outlet-templates/"

    class PowerOutletsC(Connector):
        """PowerOutletsC."""

        path = "dcim/power-outlets/"

    class PowerPanelsC(Connector):
        """PowerPanelsC."""

        path = "dcim/power-panels/"

    class PowerPortTemplatesC(Connector):
        """PowerPortTemplatesC."""

        path = "dcim/power-port-templates/"

    class PowerPortsC(Connector):
        """PowerPortsC."""

        path = "dcim/power-ports/"

    class RackReservationsC(Connector):
        """RackReservationsC."""

        path = "dcim/rack-reservations/"

    class RackRolesC(Connector):
        """RackRolesC."""

        path = "dcim/rack-roles/"

    class RacksC(Connector):
        """RacksC."""

        path = "dcim/racks/"

    class RearPortTemplatesC(Connector):
        """RearPortTemplatesC."""

        path = "dcim/rear-port-templates/"

    class RearPortsC(Connector):
        """RearPortsC."""

        path = "dcim/rear-ports/"

    class RegionsC(Connector):
        """RegionsC."""

        path = "dcim/regions/"

    class SiteGroupsC(Connector):
        """SiteGroupsC."""

        path = "dcim/site-groups/"

    class SitesC(Connector):
        """SitesC."""

        path = "dcim/sites/"

    class VirtualChassisC(Connector):
        """VirtualChassisC."""

        path = "dcim/virtual-chassis/"

    class VirtualDeviceContextsC(Connector):
        """VirtualDeviceContextsC."""

        path = "dcim/virtual-device-contexts/"
