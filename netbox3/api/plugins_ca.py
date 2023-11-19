# pylint: disable=R0902,R0903

"""Plugins connectors."""

from netbox3.api.connector import Connector
from netbox3.types_ import LDAny


class PluginsAC:
    """Plugins connectors."""

    def __init__(self, **kwargs):
        """Init PluginsAC."""
        self.installed_plugins = self.InstalledPluginsC(**kwargs)

    class InstalledPluginsC(Connector):
        """InstalledPluginsC."""

        path = "plugins/installed-plugins/"

        def get(self, **kwargs) -> LDAny:
            """Get data."""
            _ = kwargs  # noqa
            return self._get_l()
