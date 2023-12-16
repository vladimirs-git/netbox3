"""Create a group of interfaces."""
import logging

from demo.create_bulk.create_bulk import create__extras__tags, create__ipam__vrfs
from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)


# noinspection DuplicatedCode
def _create_address(address, tag, vrf):
    """Create address"""
    if not nb.ipam.ip_addresses.get(address=address, vrf_id=vrf):
        params = dict(address=address, tags=[tag])
        if vrf:
            params["vrf"] = vrf
        response = nb.ipam.ip_addresses.create(**params)
        print(f"{response} {address=}")


# noinspection DuplicatedCode
def _create_prefix(prefix, tag, vrf):
    """Create prefix"""
    if not nb.ipam.prefixes.get(prefix=prefix, vrf_id=vrf):
        params = dict(prefix=prefix, tags=[tag])
        if vrf:
            params["vrf"] = vrf
        response = nb.ipam.prefixes.create(**params)
        print(f"{response} {prefix=}")


def main():
    """Main"""
    create__extras__tags()
    create__ipam__vrfs()
    tag = nb.extras.tags.get(name="TAG1")[0]["id"]
    vrfs = nb.ipam.vrfs.get(name=["VRF1", "VRF2"])
    vrfs.insert(0, {})

    pref_pattern = "10.3.{}.{}/{}"

    for vrf_d in vrfs:
        vrf = vrf_d["id"] if vrf_d else 0

        for idx3 in range(2 + 1):
            # prefix
            prefix = pref_pattern.format(idx3, 0, 23)
            _create_prefix(prefix, tag, vrf)
            prefix = pref_pattern.format(idx3, 0, 24)
            _create_prefix(prefix, tag, vrf)
            prefix = pref_pattern.format(idx3, 0, 31)
            _create_prefix(prefix, tag, vrf)
            prefix = pref_pattern.format(idx3, 0, 32)
            _create_prefix(prefix, tag, vrf)
            # address
            for idx4 in range(2 + 1):
                address = pref_pattern.format(idx3, idx4, 24)
                _create_address(address, tag, vrf)


if __name__ == "__main__":
    main()
