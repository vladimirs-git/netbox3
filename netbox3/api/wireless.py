# pylint: disable=R0902,R0903

"""Wireless connectors."""

from netbox3.api.connector import Connector


class WirelessAC:
    """Wireless connectors."""

    def __init__(self, **kwargs):
        """Init WirelessAC."""
        self.wireless_lan_groups = self.WirelessLanGroupsC(**kwargs)
        self.wireless_lans = self.WirelessLansC(**kwargs)
        self.wireless_links = self.WirelessLinksC(**kwargs)

    class WirelessLanGroupsC(Connector):
        """WirelessLanGroupsC."""

        path = "wireless/wireless-lan-groups/"

    class WirelessLansC(Connector):
        """WirelessLansC."""

        path = "wireless/wireless-lans/"

    class WirelessLinksC(Connector):
        """WirelessLinksC."""

        path = "wireless/wireless-links/"
