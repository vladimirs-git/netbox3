# pylint: disable=R0902,R0903

"""Base for application connectors."""

from __future__ import annotations

from netbox3 import helpers as h


class BaseAC:
    """Base for application connectors."""

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        attrs = h.attr_names(self)
        attr = attrs[0]
        host = getattr(self, attr).host
        return f"<{name}: {host}>"
