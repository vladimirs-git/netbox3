"""Map parameter {name} to {name}_id."""
from typing import Dict

from pydantic import BaseModel, Field

from netbox3.types_ import DList


class ParamPath(BaseModel):
    """Map parameter {name} to {name}_id."""

    param: str = Field(description="Parameter name that need to map")
    path: str = Field(description="app/model path to request objects for mapping")
    key: str = Field(default="name", description="Key to request objects for mapping")

    @property
    def param_id(self) -> str:
        """Mapped parameter {name}_id."""
        return f"{self.param}_id"


DParamPath = Dict[str, ParamPath]
DDParamPath = Dict[str, DParamPath]


def data(path: str) -> DParamPath:
    """Create the ParamIdMap objects.

    This mapping is used to get objects from Netbox by {name} instead of {name}_id.
    :param path: app/model path.
    :return: Dictionary of ParamIdMap objects.
    """
    result: DParamPath = {
        # circuits
        "circuit": ParamPath(param="circuit", path="circuits/circuits/", key="cid"),
        "provider": ParamPath(param="provider", path="circuits/providers/"),
        "provider_account": ParamPath(param="provider_account", path="circuits/provider-accounts/"),
        # dcim
        "device_type": ParamPath(param="device_type", path="dcim/device-types/", key="model"),
        "location": ParamPath(param="location", path="dcim/locations/"),
        "manufacturer": ParamPath(param="manufacturer", path="dcim/manufacturers/"),
        "platform": ParamPath(param="platform", path="dcim/platforms/"),
        "rack": ParamPath(param="rack", path="dcim/racks/"),
        "region": ParamPath(param="region", path="dcim/regions/"),
        "site": ParamPath(param="site", path="dcim/sites/"),
        "site_group": ParamPath(param="site_group", path="dcim/site-groups/"),
        # extras
        "content_type": ParamPath(
            param="content_type", path="extras/content-types/", key="display"
        ),
        "for_object_type": ParamPath(
            param="for_object_type", path="extras/content-types/", key="display"
        ),
        # ipam
        "export_target": ParamPath(param="export_target", path="ipam/route-targets/"),
        "exporting_vrf": ParamPath(param="exporting_vrf", path="ipam/vrfs/"),
        "import_target": ParamPath(param="import_target", path="ipam/route-targets/"),
        "importing_vrf": ParamPath(param="importing_vrf", path="ipam/vrfs/"),
        "present_in_vrf": ParamPath(param="present_in_vrf", path="ipam/vrfs/"),
        "rir": ParamPath(param="rir", path="ipam/rirs/"),
        "vrf": ParamPath(param="vrf", path="ipam/vrfs/"),
        # tenancy
        "tenant": ParamPath(param="tenant", path="tenancy/tenants/"),
        "tenant_group": ParamPath(param="tenant_group", path="tenancy/tenant-groups/"),
        # virtualization
        "bridge": ParamPath(param="bridge", path="virtualization/interfaces/"),
    }

    # group
    group_map: DDParamPath = {
        "dcim/sites/": {"group": ParamPath(param="group", path="dcim/site-groups/")},
        "ipam/vlans/": {"group": ParamPath(param="group", path="ipam/vlan-groups/")},
        "tenancy/tenants/": {"group": ParamPath(param="group", path="tenancy/tenant-groups/")},
        "virtualization/clusters/": {
            "group": ParamPath(param="group", path="virtualization/cluster-groups/")
        },
    }
    if data_ := group_map.get(path):
        result.update(data_)

    # parent
    parent_map: DDParamPath = {
        # "ipam/ip-addresses/":, "parent" mapping is not required
        "dcim/locations/": {"parent": ParamPath(param="parent", path="dcim/locations/")},
        "dcim/regions/": {"parent": ParamPath(param="parent", path="dcim/regions/")},
        "dcim/site-groups/": {"parent": ParamPath(param="parent", path="dcim/site-groups/")},
        "tenancy/tenant-groups/": {
            "parent": ParamPath(param="parent", path="tenancy/tenant-groups/")
        },
        "virtualization/interfaces/": {
            "parent": ParamPath(param="parent", path="virtualization/interfaces/")
        },
    }
    if data_ := parent_map.get(path):
        result.update(data_)

    # role
    if path.startswith("dcim/devices/"):
        result["role"] = ParamPath(param="role", path="dcim/device-roles/")
    elif path.startswith("dcim/racks/"):
        result["role"] = ParamPath(param="role", path="dcim/rack-roles/")
    elif path.startswith("ipam/"):
        result["role"] = ParamPath(param="role", path="ipam/roles/")
    elif path == "virtualization/virtual-machines/":
        result["role"] = ParamPath(param="role", path="dcim/device-roles/")

    # type
    if path == "circuits/circuits/":
        result["type"] = ParamPath(param="type", path="circuits/circuit-types/")

    return result


def need_change(params_d: DList, mapping: DParamPath) -> DList:
    """Filter ``{parameter}`` that need change to ``{parameter}_id``.

    Skip parameter for global vrf filtering.
    :param params_d: Parameters that need to filter.
    :param mapping: Dictionary of ParamIdMap objects.
    :return: Parameters that need to change.
    """
    need_change_d: DList = {}

    for key, values in params_d.items():
        if key.startswith("or_"):
            key = key.replace("or_", "", 1)
        if key not in mapping:
            continue
        if key in ["vrf", "present_in_vrf"]:
            if values == ["null"]:
                continue
        need_change_d[key] = values

    return need_change_d
