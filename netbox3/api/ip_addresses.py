# pylint: disable=R0801

"""IP Addresses connectors."""

from netbox3.api.connector import Connector
from netbox3.types_ import LDAny


class IpAddressesC(Connector):
    """IpAddressesC."""

    path = "ipam/ip-addresses/"

    # noinspection PyIncorrectDocstring
    def get(self, **kwargs) -> LDAny:  # pylint: disable=W0246
        """Request data from Netbox using `Filtering parameters`_.

        Only ``NbApi.ipam.ip_addresses.get()`` is described in this documentation.
        Other models are implemented in a similar manner.

        NbApi parameters:

        :param max_limit: Maximum count of objects that need to be requested.
            This is useful in development to prevent script blocking when
            receiving only part of the requested data is acceptable.
            Default is `0` no limit.
        :type max_limit: int

        :param or_{parameter}: List of parameters that need to be requested
            in an ``OR`` manner, where ``{parameter}`` is the name of the
            Netbox REST API `Filtering parameters`_.
        :type or_{parameter}: list

        WEB UI Filter parameters:

        :param q: IP address substring.
        :type q: str or List[str]

        :param tag: Tag (slug).
        :type tag: str or List[str]

        Attributes:

        :param parent: Parent Prefix. Addresses of this prefix.
        :type parent: str or List[str]

        :param family: Address family. IP version.
        :type family: int or List[int]

        :param status: Status.
        :type parent: str or List[str]

        :param role: Role.
        :type role: str or List[str]

        :param mask_length: Mask length.
        :type mask_length: int or List[int]

        :param assigned_to_interface: Assigned to an interface.
        :type assigned_to_interface: bool

        :param dns_name: DNS name.
        :type dns_name: str or List[str]

        VRF:

        :param vrf: Assigned VRF name.
        :type vrf: str or List[str]
        :param vrf_id: Assigned VRF object ID.
        :type vrf_id: int or List[int]

        :param present_in_vrf: Present in VRF name.
        :type present_in_vrf: str or List[str]
        :param present_in_vrf_id: Present in VRF object ID.
        :type present_in_vrf_id: int or List[int]

        Tenant:

        :param tenant_group: Tenant group name.
        :type tenant_group: str or List[str]
        :param tenant_group_id: Tenant group object ID.
        :type tenant_group_id: int or List[int]

        :param tenant: Tenant name.
        :type tenant: str or List[str]
        :param tenant_id: Tenant object ID.
        :type tenant_id: int or List[int]

        Device/VM:

        :param device: Assigned Device name.
        :type device: str or List[str]
        :param device_id: Assigned Device object ID.
        :type device_id: int or List[int]

        :param virtual_machine: Assigned Virtual Machine name.
        :type virtual_machine: str or List[str]
        :param virtual_machine_id: Assigned Virtual Machine object ID.
        :type virtual_machine_id: int or List[int]

        Data Filter parameters:

        :param id: Object ID.
        :type id: int or List[int]

        :param address: IP address.
        :type address: str or List[str]

        Text pattern:

        :param description: Description exact value.
        :type description: str or List[str]
        :param description_empty: Is empty.
        :type description_empty: bool
        :param description__ic: Case-insensitive contains.
        :type description__ic: str or List[str]
        :param description__ie: Case-insensitive exact.
        :type description__ie: str or List[str]
        :param description__iew: Case-insensitive ends with.
        :type description__iew: str or List[str]
        :param description__isw: Case-insensitive starts with.
        :type description__isw: str or List[str]
        :param description__n: Not case-sensitive.
        :type description__n: str or List[str]
        :param description__nic: Not case-insensitive contains.
        :type description__nic: str or List[str]
        :param description__nie: Not case-insensitive exact.
        :type description__nie: str or List[str]
        :param description__niew: Not case-insensitive ends with.
        :type description__niew: str or List[str]
        :param description__nisw: Not case-insensitive starts with.
        :type description__nisw: str or List[str]

        Date pattern:

        :param created: Object created date.
        :type created: str or List[str]
        :param created__empty: Is empty.
        :type created__empty: bool
        :param created__gt: Greater than.
        :type created__gt: str or List[str]
        :param created__gte: Greater than or equal.
        :type created__gte: str or List[str]
        :param created__lt: Less than.
        :type created__lt: str or List[str]
        :param created__lte: Less than or equal.
        :type created__lte: str or List[str]
        :param created__n: Not.
        :type created__n: str or List[str]
        """
        return super().get(**kwargs)
