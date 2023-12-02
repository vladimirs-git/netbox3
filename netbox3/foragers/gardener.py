"""Gardener."""
from operator import itemgetter

from netports import Intf
from vhelpers import vlist

from netbox3.api.base_c import BaseC
from netbox3.foragers.ipv4 import IPv4
from netbox3.nb_tree import NbTree
from netbox3.types_ import LDAny, DAny, LStr, DiDAny, LInt, DiLDAny


class Gardener:
    """Helper methods are used to create additional keys in Netbox objects,

    representing them similarly to the WEB UI.
    """

    def __init__(self, tree: NbTree):
        """Init Gardener.
        :param NbTree tree: Contains Netbox that need to be updated similar to the WEB UI.
        """
        self.tree = tree

    def grow_dcim_devices(self) -> None:
        """Create additional keys to represent dcim.devices similar to the WEB UI.

        Add console_ports, console_server_ports, device_bays, front_ports, interfaces,
        inventory_items, module_bays, power_outlets, power_ports, rear_ports
        in dcim.devices.

        :return: None. Update NbTree object.
        """
        self._grow_devices(app="dcim")

    def grow_virtualization_virtual_machines(self) -> None:
        """Create additional keys to represent virtualization.virtual_machines.

        Add interfaces in virtualization.virtual_machines.

        :return: None. Update NbTree object.
        """
        self._grow_devices(app="virtualization")

    # noinspection PyProtectedMember
    def _grow_devices(self, app: str) -> None:
        """Create additional keys to represent devices/VM similar to the WEB UI.

        :param app: Application name: "dcim", "virtualization"
        :return: None. Update NbTree object.
        """
        model = "devices"
        key = "dcim/devices/"
        if app == "virtualization":
            model = "virtual_machines"
            key = "virtualization/virtual-machines/"
        models: LStr = BaseC._reserved_keys[key]  # pylint: disable=W0212

        # init extra keys
        devices_d: DiDAny = getattr(getattr(self.tree, app), model)
        for device in devices_d.values():
            for model in models:
                device[model] = {}

        # set extra values
        key = "device"
        if app == "virtualization":
            key = "virtual_machine"

        for model in models:
            ports_d: DiDAny = getattr(getattr(self.tree, app), model)
            ports: LDAny = list(ports_d.values())

            # sort by interface idx
            ports_lt = [(Intf(d["name"]), d) for d in ports]
            ports_lt.sort(key=itemgetter(0))
            ports = [dict(t[1]) for t in ports_lt]

            for port in ports:
                name = port["name"]
                id_ = port[key]["id"]
                device_: DAny = devices_d.get(id_, {})  # pylint: disable=E1101
                if model in device_:
                    device_[model][name] = port

    def grow_ipam_ipv4(self) -> None:
        """Create additional keys to represent ipam similar to the WEB UI.

            Add ipv4, aggregate, super_prefix, sub_prefixes, ip_addresses
            in ipam.aggregate, ipam.prefixes, ipam.ip_addresses.

        :return: None. Update NbTree object.
        """
        self._init_ipam_keys()
        self._grow_ipam_aggregates()
        self._grow_ipam_prefixes()
        self._grow_ipam_ip_addresses()
        self._grow_update_sub_prefixes()

    def _init_ipam_keys(self) -> None:
        """Init extra keys that are required for aggregates, prefixes, ip_addresses."""
        for model, key, strict in [
            ("aggregates", "prefix", True),
            ("prefixes", "prefix", True),
            ("ip_addresses", "address", False),
        ]:
            objects: DiDAny = getattr(self.tree.ipam, model)
            for data in objects.values():
                snet = data[key]
                data["ipv4"] = IPv4(snet, strict=strict)
                data["aggregate"] = {}
                data["super_prefix"] = {}
                data["sub_prefixes"] = []
                data["ip_addresses"] = []

    def _grow_ipam_aggregates(self) -> None:
        """Add prefixes to tree.ipam.aggregates.sub_prefixes."""
        aggregates: LDAny = self._get_aggregates_ip4()
        prefixes_d: DiLDAny = self._get_prefixes_ip4_d()
        for aggregate in aggregates:
            for depth, prefixes in prefixes_d.items():
                for prefix in prefixes:
                    _aggregate = aggregate["prefix"]
                    _prefix = prefix["prefix"]
                    if prefix["ipv4"] in aggregate["ipv4"]:
                        prefix["aggregate"] = aggregate
                        if depth == 0:
                            aggregate["sub_prefixes"].append(prefix)

    def _grow_ipam_ip_addresses(self) -> None:
        """Add prefixes to tree.ipam.ip-addresses.super_prefix."""
        ip_addresses: LDAny = self._get_ip_addresses_ip4()
        prefixes_d: DiLDAny = self._get_prefixes_ip4_d()
        depths: LInt = list(prefixes_d)
        depths.reverse()

        added_addresses: LDAny = []
        for depth in depths:
            ip_addresses_ = ip_addresses.copy()
            prefixes: LDAny = prefixes_d.get(depth, [])
            for ip_address in ip_addresses_:
                for prefix in prefixes:
                    if ip_address["ipv4"] not in prefix["ipv4"]:
                        continue
                    if ip_address in added_addresses:
                        continue
                    ip_address["aggregate"] = prefix["aggregate"]
                    ip_address["super_prefix"] = prefix
                    prefix["ip_addresses"].append(ip_address)
                    added_addresses.append(ip_address)
            ip_addresses = [d for d in ip_addresses if d not in added_addresses]

    def _grow_ipam_prefixes(self) -> None:
        """Add prefixes to tree.ipam.prefixes.sub_prefixes, super_prefix"""
        super_prefixes = []
        prefixes_d: DiLDAny = self._get_prefixes_ip4_d()
        for depth, sub_prefixes in enumerate(prefixes_d.values()):
            if not depth:
                super_prefixes = sub_prefixes
                continue
            for super_prefix in super_prefixes:
                if super_prefix["ipv4"].prefixlen == 32:
                    continue
                for sub_prefix in sub_prefixes:
                    if sub_prefix["ipv4"] in (super_prefix["ipv4"]):
                        super_prefix["sub_prefixes"].append(sub_prefix)
                        sub_prefix["super_prefix"] = super_prefix
            super_prefixes = sub_prefixes

    def _grow_update_sub_prefixes(self) -> None:
        """Update sub_prefixes in ipam.aggregates and ipam.prefixes.

        Remove duplicates, remove objects with improper depth, sort by IPv4.
        """
        aggregates = self._get_aggregates_ip4()
        for aggregate in aggregates:
            sub_prefixes = vlist.no_dupl(aggregate["sub_prefixes"])
            sub_prefixes = [d for d in sub_prefixes if not d["super_prefix"]]
            aggregate["sub_prefixes"] = sorted(sub_prefixes, key=itemgetter("ipv4"))

        prefixes = self._get_prefixes_ip4()
        for prefix in prefixes:
            sub_prefixes = vlist.no_dupl(prefix["sub_prefixes"])
            prefix["sub_prefixes"] = sorted(sub_prefixes, key=itemgetter("ipv4"))
            ip_addresses = vlist.no_dupl(prefix["ip_addresses"])
            prefix["ip_addresses"] = sorted(ip_addresses, key=itemgetter("ipv4"))

    # ============================= helpers ==============================

    def _get_aggregates_ip4(self) -> LDAny:
        """Return ipam.aggregates family=4 sorted by IPv4."""
        aggregates: LDAny = list(self.tree.ipam.aggregates.values())
        aggregates = [d for d in aggregates if d["family"]["value"] == 4]
        return sorted(aggregates, key=itemgetter("ipv4"))

    def _get_ip_addresses_ip4(self) -> LDAny:
        """Return ipam.ip_addresses family=4 sorted by IPv4."""
        ip_addresses: LDAny = list(self.tree.ipam.ip_addresses.values())
        ip_addresses = [d for d in ip_addresses if d["family"]["value"] == 4 and d["vrf"] is None]
        return sorted(ip_addresses, key=itemgetter("ipv4"))

    def _get_prefixes_ip4(self) -> LDAny:
        """Return ipam.prefixes family=4 sorted by IPv4."""
        prefixes: LDAny = list(self.tree.ipam.prefixes.values())
        prefixes = [d for d in prefixes if d["family"]["value"] == 4 and d["vrf"] is None]
        return sorted(prefixes, key=itemgetter("ipv4"))

    def _get_prefixes_ip4_d(self) -> DiLDAny:
        """Split prefixes by depth.

        :return: A dictionary of prefixes where the key represents the depth
            and the value represents a list of prefixes at that depth.
        """
        prefixes: LDAny = self._get_prefixes_ip4()
        prefixes_d: DiLDAny = {d["_depth"]: [] for d in prefixes}
        for prefix in prefixes:
            depth = int(prefix["_depth"])
            prefixes_d[depth].append(prefix)
        return prefixes_d
