# pylint: disable=R0902,R0903

"""Tenancy Forager."""
from netbox3.foragers.base_fa import BaseAF
from netbox3.foragers.forager import Forager
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree


class TenancyAF(BaseAF):
    """Tenancy Forager."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init TenancyAF.

        :param api: NbApi object, connector to Netbox API.
        :param root: NbTree object where raw data from Netbox needs to be saved.
        :param tree: NbTree object where transformed data from Netbox needs to be saved.
        """
        super().__init__(api, root, tree)
        self.contact_assignments = self.ContactAssignmentsF(self)
        self.contact_groups = self.ContactGroupsF(self)
        self.contact_roles = self.ContactRolesF(self)
        self.contacts = self.ContactsF(self)
        self.tenant_groups = self.TenantGroupsF(self)
        self.tenants = self.TenantsF(self)

    class TenancyF(Forager):
        """TenancyF."""

    class ContactAssignmentsF(Forager):
        """ContactAssignmentsF."""

    class ContactGroupsF(Forager):
        """ContactGroupsF."""

    class ContactRolesF(Forager):
        """ContactRolesF."""

    class ContactsF(Forager):
        """ContactsF."""

    class TenantGroupsF(Forager):
        """TenantGroupsF."""

    class TenantsF(Forager):
        """TenantsF."""
