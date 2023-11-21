"""Delete the objects used in other examples."""
import logging

# noinspection PyProtectedMember
from examples.create_bulk import create_bulk as ca
from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

nb = NbApi(host=ca.HOST, token=ca.TOKEN)

ITEMS = [
    # virtualization
    "virtual_machines",
    "clusters",
    "cluster_types",
    "cluster_groups",
    # devices
    "devices",
    "platforms",
    "device_types",
    "device_roles",
    "manufacturers",
    # ipam
    "ip_addresses",
    "ip_addresses",
    "prefixes",
    "prefixes",
    "aggregates",
    "aggregates",
    "vlans",
    "vlan_groups",
    "vrfs",
    "route_targets",
    "route_targets",
    "asn_ranges",
    "asns",
    "asns",
    "roles",
    # circuits
    "circuit_terminations",
    "circuits_",
    "provider_networks",
    "provider_accounts",
    "providers",
    "circuit_types",
    # dcim location
    "racks",
    "locations",
    "sites",
    "site_groups",
    "regions",
    "rack_roles",
    # tenancy
    "tenants",
    "tenant_groups",
]


def delete_objects(models: list):
    """Delete objects from the Netbox."""
    for model in models:
        tags = [f"{ca.TAG}{i}".lower() for i in range(1, ca.COUNT + 1)]
        objects = getattr(nb, model).get(or_tag=tags)
        for data in objects:
            response = getattr(nb, model).delete(id=data["id"])
            print(response, model, len(objects))


if __name__ == "__main__":
    delete_objects(ITEMS)
