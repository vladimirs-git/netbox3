# pylint: disable=R0904

"""NbCustom."""
import re

from vhelpers import vlist, vre

from netbox3.branch.nb_value import NbValue, RE_PREFIX
from netbox3.types_ import SStr, T2Str


class NbCustom(NbValue):
    """Extracts a value from a Netbox object using a chain of keys."""

    # ========================== custom_fields ===========================

    def cf_cloud_account(self) -> str:
        """ipam/aggregates/custom_fields/cloud_account/label."""
        return self.str("custom_fields", "cloud_account")

    def cf_end_of_support(self) -> str:
        """dcim/devices/custom_fields/end_of_support/value."""
        cf_value = self.str("custom_fields", "end_of_support").strip()
        return cf_value

    def cf_env(self) -> str:
        """ipam/prefixes/custom_fields/env/label."""
        return self.str("custom_fields", "env")

    def cf_super_aggr(self) -> T2Str:
        """ipam/aggregates/custom_fields/super_aggregate/value."""
        value = self.str("custom_fields", "super_aggregate")
        value = value.strip()
        prefix, descr = vre.find2(f"^({RE_PREFIX})(.*)", value)
        return prefix, descr.strip()

    def cf_sw_planned(self) -> str:
        """dcim/devices/device-types/custom_fields/sw_planned."""
        return self.str("custom_fields", "sw_planned")

    def cf_sw_version(self) -> str:
        """dcim/devices/custom_fields/sw_version."""
        return self.str("custom_fields", "sw_version")

    # ========================== custom values ===========================

    def firewalls__in_aggregate(self) -> SStr:
        """aggregates/custom_fields/ or description."""
        if hostnames := self._hosts_in_cf_firewalls():
            return hostnames
        if hostnames := self._hosts_in_aggr_descr():
            return hostnames
        return set()

    def _hosts_in_cf_firewalls(self) -> SStr:
        """Hostnames in aggregates/custom_fields/firewalls."""
        try:
            value = self.data["custom_fields"]["firewalls"]
        except (KeyError, TypeError):
            return set()
        if not value or not isinstance(value, str):
            return set()
        hostnames_ = "\n".join(vlist.split(value, ignore="_-"))
        hostnames = re.findall(r"^(\w+-\w+-\w+-\w+)", hostnames_, re.M)
        return set(hostnames)

    def _hosts_in_aggr_descr(self) -> SStr:
        """Hostnames in aggregates/description."""
        tags = self.tags()
        if "noc_aggregates_belonging" not in tags:
            return set()

        try:
            description = self.data["description"]
        except (KeyError, TypeError):
            if self.strict:
                raise
            return set()

        if not isinstance(description, str):
            if self.strict:
                raise TypeError(f"{description=}, {str} expected.")
            return set()

        descr_ = "\n".join(vlist.split(description, ignore="_-"))
        hostnames = set(re.findall(r"^(\w+-\w+-\w+-\w+)", descr_, re.M))
        return hostnames
