# pylint: disable=R0902,R0903

"""Tenancy connectors."""

from netbox3.api.connector import Connector


class TenancyAC:
    """Tenancy connectors."""

    def __init__(self, **kwargs):
        """Init TenancyAC."""
        self.contact_assignments = self.ContactAssignmentsC(**kwargs)
        self.contact_groups = self.ContactGroupsC(**kwargs)
        self.contact_roles = self.ContactRolesC(**kwargs)
        self.contacts = self.ContactsC(**kwargs)
        self.tenant_groups = self.TenantGroupsC(**kwargs)
        self.tenants = self.TenantsC(**kwargs)

    class ContactAssignmentsC(Connector):
        """ContactAssignmentsC."""

        path = "tenancy/contact-assignments/"

    class ContactGroupsC(Connector):
        """ContactGroupsC."""

        path = "tenancy/contact-groups/"

    class ContactRolesC(Connector):
        """ContactRolesC."""

        path = "tenancy/contact-roles/"

    class ContactsC(Connector):
        """ContactsC."""

        path = "tenancy/contacts/"

    class TenantGroupsC(Connector):
        """TenantGroupsC."""

        path = "tenancy/tenant-groups/"

    class TenantsC(Connector):
        """TenantsC."""

        path = "tenancy/tenants/"
