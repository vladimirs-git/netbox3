# pylint: disable=R0902,R0903

"""Users Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class UsersAF(BaseAF):
    """Users Forager."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init UsersAF.

        :param api: NbApi object, connector to Netbox API.
        :param root: NbTree object where raw data from Netbox needs to be saved.
        :param tree: NbTree object where transformed data from Netbox needs to be saved.
        """
        super().__init__(api, root, tree)
        # config: is not DiDAny
        self.groups = self.GroupsF(self)
        self.permissions = self.PermissionsF(self)
        self.tokens = self.TokensF(self)
        self.users = self.UsersF(self)

    class ConfigF(Forager):
        """ConfigF."""

    class GroupsF(Forager):
        """GroupsF."""

    class PermissionsF(Forager):
        """PermissionsF."""

    class TokensF(Forager):
        """TokensF."""

    class UsersF(Forager):
        """UsersF."""
