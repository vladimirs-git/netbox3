"""Tree of Netbox model objects."""
import logging
from copy import deepcopy
from typing import Optional

from pydantic import BaseModel, Field

from netbox3 import helpers as h
from netbox3.types_ import DiDAny, LStr, DAny


class BaseTree(BaseModel):
    """Base for BbTree models."""

    def count(self) -> int:
        """Count the number of Netbox objects for all models."""
        return sum(len(getattr(self, s)) for s in self.models())

    def models(self) -> LStr:
        """Get all application model names.

        :return: Model names.

        :example:
            NbTree().circuits.models() -> ["circuit_terminations", "circuit_types", ...]
        """
        return list(self.__annotations__)


# noinspection DuplicatedCode
class CircuitsM(BaseTree):
    """Base for Circuits application."""

    circuit_terminations: DiDAny = Field(default={})
    circuit_types: DiDAny = Field(default={})
    circuits: DiDAny = Field(default={})
    provider_accounts: DiDAny = Field(default={})
    provider_networks: DiDAny = Field(default={})
    providers: DiDAny = Field(default={})


class CoreM(BaseTree):
    """Base for Core application."""

    data_files: DiDAny = Field(default={})
    data_sources: DiDAny = Field(default={})
    jobs: DiDAny = Field(default={})


class DcimM(BaseTree):
    """Base for DCIM application."""

    cable_terminations: DiDAny = Field(default={})
    cables: DiDAny = Field(default={})
    # connected_device, is not model
    console_port_templates: DiDAny = Field(default={})
    console_ports: DiDAny = Field(default={})
    console_server_port_templates: DiDAny = Field(default={})
    console_server_ports: DiDAny = Field(default={})
    device_bay_templates: DiDAny = Field(default={})
    device_bays: DiDAny = Field(default={})
    device_roles: DiDAny = Field(default={})
    device_types: DiDAny = Field(default={})
    devices: DiDAny = Field(default={})
    front_port_templates: DiDAny = Field(default={})
    front_ports: DiDAny = Field(default={})
    interface_templates: DiDAny = Field(default={})
    interfaces: DiDAny = Field(default={})
    inventory_item_roles: DiDAny = Field(default={})
    inventory_item_templates: DiDAny = Field(default={})
    inventory_items: DiDAny = Field(default={})
    locations: DiDAny = Field(default={})
    manufacturers: DiDAny = Field(default={})
    module_bay_templates: DiDAny = Field(default={})
    module_bays: DiDAny = Field(default={})
    module_types: DiDAny = Field(default={})
    modules: DiDAny = Field(default={})
    platforms: DiDAny = Field(default={})
    power_feeds: DiDAny = Field(default={})
    power_outlet_templates: DiDAny = Field(default={})
    power_outlets: DiDAny = Field(default={})
    power_panels: DiDAny = Field(default={})
    power_port_templates: DiDAny = Field(default={})
    power_ports: DiDAny = Field(default={})
    rack_reservations: DiDAny = Field(default={})
    rack_roles: DiDAny = Field(default={})
    racks: DiDAny = Field(default={})
    rear_port_templates: DiDAny = Field(default={})
    rear_ports: DiDAny = Field(default={})
    regions: DiDAny = Field(default={})
    site_groups: DiDAny = Field(default={})
    sites: DiDAny = Field(default={})
    virtual_chassis: DiDAny = Field(default={})
    virtual_device_contexts: DiDAny = Field(default={})


class ExtrasM(BaseTree):
    """Base for extras application."""

    bookmarks: DiDAny = Field(default={})
    config_contexts: DiDAny = Field(default={})
    config_templates: DiDAny = Field(default={})
    content_types: DiDAny = Field(default={})
    custom_field_choice_sets: DiDAny = Field(default={})
    custom_fields: DiDAny = Field(default={})
    custom_links: DiDAny = Field(default={})
    export_templates: DiDAny = Field(default={})
    image_attachments: DiDAny = Field(default={})
    journal_entries: DiDAny = Field(default={})
    object_changes: DiDAny = Field(default={})
    reports: DiDAny = Field(default={})
    saved_filters: DiDAny = Field(default={})
    scripts: DiDAny = Field(default={})
    tags: DiDAny = Field(default={})
    webhooks: DiDAny = Field(default={})


class IpamM(BaseTree):
    """Base for IPAM application."""

    aggregates: DiDAny = Field(default={})
    asn_ranges: DiDAny = Field(default={})
    asns: DiDAny = Field(default={})
    fhrp_group_assignments: DiDAny = Field(default={})
    fhrp_groups: DiDAny = Field(default={})
    ip_addresses: DiDAny = Field(default={})
    ip_ranges: DiDAny = Field(default={})
    l2vpn_terminations: DiDAny = Field(default={})
    l2vpns: DiDAny = Field(default={})
    prefixes: DiDAny = Field(default={})
    rirs: DiDAny = Field(default={})
    roles: DiDAny = Field(default={})
    route_targets: DiDAny = Field(default={})
    service_templates: DiDAny = Field(default={})
    services: DiDAny = Field(default={})
    vlan_groups: DiDAny = Field(default={})
    vlans: DiDAny = Field(default={})
    vrfs: DiDAny = Field(default={})


# noinspection DuplicatedCode
class TenancyM(BaseTree):
    """Base for Tenancy application."""

    contact_assignments: DiDAny = Field(default={})
    contact_groups: DiDAny = Field(default={})
    contact_roles: DiDAny = Field(default={})
    contacts: DiDAny = Field(default={})
    tenant_groups: DiDAny = Field(default={})
    tenants: DiDAny = Field(default={})


class UsersM(BaseTree):
    """Base for Users application."""

    # config: is not DiDAny
    groups: DiDAny = Field(default={})
    permissions: DiDAny = Field(default={})
    tokens: DiDAny = Field(default={})
    users: DiDAny = Field(default={})


class VirtualizationM(BaseTree):
    """Base for Virtualization application."""

    cluster_groups: DiDAny = Field(default={})
    cluster_types: DiDAny = Field(default={})
    clusters: DiDAny = Field(default={})
    interfaces: DiDAny = Field(default={})
    virtual_machines: DiDAny = Field(default={})


class WirelessM(BaseTree):
    """Base for Wireless application."""

    wireless_lan_groups: DiDAny = Field(default={})
    wireless_lans: DiDAny = Field(default={})
    wireless_links: DiDAny = Field(default={})


class NbTree(BaseModel):
    """Base for Netbox models tree."""

    circuits: CircuitsM = Field(default=CircuitsM())
    core: CoreM = Field(default=CoreM())
    dcim: DcimM = Field(default=DcimM())
    extras: ExtrasM = Field(default=ExtrasM())
    ipam: IpamM = Field(default=IpamM())
    tenancy: TenancyM = Field(default=TenancyM())
    users: UsersM = Field(default=UsersM())
    virtualization: VirtualizationM = Field(default=VirtualizationM())
    wireless: WirelessM = Field(default=WirelessM())

    def apps(self) -> LStr:
        """Get all application names.

        :return: Application names.

        :example:
            NbTree().apps() -> ["circuit_terminations", "circuit_types", ...]
        """
        return list(self.__annotations__)

    def count(self) -> int:
        """Count the number of Netbox objects for all models."""
        return sum(getattr(self, s).count() for s in self.apps())


ONbTree = Optional[NbTree]


def insert_tree(src: NbTree, dst: NbTree) -> None:
    """Insert the data from the source NbTree object into the destination NbTree object.

    :param src: The source tree from which data will be copied.
    :param dst: The destination tree where data will be inserted.

    :return: None. The data is updated in the destination tree.
    """
    for app in src.apps():
        for model in getattr(src, app).models():
            src_d: dict = getattr(getattr(src, app), model)
            dst_d: dict = getattr(getattr(dst, app), model)
            dst_d.update(src_d)


def grow_tree(tree: NbTree) -> NbTree:
    """Assemble Netbox objects in tree within itself.

    The Netbox objects are represented as a multidimensional dictionary.
    :param tree: NbTree object to join the data in.

    :return: NbTree object with the joined data.
    """
    tree = deepcopy(tree)
    for app in tree.apps():  # pylint: disable=R1702
        for model in getattr(tree, app).models():
            objects_d = getattr(getattr(tree, app), model)
            for _, parent in objects_d.items():
                for key, child in parent.items():
                    if isinstance(child, dict):
                        if child_full := _get_child(child=child, tree=tree):
                            parent[key].clear()
                            parent[key].update(child_full)
                    elif isinstance(child, list):
                        for child_ in child:
                            if not isinstance(child_, dict):
                                continue
                            if child_full := _get_child(child=child_, tree=tree):
                                child_.clear()
                                child_.update(child_full)
    return tree


def missed_urls(urls: LStr, tree: NbTree) -> LStr:
    """Return URLs to objects that are missed in the tree.

    :param urls: A list of URLs to filter.
    :param tree: NbTree object to check URLs inside.

    :return: A list of URLs that are missed in the tree.
    """
    urls_: LStr = []
    for url in urls:
        url = url.rstrip("/")
        app, model, digit = url.split("/")[-3:]
        model = h.model_to_attr(model)
        id_ = int(digit)

        try:
            data = getattr(getattr(tree, app), model).get(id_)
        except AttributeError as ex:
            msg = f"{type(ex).__name__}: {ex}"
            logging.error(msg)
            continue

        if not data:
            urls_.append(url)
    return urls_


# ============================= helpers ==============================


def _get_child(child: DAny, tree: NbTree) -> DAny:
    """Search child Netbox object in the model data to insert (replace) it in the parent.

    :param child: Netbox object that require dependency update.
    :param tree: NbTree object, contains model data (Netbox objects).

    :return: Child dictionary from the model that needs to be inserted into the parent dictionary.
    """
    if child.get("url"):
        url = str(child["url"]).strip("/")
        app, model, digit = h.split_url(url)
        model = h.model_to_attr(model)
        if model_d := getattr(getattr(tree, app), model):
            if child_full := model_d.get(int(digit)):
                return child_full

    if child.get("object_id") and child.get("object"):
        if isinstance(child["object"], dict):
            child_full = _get_child(child["object"], tree)
            child["object"].clear()
            child["object"].update(child_full)
            return {}

    return {}
