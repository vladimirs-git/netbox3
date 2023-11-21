netbox3
========


.. note::

   This project is under active development.


Overview
========


**netbox3** comprises t\ :strike:`h`\ ree Python tools designed for working with Netbox using the REST API.
Checked with Python >= 3.8, Netbox >= v3.6.

- :ref:`NbApi` Request data from Netbox using filter parameters identical to those in the web interface filter form.
- :ref:`NbForager` Join Netbox objects within itself, represent them as a multidimensional dictionary.
- :ref:`NbBranch` Extract the typed values from a Netbox object dictionary by using a chain of keys.


----------------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

    NbApi <api/nb_api.rst>
    NbForager <foragers/nb_forager.rst>
    NbBranch <branch/nb_branch.rst>

:ref:`Examples`


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

    # Create 2 addresses with different parameters
    response = nb.ip_addresses.create(address="1.2.3.4/24", tags=[1], status="active")
    print(response)  # <Response [201]>
    response = nb.ip_addresses.create(address="1.2.3.4/24", tags=[2], status="reserved")
    print(response)  # <Response [201]>

    # Get all addresses
    addresses = nb.ip_addresses.get()
    print(len(addresses))  # 181

    # Simple filter
    addresses = nb.ip_addresses.get(vrf="null")
    print(len(addresses))  # 30
    addresses = nb.ip_addresses.get(tag=["alpha", "bravo"])
    print(len(addresses))  # 4

    # Complex filter.
    # Get addresses that do not have VRF and
    # (have either the tag "alpha" or "bravo") and
    # (have a status of either active or reserved).
    addresses = nb.ip_addresses.get(vrf="null",
                                    tag=["alpha", "bravo"],
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


More examples in https://github.com/vladimirs-git/netbox3/tree/main/examples


----------------------------------------------------------------------------------------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

