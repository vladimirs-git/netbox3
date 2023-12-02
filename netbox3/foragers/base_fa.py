"""Base for Application Foragers."""

from netbox3 import helpers as h
from netbox3.api import ConnectorA
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree
from netbox3.types_ import LStr


class BaseAF:
    """Base for Application Foragers."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init BaseAF.

        :param root: Dictionary where data from Netbox needs to be saved.
        """
        self.api = api
        self.root: NbTree = root
        self.tree: NbTree = tree
        self.app: str = h.attr_name(self)
        self.connector: ConnectorA = getattr(api, self.app)  # connector to application

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        count = self.count()
        return f"<{name}: {count}>"

    def count(self) -> int:
        """Count of the Netbox objects in the self root model.

        :return: Count of the Netbox objects.
        """
        return getattr(self.root, self.app).count()

    def get(self, nested: bool = False, **kwargs) -> None:
        """Get all objects from the Netbox, add objects to root.

        :param bool nested: True - Request base and nested objects,
            False - Request only base objects. Default is `False`.

        :param kwargs: Filtering parameters.

        :return: None. Update self object.
        """
        models: LStr = getattr(self.root, self.app).models()
        for model in models:
            getattr(self, model).get(nested=nested, **kwargs)
