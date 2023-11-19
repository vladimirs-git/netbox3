# pylint: disable=R0902,R0903

"""Users connectors."""

from netbox3.api.connector import Connector
from netbox3.types_ import DAny


class UsersAC:
    """Users connectors."""

    def __init__(self, **kwargs):
        """Init UsersAC."""
        self.config = self.ConfigC(**kwargs)
        self.groups = self.GroupsC(**kwargs)
        self.permissions = self.PermissionsC(**kwargs)
        self.tokens = self.TokensC(**kwargs)
        self.users = self.UsersC(**kwargs)

    class ConfigC(Connector):
        """ConfigC."""

        path = "users/config/"

        def get(self, **kwargs) -> DAny:  # type: ignore
            """Get data."""
            _ = kwargs  # noqa
            return self._get_d()

    class GroupsC(Connector):
        """GroupsC."""

        path = "users/groups/"

    class PermissionsC(Connector):
        """PermissionsC."""

        path = "users/permissions/"

    class TokensC(Connector):
        """TokensC."""

        path = "users/tokens/"

    class UsersC(Connector):
        """UsersC."""

        path = "users/users/"
