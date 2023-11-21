netbox3
========


.. note::

   This project is under active development.


Overview
========


**netbox3** comprises three Python tools designed
for working with `Netbox`_ using the REST API.
Checked with Python >= 3.8, Netbox >= v3.6.

- `NbApi`_ Request data from Netbox using filter parameters identical to those in the web interface filter form.
- `NbForager`_ Join Netbox objects within itself, represent them as a multidimensional dictionary.
- `NbBranch`_ Extract the typed values from a Netbox object dictionary by using a chain of keys.

The full documented on `Read the Docs`_.


----------------------------------------------------------------------------------------

Quickstart
==========

Install the package from pypi.org

.. code:: bash

    pip install netbox3


NbApi demonstration.
Create, get, update and delete ip-address.

.. code:: python

    HOST = "demo.netbox.dev"
    TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
    nb = NbApi(host=HOST, token=TOKEN)

    # Create 2 addresses with different methods (different outputs)
    response = nb.ip_addresses.create(address="1.2.3.4/24", tags=[1], status="active")
    print(response)  # <Response [201]>
    data = nb.ip_addresses.create_d(address="1.2.3.4/24", tags=[2], status="reserved")
    print(data)  # {'id': 183, 'display': '1.2.3.4/24', ...

    # Get all addresses
    addresses = nb.ip_addresses.get()
    print(len(addresses))  # 181

    # Get all ip-addresses in global routing
    addresses = nb.ip_addresses.get(vrf="null")
    print(len(addresses))  # 30

    # Get newly created ip-addresses by complex filter
    # Note, you can use parameters similarly to the ``OR`` operator.
    # Filter addresses in the global routing AND
    # (have either the tag "bravo" OR "charlie") AND
    # (have a status of either active OR reserved).
    addresses = nb.ip_addresses.get(or_q=["1.2.3", "4.5.6"],
                                    vrf="null",
                                    or_tag=["bravo", "charlie"],
                                    status=["active", "reserved"])
    print(len(addresses))  # 2

    addresses = nb.ip_addresses.get(address="1.2.3.4/24")
    for address in addresses:
        # Update
        id_ = address["id"]
        response = nb.ip_addresses.update(id=id_, description="text")
        print(response)  # <Response [200]>
        print(nb.ip_addresses.get(id=id_)[0]["description"])  # text

        # Delete
        response = nb.ip_addresses.delete(id=id_)
        print(response)  # <Response [204]>


NbForager demonstration.
Join Netbox objects within self as a multidimensional dictionary.

.. code:: python

    from pprint import pprint

    from netbox3 import NbForager

    HOST = "demo.netbox.dev"
    TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
    nbf = NbForager(host=HOST, token=TOKEN, max_limit=10)

    # Get all sites and only 3 devices from Netbox.
    # Note that the site in the device only contains basic data and
    # does not include tags, region and other extended data.
    nbf.dcim.sites.get()
    nbf.dcim.devices.get(max_limit=3)
    pprint(nbf.root.dcim.devices)
    # {88: {'id': 88,
    #       'name': 'PP:B117',
    #       'site': {'id': 21,
    #      ...

    # Join objects within self.
    # Note that the device now includes site region and all other data.
    tree = nbf.grow_tree()
    pprint(tree.dcim.devices)
    # {88: {'id': 88,
    #       'name': 'PP:B117',
    #       'site': {'id': 21,
    #                'region': {'id': 40,
    #                           'name': 'North Carolina',
    #                           'url': 'https://demo.netbox.dev/api/dcim/regions/40/',
    #      ...

    # You can access any site attribute through a device.
    print(tree.dcim.devices[88]["site"]["region"]["name"])  # North Carolina


NbForager demonstration.
Get data in threading mode.

.. code:: python

    import logging
    from datetime import datetime

    from netbox3 import NbApi

    # Enable logging DEBUG mode
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    HOST = "demo.netbox.dev"
    TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"

    # Get data in threading mode.
    start = datetime.now()
    nb = NbApi(host=HOST, token=TOKEN, threads=10, interval=0.1, limit=200)
    objects = nb.ip_addresses.get()
    seconds = (datetime.now() - start).seconds
    print([d["address"] for d in objects])
    print(f"{len(objects)=} {seconds=}")
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/?brief=1&limit=1 ...
    # DEBUG    Starting new HTTPS connection (2): demo.netbox.dev:443
    # DEBUG    Starting new HTTPS connection (3): demo.netbox.dev:443
    # DEBUG    Starting new HTTPS connection (4): demo.netbox.dev:443
    # DEBUG    Starting new HTTPS connection (5): demo.netbox.dev:443
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/addresses/? ...
    # len(objects)=4153 seconds=3


    # Get data in loop mode, to compare time performance.
    start = datetime.now()
    nb = NbApi(host=HOST, token=TOKEN)
    objects = nb.ip_addresses.get()
    seconds = (datetime.now() - start).seconds
    print(f"{len(objects)=} {seconds=}")
    # DEBUG    : Starting new HTTPS connection (1): demo.netbox.dev:443
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
    # DEBUG    https://demo.netbox.dev:443 "GET /api/ipam/prefixes/? ...
    # len(objects)=4153 seconds=7


----------------------------------------------------------------------------------------

.. _`Netbox`: https://github.com/netbox-community/netbox
.. _`Read the Docs`: https://netbox3.readthedocs.io/en/latest/
.. _`NbApi`: https://netbox3.readthedocs.io/en/latest/api/nb_api.html#nbapi
.. _`NbForager`: https://netbox3.readthedocs.io/en/latest/foragers/nb_forager.html#nbforager
.. _`NbBranch`: https://netbox3.readthedocs.io/en/latest/branch/nb_branch.html#nbbranch
