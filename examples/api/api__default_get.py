"""Example of how to set default get parameters."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
nb = NbApi(host=HOST, token=TOKEN)

# Problem demonstration
# Assume you are working with ip-addresses that have similar filters in each request.
# In each request you need use long list of parameters
objects1 = nb.ipam.ip_addresses.get(q="10.200.0.", family=4, status="active", vrf="null")
objects2 = nb.ipam.ip_addresses.get(q="10.200.1.", family=4, status="active", vrf="null")
objects3 = nb.ipam.prefixes.get(prefix="10.200.0.0/24", family=4, status="active", vrf="null")
objects4 = nb.ipam.prefixes.get(prefix="10.200.0.0/24", family=4, status="reserved", vrf="null")
# "GET /api/ipam/ip-addresses/?q=10.200.0.&family=4&status=active&vrf=null&limit=1000&offset=0"
# "GET /api/ipam/ip-addresses/?q=10.200.1.&family=4&status=active&vrf=null&limit=1000&offset=0"
# "GET /api/ipam/prefixes/?family=4&status=active&vrf=null&prefix=10.200.0.0%2F24&limit=1000&offset=0"
# "GET /api/ipam/prefixes/?family=4&status=reserved&vrf=null&prefix=10.200.0.0%2F24&limit=1000&offset=0"


# To reduce the number of similar parameters, you can use the default_get setting.
# If the parameter is not specified it wll be applied to the request.
default_get = {
    "ipam/ip-addresses/": {"family": 4, "status": "active", "vrf": "null"},
    "ipam/prefixes/": {"family": 4, "status": "active", "vrf": "null"},
}
nb = NbApi(host=HOST, token=TOKEN, default_get=default_get)
objects1 = nb.ipam.ip_addresses.get(q="10.200.0.")
objects2 = nb.ipam.ip_addresses.get(q="10.200.1.")
objects3 = nb.ipam.prefixes.get(prefix="10.200.0.0/24")
objects4 = nb.ipam.prefixes.get(prefix="10.200.0.0/24", status="reserved")
# "GET /api/ipam/ip-addresses/?q=10.200.0.&family=4&status=active&vrf=null&limit=1000&offset=0"
# "GET /api/ipam/ip-addresses/?q=10.200.1.&family=4&status=active&vrf=null&limit=1000&offset=0"
# "GET /api/ipam/prefixes/?family=4&status=active&vrf=null&prefix=10.200.0.0%2F24&limit=1000&offset=0"
# "GET /api/ipam/prefixes/?family=4&status=reserved&vrf=null&prefix=10.200.0.0%2F24&limit=1000&offset=0"
