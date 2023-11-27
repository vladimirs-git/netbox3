"""Create a group of interfaces."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)


def create__ipam__ip_addresses():
    """Create /ipam/ip-addresses objects."""
    for idx1 in range(10 + 1):
        for idx2 in range(255 + 1):
            address = f"10.200.{idx1}.{idx2}/24"
            response = nb.ipam.ip_addresses.create(address=address)
            print(response, address)


if __name__ == "__main__":
    create__ipam__ip_addresses()
