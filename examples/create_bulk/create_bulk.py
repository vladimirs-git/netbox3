"""Create the objects used in other examples."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

COUNT = 2  # object count

ASN_RANGE = "ASN RANGE"
CID = "CID"
CIRCUIT_TYPE = "CIRCUIT TYPE"
CLUSTER = "CLUSTER"
CLUSTER_GROUP = "CLUSTER GROUP"
CLUSTER_TYPE = "CLUSTER TYPE"
COMMENT = "COMMENT"
DESCRIPTION = "DESCRIPTION"
DEVICE = "DEVICE"
DEVICE_ROLE = "DEVICE ROLE"
INTERFACE = "INTERFACE"
LOCATION = "LOCATION"
MANUFACTURER = "MANUFACTURER"
MODEL = "MODEL"
PLATFORM = "PLATFORM"
PROVIDER = "PROVIDER"
PROVIDER_ACCOUNT = "PROVIDER ACCOUNT"
PROVIDER_NETWORK = "PROVIDER NETWORK"
RACK = "RACK"
RACK_ROLE = "RACK ROLE"
REGION = "REGION"
ROLE = "ROLE"
SITE = "SITE"
SITE_GROUP = "SITE GROUP"
TAG = "TAG"
TENANT = "TENANT"
TENANT_GROUP = "TENANT GROUP"
VIRTUAL_MACHINE = "VIRTUAL MACHINE"
VLAN = "VLAN"
VLAN_GROUP = "VLAN GROUP"
VRF = "VRF"

AGGREGATE1 = "10.0.0.0/8"
AGGREGATE2 = "192.168.0.0/16"
IP_ADDRESS1 = "10.1.1.1/24"
IP_ADDRESS2 = "10.2.2.1/28"
PREFIX1 = "10.1.1.0/24"
PREFIX2 = "10.2.2.0/28"


def slug(name):
    """Create the slug based on the name."""
    return "-".join(name.lower().split())


# noinspection DuplicatedCode
def create__circuits__circuit_terminations():
    """Create /circuits/circuit-terminations objects."""
    for idx in range(1, COUNT + 1):
        cid = f"{CID}{idx}"
        c_id = nb.circuits.circuits.get(cid=cid)[0]["id"]

        for idx_, side in enumerate(["A", "Z"], start=1):
            if not nb.circuits.circuit_terminations.get(circuit_id=c_id):
                response = nb.circuits.circuit_terminations.create(
                    circuit=c_id,
                    site=nb.dcim.sites.get(name=f"{SITE}{idx_}")[0]["id"],
                    term_side=side,
                )
                print(response)

        for idx_, side in enumerate(["A", "Z"], start=1):
            response = nb.circuits.circuit_terminations.update(
                id=nb.circuits.circuit_terminations.get(circuit_id=c_id)[0]["id"],
                circuit=c_id,
                term_side=side,

                site=nb.dcim.sites.get(name=f"{SITE}{idx_}")[0]["id"],
                # Termination,
                port_speed=100000 * idx,
                # Cross-Connect,
                # Patch Panel/Port,
                description=f"{DESCRIPTION}{idx}",
                tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
            )
            print(response)


# noinspection DuplicatedCode
def create__circuits__circuit_types():
    """Create /circuits/circuit-types objects."""
    for idx in range(1, COUNT + 1):
        name = f"{CIRCUIT_TYPE}{idx}"
        if not nb.circuits.circuit_types.get(name=name):
            response = nb.circuits.circuit_types.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.circuits.circuit_types.update(
            id=nb.circuits.circuit_types.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__circuits__circuits():
    """Create /circuits/circuits objects."""
    for idx in range(1, COUNT + 1):
        cid = f"{CID}{idx}"
        if not nb.circuits.circuits.get(cid=cid):
            response = nb.circuits.circuits.create(
                provider=nb.circuits.providers.get(name=f"{PROVIDER}{idx}")[0]["id"],
                cid=cid,
                type=nb.circuits.circuit_types.get(name=f"{CIRCUIT_TYPE}{idx}")[0]["id"],
            )
            print(response)

        response = nb.circuits.circuits.update(
            id=nb.circuits.circuits.get(cid=cid)[0]["id"],
            provider=nb.circuits.providers.get(name=f"{PROVIDER}{idx}")[0]["id"],
            provider_account=nb.circuits.provider_accounts.get(
                account=idx, provider=f"{PROVIDER}{idx}",
            )[0]["id"],
            cid=cid,
            type=nb.circuits.circuit_types.get(name=f"{CIRCUIT_TYPE}{idx}")[0]["id"],
            status="active",
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Service Parameters
            # Installed,
            # Terminates,
            # Commit rate (Kbps),

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__circuits__provider_accounts():
    """Create /circuits/provider-accounts objects."""
    for idx in range(1, COUNT + 1):
        name = f"{PROVIDER_ACCOUNT}{idx}"
        provider = f"{PROVIDER}{idx}"
        if not nb.circuits.provider_accounts.get(account=idx):
            response = nb.circuits.provider_accounts.create(
                provider=nb.circuits.providers.get(name=provider)[0]["id"],
                account=idx,
            )
            print(response)

        response = nb.circuits.provider_accounts.update(
            id=nb.circuits.provider_accounts.get(account=idx, provider=provider)[0]["id"],
            provider=nb.circuits.providers.get(name=provider)[0]["id"],
            name=name,
            account=idx,
            description=f"{DESCRIPTION}{idx}",
            comments=f"{COMMENT}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__circuits__provider_networks():
    """Create /circuits/provider-networks objects."""
    for idx in range(1, COUNT + 1):
        name = f"{PROVIDER_NETWORK}{idx}"
        if not nb.circuits.provider_networks.get(name=name):
            response = nb.circuits.provider_networks.create(
                provider=nb.circuits.providers.get(name=f"{PROVIDER}{idx}")[0]["id"],
                name=name,
            )
            print(response)

        response = nb.circuits.provider_networks.update(
            id=nb.circuits.provider_networks.get(name=name)[0]["id"],
            provider=nb.circuits.providers.get(name=f"{PROVIDER}{idx}")[0]["id"],
            name=name,
            service_id=f"service{idx}",
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__circuits__providers():
    """Create /circuits/providers objects."""
    for idx in range(1, COUNT + 1):
        name = f"{PROVIDER}{idx}"
        if not nb.circuits.providers.get(name=name):
            response = nb.circuits.providers.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.circuits.providers.update(
            id=nb.circuits.providers.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            asns=[nb.ipam.asns.get(asn=65100 + idx)[0]["id"]],
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__device_roles():
    """Create /dcim/device-roles objects."""
    for idx in range(1, COUNT + 1):
        name = f"{DEVICE_ROLE}{idx}"
        if not nb.dcim.device_roles.get(name=name):
            response = nb.dcim.device_roles.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.device_roles.update(
            id=nb.dcim.device_roles.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            color="aa1409",  # dark red
            vm_role=False,
            # Config template,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)

    # virtualization
    response = nb.dcim.device_roles.update(
        id=nb.dcim.device_roles.get(name=f"{DEVICE_ROLE}2")[0]["id"],
        vm_role=True,
    )
    print(response)


# noinspection DuplicatedCode
def create__dcim__device_types():
    """Create /dcim/device-types objects."""
    for idx in range(1, COUNT + 1):
        model = f"{MODEL}{idx}"
        if not nb.dcim.device_types.get(model=model):
            response = nb.dcim.device_types.create(
                manufacturer=nb.dcim.manufacturers.get(name=f"{MANUFACTURER}{idx}")[0]["id"],
                model=model,
                slug=slug(model),
            )
            print(response)

        response = nb.dcim.device_types.update(
            # Device Type
            id=nb.dcim.device_types.get(model=model)[0]["id"],
            manufacturer=nb.dcim.manufacturers.get(name=f"{MANUFACTURER}{idx}")[0]["id"],
            model=model,
            slug=slug(model),
            # default_platform=id,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Chassis
            u_height=1,
            is_full_depth=True,
            part_number=f"part_number{idx}",
            # Parent/child status
            airflow="rear-to-front",  # front-to-rear, rear-to-front, ...
            weight=idx,
            weight_unit="kg",  # kg, g, ...
            # Front image
            # Rear image

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__devices():
    """Create /dcim/devices objects."""
    for idx in range(1, COUNT + 1):
        name = f"{DEVICE}{idx}"
        if not nb.dcim.devices.get(name=name):
            response = nb.dcim.devices.create(
                name=name,
                role=nb.dcim.device_roles.get(name=f"{DEVICE_ROLE}{idx}")[0]["id"],
                device_type=nb.dcim.device_types.get(model=f"{MODEL}{idx}")[0]["id"],
                site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
            )
            print(response)

        response = nb.dcim.devices.update(
            id=nb.dcim.devices.get(name=name)[0]["id"],
            name=name,
            device_role=nb.dcim.device_roles.get(name=f"{DEVICE_ROLE}{idx}")[0]["id"],
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Hardware
            device_type=nb.dcim.device_types.get(model=f"{MODEL}{idx}")[0]["id"],
            airflow="rear-to-front",  # front-to-rear, rear-to-front, ...
            serial=f"serial{idx}",
            # Asset tag,

            # Location
            site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
            location=nb.dcim.locations.get(name=f"{LOCATION}{idx}")[0]["id"],
            rack=nb.dcim.racks.get(name=f"{RACK}{idx}")[0]["id"],
            # Rack face,
            # Position,
            # Latitude,
            # Longitude,

            # Management
            status="active",
            platform=nb.dcim.platforms.get(name=f"{PLATFORM}{idx}")[0]["id"],
            # Config template,

            # Virtualization
            # Cluster,

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            # Virtual Chassis
            # Virtual chassis,
            # Position,
            # Priority,

            # Local Config Context Data

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__interfaces():
    """Create /dcim/interfaces objects."""
    for idx_ in range(1, COUNT + 1):
        device_name = f"{DEVICE}{idx_}"
        device_id = nb.dcim.devices.get(name=device_name)[0]["id"]

        for idx in range(1, COUNT + 1):
            name = f"GigabitEthernet1/0/{idx}"
            if not nb.dcim.interfaces.get(name=name, device=device_name):
                response = nb.dcim.interfaces.create(
                    device=device_id,
                    name=name,
                    type="1000base-x-sfp",
                )
                print(response)

            response = nb.dcim.interfaces.update(
                id=nb.dcim.interfaces.get(name=name, device=device_name)[0]["id"],
                device=device_id,
                # Module,
                name=name,
                label=f"label{idx}",
                type="1000base-x-sfp",
                speed=1000000,
                duplex="auto",
                description=f"{DESCRIPTION}{idx}",
                tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

                # Addressing
                # VRF,
                mac_address=f"00000000000{idx}",
                # WWN,
                enabled=True,
                mgmt_only=True,
                # Mark connected,

                # Related Interfaces
                # Parent interface,
                # Bridged interface,
                # LAG interface,

                # PoE
                # PoE mode,
                # PoE type,

                # 802.1Q Switching
                # 802.1Q Mode,

                # Wireless
                # Wireless role,
                # Wireless channel,
                # Channel frequency (MHz),
                # Channel width (MHz),
                # Wireless LAN group,
                # Wireless LANs,
            )
            print(response)


# noinspection DuplicatedCode
def create__dcim__platforms():
    """Create /dcim/platforms objects."""
    for idx in range(1, COUNT + 1):
        name = f"{PLATFORM}{idx}"
        if not nb.dcim.platforms.get(name=name):
            response = nb.dcim.platforms.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.platforms.update(
            id=nb.dcim.platforms.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            manufacturer=nb.dcim.manufacturers.get(name=f"{MANUFACTURER}{idx}")[0]["id"],
            # Config template,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__locations():
    """Create /dcim/locations objects."""
    for idx in range(1, COUNT + 1):
        name = f"{LOCATION}{idx}"
        if not nb.dcim.locations.get(name=name):
            response = nb.dcim.locations.create(
                site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.locations.update(
            id=nb.dcim.locations.get(name=name)[0]["id"],
            site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
            name=name,
            slug=slug(name),
            status="active",
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],
        )
        print(response)

    # NOTE parent not working
    if nb.dcim.locations.get(name=f"{LOCATION}3"):
        response = nb.dcim.locations.update(
            id=nb.dcim.locations.get(name=f"{LOCATION}3")[0]["id"],
            paren=nb.dcim.locations.get(name=f"{LOCATION}2")[0]["id"],
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__manufacturers():
    """Create /dcim/manufacturers objects."""
    for idx in range(1, COUNT + 1):
        name = f"{MANUFACTURER}{idx}"
        if not nb.dcim.manufacturers.get(name=name):
            response = nb.dcim.manufacturers.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.manufacturers.update(
            id=nb.dcim.manufacturers.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__rack_roles():
    """Create /dcim/rack-roles objects."""
    for idx in range(1, COUNT + 1):
        name = f"{RACK_ROLE}{idx}"
        if not nb.dcim.rack_roles.get(name=name):
            response = nb.dcim.rack_roles.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.rack_roles.update(
            id=nb.dcim.rack_roles.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            color="aa1409",  # dark red
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__racks():
    """Create /dcim/racks objects."""
    for idx in range(1, COUNT + 1):
        name = f"{RACK}{idx}"
        if not nb.dcim.racks.get(name=name):
            response = nb.dcim.racks.create(
                site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
                name=name,
            )
            print(response)

        response = nb.dcim.racks.update(
            id=nb.dcim.racks.get(name=name)[0]["id"],
            site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
            location=nb.dcim.locations.get(name=f"{LOCATION}{idx}")[0]["id"],
            name=name,
            status="active",
            role=nb.dcim.rack_roles.get(name=f"{RACK_ROLE}{idx}")[0]["id"],
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Inventory Control
            facility=f"facility{idx}",
            # Serial number,
            # Asset tag,

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            # Dimensions
            # Type,
            # Width,
            # Starting unit,
            # Height (U),
            # Outer Dimensions,
            # Mounting depth,

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__dcim__regions():
    """Create /dcim/regions objects."""
    for idx in range(1, COUNT + 1):
        name = f"{REGION}{idx}"
        if not nb.dcim.regions.get(name=name):
            response = nb.dcim.regions.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.regions.update(
            id=nb.dcim.regions.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)

    # NOTE parent not working
    response = nb.dcim.regions.update(
        id=nb.dcim.regions.get(name=f"{REGION}2")[0]["id"],
        paren=nb.dcim.regions.get(name=f"{REGION}1")[0]["id"],
    )
    print(response)


# noinspection DuplicatedCode
def create__dcim__site_groups():
    """Create /dcim/site-groups objects."""
    for idx in range(1, COUNT + 1):
        name = f"{SITE_GROUP}{idx}"
        if not nb.dcim.site_groups.get(name=name):
            response = nb.dcim.site_groups.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.site_groups.update(
            id=nb.dcim.site_groups.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)

    # NOTE parent not working
    response = nb.dcim.site_groups.update(
        id=nb.dcim.site_groups.get(name=f"{SITE_GROUP}2")[0]["id"],
        paren=nb.dcim.site_groups.get(name=f"{SITE_GROUP}1")[0]["id"],
    )
    print(response)


# noinspection DuplicatedCode
def create__dcim__sites():
    """Create /dcim/sites objects."""
    for idx in range(1, COUNT + 1):
        name = f"{SITE}{idx}"
        if not nb.dcim.sites.get(name=name):
            response = nb.dcim.sites.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.dcim.sites.update(
            id=nb.dcim.sites.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            status="active",
            region=nb.dcim.regions.get(name=f"{REGION}{idx}")[0]["id"],
            group=nb.dcim.site_groups.get(name=f"{SITE_GROUP}{idx}")[0]["id"],
            facility=f"facility{idx}",
            # asns=[nb.ipam.asns.get(asn=65100 + idx)[0]["id"]],
            # Time zone,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            # Contact Info
            # Physical address,
            # Shipping address,
            # Latitude,
            # Longitude,

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__extras__custom_field():
    """Create /extras/custom-fields objects."""
    for idx in range(1, COUNT + 1):
        ascii_a = 97 - 1
        name = f"custom_field_{chr(ascii_a + idx)}"
        if not nb.extras.custom_fields.get(name=name):
            response = nb.extras.custom_fields.create(
                name=name,
                content_types=["ipam.ipaddress"],
                type="text",
            )
            print(response)

        response = nb.extras.custom_fields.update(
            id=nb.extras.custom_fields.get(name=name)[0]["id"],

            # Custom Field
            content_types=["ipam.ipaddress"],
            name=name,
            label=f"label_{chr(ascii_a + idx)}",
            group_name=f"group{idx}",
            type="text",  # "text", "selection", ...
            # object_type="ipam.ipaddress",  # used for type="object"
            required=False,
            description=f"{DESCRIPTION}{idx}",

            # Behavior
            search_weight=1000 + idx,
            filter_loggic="loose",  # "exact", "disabled", "loose"
            ui_visibility="read-only",  # "read-write", ...
            weight=100 + idx,
            is_cloneable=False,

            # Values
            default=f"value{idx}",
            # choice_set="",  # for type="selection"
        )
        print(response)


# noinspection DuplicatedCode
def create__extras__tags():
    """Create /extras/tags objects."""
    for idx in range(1, COUNT + 1):
        name = f"{TAG}{idx}"
        if not nb.extras.tags.get(name=name):
            response = nb.extras.tags.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.extras.tags.update(
            id=nb.extras.tags.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            color="aa1409",  # dark red
            description=f"{DESCRIPTION}{idx}",
            # object_types=['circuits.circuit'],
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__aggregates():
    """Create /ipam/aggregates objects."""
    for idx, prefix in enumerate([AGGREGATE1, AGGREGATE2], start=1):
        rir = nb.ipam.rirs.get(name="RFC 1918")[0]["id"]
        if not nb.ipam.aggregates.get(prefix=prefix):
            response = nb.ipam.aggregates.create(
                prefix=prefix,
                rir=rir,
            )
            print(response)

        response = nb.ipam.aggregates.update(
            id=nb.ipam.aggregates.get(prefix=prefix)[0]["id"],
            prefix=prefix,
            rir=rir,
            # Date added,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__asn_ranges():
    """Create /ipam/asn-ranges objects."""
    for idx in range(1, COUNT + 1):
        name = f"{ASN_RANGE}{idx}"
        if not nb.ipam.asn_ranges.get(name=name):
            response = nb.ipam.asn_ranges.create(
                name=name,
                slug=slug(name),
                rir=nb.ipam.rirs.get(name="RFC 6996")[0]["id"],
                start=65000 + (100 * idx) + 1,
                end=65000 + (100 * idx) + 3,
            )
            print(response)

        response = nb.ipam.asn_ranges.update(
            id=nb.ipam.asn_ranges.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            rir=nb.ipam.rirs.get(name="RFC 6996")[0]["id"],
            start=65000 + (100 * idx) + 1,
            end=65000 + (100 * idx) + 3,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__asns():
    """Create /ipam/asns objects."""
    for idx in range(1, COUNT + 1):
        asn = 65100 + idx
        if not nb.ipam.asns.get(asn=asn):
            response = nb.ipam.asns.create(
                asn=asn,
                rir=nb.ipam.rirs.get(name="RFC 6996")[0]["id"],
            )
            print(response)

        response = nb.ipam.asns.update(
            # ASN
            id=nb.ipam.asns.get(asn=asn)[0]["id"],
            asn=asn,
            rir=nb.ipam.rirs.get(name="RFC 6996")[0]["id"],
            # Sites,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__ip_addresses():
    """Create /ipam/ip-addresses objects."""
    for idx, address in enumerate([IP_ADDRESS1, IP_ADDRESS2], start=1):
        if not nb.ipam.ip_addresses.get(address=address):
            response = nb.ipam.ip_addresses.create(
                address=address,
            )
            print(response)

        response = nb.ipam.ip_addresses.update(
            id=nb.ipam.ip_addresses.get(address=address)[0]["id"],
            address=address,
            status="active",
            role="loopback",
            vrf=nb.ipam.vrfs.get(name=f"{VRF}{idx}")[0]["id"],
            dns_name="domain.com",
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            # Interface Assignment
            # Interface,
            # Device, Virtual Machine, FHRP Group,

            # NAT IP (Inside)
            # IP Address,

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__prefixes():
    """Create /ipam/prefixes objects."""
    for idx, prefix in enumerate([PREFIX1, PREFIX2], start=1):
        if not nb.ipam.prefixes.get(prefix=prefix):
            response = nb.ipam.prefixes.create(
                prefix=prefix,
            )
            print(response)

        response = nb.ipam.prefixes.update(
            id=nb.ipam.prefixes.get(prefix=prefix)[0]["id"],
            prefix=prefix,
            status="active",
            vrf=nb.ipam.vrfs.get(name=f"{VRF}{idx}")[0]["id"],
            role=nb.ipam.roles.get(name=f"{ROLE}{idx}")[0]["id"],
            # Is a pool,
            # Mark utilized,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Site/VLAN Assignment
            site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
            vlan=nb.ipam.vlans.get(name=f"{VLAN}{idx}")[0]["id"],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__rirs():
    """Create /ipam/rirs objects."""
    for idx, name in enumerate(["RFC 1918", "RFC 6996"], start=1):
        if not nb.ipam.rirs.get(name=name):
            response = nb.ipam.rirs.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.ipam.rirs.update(
            id=nb.ipam.rirs.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            # description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__route_targets():
    """Create /ipam/route-targets objects."""
    for idx in range(1, COUNT + 1):
        name = f"6510{idx}:1"
        if not nb.ipam.route_targets.get(name=name):
            response = nb.ipam.route_targets.create(
                name=name,
            )
            print(response)

        response = nb.ipam.route_targets.update(
            id=nb.ipam.route_targets.get(name=name)[0]["id"],
            name=name,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__roles():
    """Create /ipam/roles objects."""
    for idx in range(1, COUNT + 1):
        name = f"{ROLE}{idx}"
        if not nb.ipam.roles.get(name=name):
            response = nb.ipam.roles.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.ipam.roles.update(
            id=nb.ipam.roles.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            weight=1000 + idx,
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__vlan_groups():
    """Create /ipam/vlan-groups objects."""
    for idx in range(1, COUNT + 1):
        name = f"{VLAN_GROUP}{idx}"
        if not nb.ipam.vlan_groups.get(name=name):
            response = nb.ipam.vlan_groups.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.ipam.vlan_groups.update(
            id=nb.ipam.vlan_groups.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Child VLANs
            min_vid=1,
            max_vid=4094,
            scope_type="dcim.site",
            scope_id=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__vlans():
    """Create /ipam/vlans objects."""
    for idx in range(1, COUNT + 1):
        name = f"{VLAN}{idx}"
        if not nb.ipam.vlans.get(name=name):
            response = nb.ipam.vlans.create(
                vid=idx,
                name=name,
            )
            print(response)

        response = nb.ipam.vlans.update(
            id=nb.ipam.vlans.get(name=name)[0]["id"],
            vid=idx,
            name=name,
            status="active",
            role=nb.ipam.roles.get(name=f"{ROLE}{idx}")[0]["id"],
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            # Assignment
            group=nb.ipam.vlan_groups.get(name=f"{VLAN_GROUP}{idx}")[0]["id"],  # group or site
            # site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],  # group or site

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__ipam__vrfs():
    """Create /ipam/vrfs objects."""
    for idx in range(1, COUNT + 1):
        name = f"{VRF}{idx}"
        if not nb.ipam.vrfs.get(name=name):
            response = nb.ipam.vrfs.create(
                name=name,
            )
            print(response)

        response = nb.ipam.vrfs.update(
            id=nb.ipam.vrfs.get(name=name)[0]["id"],
            name=name,
            rd=nb.ipam.route_targets.get(name=f"6510{idx}:1")[0]["id"],
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Route Targets
            import_targets=[nb.ipam.route_targets.get(name=f"6510{idx}:1")[0]["id"]],
            export_targets=[nb.ipam.route_targets.get(name=f"6510{idx}:1")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__tenancy__tenant_groups():
    """Create /dcim/tenant-groups objects."""
    for idx in range(1, COUNT + 1):
        name = f"{TENANT_GROUP}{idx}"
        if not nb.tenancy.tenant_groups.get(name=name):
            response = nb.tenancy.tenant_groups.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.tenancy.tenant_groups.update(
            id=nb.tenancy.tenant_groups.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)

    # NOTE parent not working
    response = nb.tenancy.tenant_groups.update(
        id=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}2")[0]["id"],
        paren=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}1")[0]["id"],
    )
    print(response)


# noinspection DuplicatedCode
def create__tenancy__tenants():
    """Create /dcim/tenants objects."""
    for idx in range(1, COUNT + 1):
        name = f"{TENANT}{idx}"
        if not nb.tenancy.tenants.get(name=name):
            response = nb.tenancy.tenants.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.tenancy.tenants.update(
            id=nb.tenancy.tenants.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__virtualization__cluster_groups():
    """Create /virtualization/cluster-groups objects."""
    for idx in range(1, COUNT + 1):
        name = f"{CLUSTER_GROUP}{idx}"
        if not nb.virtualization.cluster_groups.get(name=name):
            response = nb.virtualization.cluster_groups.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.virtualization.cluster_groups.update(
            id=nb.virtualization.cluster_groups.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__virtualization__cluster_types():
    """Create /virtualization/cluster-types objects."""
    for idx in range(1, COUNT + 1):
        name = f"{CLUSTER_TYPE}{idx}"
        if not nb.virtualization.cluster_types.get(name=name):
            response = nb.virtualization.cluster_types.create(
                name=name,
                slug=slug(name),
            )
            print(response)

        response = nb.virtualization.cluster_types.update(
            id=nb.virtualization.cluster_types.get(name=name)[0]["id"],
            name=name,
            slug=slug(name),
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],
        )
        print(response)


# noinspection DuplicatedCode
def create__virtualization__clusters():
    """Create /virtualization/clusters objects."""
    for idx in range(1, COUNT + 1):
        name = f"{CLUSTER}{idx}"
        if not nb.virtualization.clusters.get(name=name):
            response = nb.virtualization.clusters.create(
                name=name,
                type=nb.virtualization.cluster_types.get(name=f"{CLUSTER_TYPE}{idx}")[0]["id"],
            )
            print(response)

        response = nb.virtualization.clusters.update(
            id=nb.virtualization.clusters.get(name=name)[0]["id"],
            name=name,
            type=nb.virtualization.cluster_types.get(name=f"{CLUSTER_TYPE}{idx}")[0]["id"],
            group=nb.virtualization.cluster_groups.get(name=f"{CLUSTER_GROUP}{idx}")[0]["id"],
            site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],
            status="active",
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            comments=f"{COMMENT}{idx}",
        )
        print(response)


# noinspection DuplicatedCode
def create__virtualization__interfaces():
    """Create /virtualization/interfaces objects."""
    for idx_ in range(1, COUNT + 1):
        vm_name = f"{VIRTUAL_MACHINE}{idx_}"

        vm_ids = nb.virtualization.virtual_machines.get(name=vm_name)
        if len(vm_ids) != 1:
            raise ValueError(f"{len(vm_ids)=} expected 1")
        vm_id = vm_ids[0]["id"]

        for idx in range(1, COUNT + 1):
            name = f"{INTERFACE}{idx}"
            if not nb.virtualization.interfaces.get(name=name, virtual_machine=vm_name):
                response = nb.virtualization.interfaces.create(
                    virtual_machine=vm_id,
                    name=name,
                )
                print(response)

            response = nb.virtualization.interfaces.update(
                # Interface
                id=nb.virtualization.interfaces.get(name=name, virtual_machine=vm_name)[0]["id"],
                virtual_machine=vm_id,
                description=f"{DESCRIPTION}{idx}",
                tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

                # Addressing
                vrf=nb.ipam.vrfs.get(name=f"{VRF}{idx}")[0]["id"],
                mac_address=f"00000000000{idx}",

                # Operation
                # MTU,
                # Enabled,

                # Related Interfaces
                # Parent interface,
                # Bridged interface,

                # 802.1Q Switching
                # 802.1Q Mode,
            )
            print(response)


# noinspection DuplicatedCode
def create__virtualization__virtual_machines():
    """Create /virtualization/virtual-machines objects."""
    for idx in range(1, COUNT + 1):
        name = f"{VIRTUAL_MACHINE}{idx}"
        if not nb.virtualization.virtual_machines.get(name=name):
            response = nb.virtualization.virtual_machines.create(
                name=name,
                # site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],  # site or cluster
                # site or cluster
                cluster=nb.virtualization.clusters.get(name=f"{CLUSTER}{idx}")[0]["id"],
            )
            print(response)

        response = nb.virtualization.virtual_machines.update(
            id=nb.virtualization.virtual_machines.get(name=name)[0]["id"],
            name=name,
            role=nb.dcim.device_roles.get(q=f"{DEVICE_ROLE}", vm_role=True)[0]["id"],
            status="active",
            description=f"{DESCRIPTION}{idx}",
            tags=[nb.extras.tags.get(name=f"{TAG}{idx}")[0]["id"]],

            # Site/Cluster
            # site=nb.dcim.sites.get(name=f"{SITE}{idx}")[0]["id"],  # site or cluster
            # site or cluster
            cluster=nb.virtualization.clusters.get(name=f"{CLUSTER}{idx}")[0]["id"],
            # device=nb.virtualization.virtual_machines.get(name=f"{DEVICE}{idx}")[0]["id"],

            # Tenancy
            tenant_group=nb.tenancy.tenant_groups.get(name=f"{TENANT_GROUP}{idx}")[0]["id"],
            tenant=nb.tenancy.tenants.get(name=f"{TENANT}{idx}")[0]["id"],

            # Management
            platform=nb.dcim.platforms.get(name=f"{PLATFORM}{idx}")[0]["id"],
            # Primary IPv4,
            # Primary IPv6,
            # Config template,

            # Resources
            # VCPUs,
            # Memory (MB),
            # Disk (GB),

            # Config Context,

            comments=f"{COMMENT}{idx}",
        )
        print(response)


def join__ipam__asns_sites():
    """Join ipam objects."""
    for idx in range(1, COUNT + 1):
        name = f"{SITE}{idx}"

        response = nb.dcim.sites.update(
            id=nb.dcim.sites.get(name=name)[0]["id"],
            asns=[nb.ipam.asns.get(asn=65100 + idx)[0]["id"]],
        )
        print(response)


if __name__ == "__main__":
    # 1 extras
    create__extras__tags()
    create__extras__custom_field()

    # 2 tenancy
    create__tenancy__tenant_groups()  # tags
    create__tenancy__tenants()  # tenant_groups

    # 3 dcim location
    create__dcim__rack_roles()  # tags
    create__dcim__regions()  # tags
    create__dcim__site_groups()  # tags
    create__dcim__sites()  # asns, regions, site_groups, tenants
    create__dcim__locations()  # sites, tenants
    create__dcim__racks()  # rack_roles, locations, sites, tenants,

    # 4 ipam
    create__ipam__rirs()  # tags
    create__ipam__roles()  # tags
    create__ipam__asns()  # rirs, tenants
    create__ipam__asn_ranges()  # rirs, tenants
    join__ipam__asns_sites()  # asns, sites
    # vrf
    create__ipam__route_targets()  # tenants
    create__ipam__vrfs()  # route_targets, tenants
    # vlan
    create__ipam__vlan_groups()  # locations, regions, sites, racks
    create__ipam__vlans()  # roles, sites, tenants
    # prefixes
    create__ipam__aggregates()  # rirs, tenants
    create__ipam__prefixes()  # vlan, vrfs, tenants
    create__ipam__ip_addresses()  # vrfs, tenants

    # 5 circuits
    create__circuits__circuit_types()  # tags
    create__circuits__providers()  # asns
    create__circuits__provider_accounts()  # providers
    create__circuits__provider_networks()  # providers
    create__circuits__circuits()  # circuit_types, providers, tenants
    create__circuits__circuit_terminations()  # circuits, sites, interfaces, devices

    # 6 devices
    create__dcim__manufacturers()  # tags
    create__dcim__device_roles()  # config_templates
    create__dcim__device_types()  # manufacturers
    create__dcim__platforms()  # manufacturers, config_templates
    create__dcim__devices()  # sites, racks, platforms, ip_addresses
    create__dcim__interfaces()  # devices, vlans

    # 7 virtualization
    create__virtualization__cluster_groups()  # tags
    create__virtualization__cluster_types()  # tags
    create__virtualization__clusters()  # sites, cluster_groups, cluster_types
    create__virtualization__virtual_machines()  # cluster
    create__virtualization__interfaces()  # virtual_machines
