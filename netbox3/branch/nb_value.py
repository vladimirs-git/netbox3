# pylint: disable=R0904

"""NbValue."""
import re

from netbox3.branch.nb_branch import NbBranch
from netbox3.exceptions import NbBranchError

RE_PREFIX = r"\d+\.\d+\.\d+\.\d+/\d+"


class NbValue(NbBranch):
    """Extracts a value from a Netbox object using a chain of keys."""

    def address(self) -> str:
        """ipam/ip-addresses/address.

        :return: IP address with prefix length A.B.C.D/LEN.

        :raise NbBranchError: if strict=True and the address does not match the naming
            convention A.B.C.D/LEN.
        """
        address = self.str("address")
        if self.strict:
            if not self._is_prefix(subnet=address):
                raise NbBranchError(f"address A.B.C.D/LEN expected in {self.data}.")
        return address

    def assigned_device(self) -> str:
        """ipam/ip-addresses/assigned_object/device/name.

        :return: Assigned device name.

        :raise NbBranchError: if strict=True and device has no assigned_object/device/name.
        """
        device = self.str("assigned_object", "device", "name")
        if self.strict and not device:
            raise NbBranchError(f"assigned_object/device/name expected in {self.data}.")
        return device

    def device_type_model(self) -> str:
        """dcim/devices/device_type/model.

        :return: Device type mode.

        :raise NbBranchError: if strict=True and device has no device_type.
        """
        model = self.str("device_type", "model")
        if self.strict and not model:
            raise NbBranchError(f"device_type/model expected in {self.data}.")
        return model

    def device_role_name(self) -> str:
        """dcim/devices/device_role/name.

        :return: Device role mode.

        :raise NbBranchError: if strict=True and device has no device_role.
        """
        device_role = self.str("device_role", "name")
        if self.strict and not device_role:
            raise NbBranchError(f"device_role/name expected in {self.data}.")
        return device_role

    def group_name(self) -> str:
        """imap/vlans/group/name.

        :return: Vlans group name.

        :raise NbBranchError: if strict=True and Vlan has no group.
        """
        group_name = self.str("group", "name")
        if self.strict and not group_name:
            raise NbBranchError(f"group/name expected in {self.data}.")
        return group_name

    def id_(self) -> int:
        """ipam/prefixes/id."""
        return self.int("id")

    def model(self) -> str:
        """dcim/devices/device-types/model.

        :return: Device-types model.

        :raise NbBranchError: if strict=True and device-types has no model.
        """
        model = self.str("model")
        if self.strict and not model:
            raise NbBranchError(f"model expected in {self.data}.")
        return model

    def name(self) -> str:
        """dcim/devices/name, dcim/vlans/name.

        :return: Name value.

        :raise NbBranchError: if strict=True and device has no name.
        """
        name = self.str("name")
        if self.strict and not name:
            raise NbBranchError(f"name expected in {self.data}.")
        return name

    def overlapped(self) -> str:
        """ipam/prefixes/overlapped."""
        return self.str("overlapped")

    def platform_slug(self) -> str:
        """dcim/devices/platform/slug.

        :return: Platform slug.

        :raise NbBranchError: if strict=True and device has no platform.
        """
        platform = self.str("platform", "slug")
        if self.strict and not platform:
            raise NbBranchError(f"platform/slug expected in {self.data}.")
        return platform

    def prefix(self) -> str:
        """ipam/prefixes/prefix, ipam/aggregates/prefix.

        :return: Prefix with length A.B.C.D/LEN.

        :raise NbBranchError: if strict=True and the prefix does not match the naming
            convention A.B.C.D/LEN.
        """
        prefix = self.str("prefix")
        if self.strict:
            if not self._is_prefix(subnet=prefix):
                raise NbBranchError(f"prefix expected in {self.data}.")
        return prefix

    def primary_ip4(self) -> str:
        """dcim/devices/primary_ip4/address.

        :return: primary_ip4 address.

        :raise NbBranchError: if strict=True and device has no primary_ip4 address.
        """
        try:
            primary_ip4 = self.data["primary_ip4"]["address"]
        except (KeyError, TypeError):
            primary_ip4 = ""
        if not isinstance(primary_ip4, str):
            primary_ip4 = ""

        if self.strict:
            if not primary_ip4:
                raise NbBranchError(f"primary_ip4/address expected in {self.data}.")
            if not re.match(r"^\d+\.\d+\.\d+\.\d+(/\d+)?$", primary_ip4):
                raise NbBranchError(f"primary_ip4/address A.B.C.D expected in {self.data}.")
        return primary_ip4

    def role_slug(self) -> str:
        """ipam/prefixes/role/slug.

        :return: Role slug.

        :raise NbBranchError: if strict=True and object has no role.
        """
        return self.str("role", "slug")

    def site_name(self, upper: bool = True) -> str:
        """ipam/prefixes/site/name, dcim/devices/sites/name.

        Convert site name to the same manner.
        Different objects have different upper or lower case:
        sites/name="SITE1",
        devices/site/name="SITE1",
        vlans/site/name="site1".

        :param upper: Whether to return the name in uppercase. Default is True.

        :return: Site name.

        :raise NbBranchError: if strict=True and object has no site name.
        """
        site = self.str("site", "name")
        if self.strict and not site:
            raise NbBranchError(f"site/name expected in {self.data}.")
        if upper:
            return site.upper()
        return site.lower()

    def status(self) -> str:
        """ipam/prefixes/status/value.

        :return: Status value.

        :raise NbBranchError: if strict=True and object has no status.
        """
        return self.str("status", "value")

    def tenant(self) -> str:
        """ipam/prefixes/tenant/name.

        :return: Tenant name.

        :raise NbBranchError: if strict=True and object has no tenant.
        """
        return self.str("tenant", "name")

    def vid(self) -> int:
        """ipam/vlans/vid.

        :return: Vlan id or 0 if no Vlan id

        :raise NbBranchError: if strict=True and object has no vlans key.
        """
        return self.int("vid")

    def vlan(self) -> int:
        """ipam/prefixes/vlan/vid.

        :return: Vlan id or 0 if no Vlan

        :raise NbBranchError: if strict=True and object has no vlan key.
        """
        return self.int("vlan", "vid")

    def url(self) -> str:
        """ipam/prefixes/url.

        :return: API URL to object.

        :raise NbBranchError: if strict=True and object has no URL.
        """
        url = self.str("url")
        if self.strict:
            if not url:
                raise NbBranchError(f"url expected in {self.data}.")
        return url

    # ================================ is ================================

    def is_dcim(self, dcim: str) -> bool:
        """Check if object is dcim/devices.

        :return: True - if object is dcim/devices, False - otherwise.
        :rtype: bool

        :raise NbBranchError: - if url is not /api/dcim/ and self.strict=True
        """
        try:
            url = self.data["url"]
            if re.search(f"/api/dcim/{dcim}/", url):
                return True
            return False
        except (KeyError, TypeError) as ex:
            if self.strict:
                raise NbBranchError(f"invalid url in {self.data}.") from ex
            return False

    def is_ipam(self, ipam: str) -> bool:
        """Check If ipam url ipam is aggregate, prefix or address.

        :return: True - if aggregate, prefix, address, False - otherwise.
        :rtype: bool

        :raise NbBranchError: If url is not aggregate or prefix or address
            and self.strict=True
        """
        try:
            url = self.data["url"]
            if re.search(f"/api/ipam/{ipam}/", url):
                return True
            return False
        except (KeyError, TypeError) as ex:
            if self.strict:
                raise NbBranchError(f"ipam url expected in {self.data}.") from ex
            return False

    def is_vrf(self) -> bool:
        """Return True if data has vrf."""
        if self.data.get("vrf"):
            return True
        return False

    # ============================= helpers ==============================

    @staticmethod
    def _is_prefix(subnet: str) -> bool:
        """Return True if subnet has A.B.C.D/LEN format."""
        if re.match(rf"^{RE_PREFIX}$", subnet):
            return True
        return False
