"""api."""

from __future__ import annotations

from typing import Union

from netbox3.api.circuits import CircuitsAC
from netbox3.api.core import CoreAC
from netbox3.api.dcim import DcimAC
from netbox3.api.extras import ExtrasAC
from netbox3.api.ipam import IpamAC
from netbox3.api.tenancy import TenancyAC
from netbox3.api.users import UsersAC
from netbox3.api.virtualization import VirtualizationAC
from netbox3.api.wireless import WirelessAC

ConnectorA = Union[
    CircuitsAC,
    CoreAC,
    DcimAC,
    ExtrasAC,
    IpamAC,
    TenancyAC,
    UsersAC,
    VirtualizationAC,
    WirelessAC,
]

APPS = [
    "circuits",
    "core",
    "dcim",
    "extras",
    "ipam",
    "plugins",
    "tenancy",
    "users",
    "virtualization",
    "wireless",
]
