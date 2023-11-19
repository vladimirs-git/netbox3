# pylint: disable=R0902,R0903

"""Wireless Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class WirelessAF(BaseAF):
    """Wireless Forager."""

    def __init__(self, root: NbTree, api: NbApi):
        """Init WirelessAF.

        :param root: NbTree object where data from Netbox needs to be saved.
        :param api: NbApi object, connector to Netbox API.
        """
        super().__init__(root, api)
        self.wireless_lan_groups = self.WirelessLanGroupsF(self)
        self.wireless_lans = self.WirelessLansF(self)
        self.wireless_links = self.WirelessLinksF(self)

    class WirelessLanGroupsF(Forager):
        """WirelessLanGroupsF."""

    class WirelessLansF(Forager):
        """WirelessLansF."""

    class WirelessLinksF(Forager):
        """WirelessLinksF."""
