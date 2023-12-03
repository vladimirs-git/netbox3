netbox3
=======


Philosophy
==========
**netbox3** is designed to help in creating Netbox data as a multidimensional
dictionary and representing data similarly to the WEB UI.

I have made many Python scripts, each with a common goal:
getting objects from the Netbox database and assembling them together
in a structure that looks like the database itself. Getting and assembling,
getting and assembling, with some additional steps. The main aim of this project is to
make these getting and assembling tasks simpler.

The Netbox database is like the root of a tree, with its branches all intertwined.
The REST API provides data in a simplified form, akin to timber.
NbForager is requesting root data from Netbox using NbApi and intertwining it into
NbForager.tree data to align with the structure of the WEB UI.


----------------------------------------------------------------------------------------

Overview
========

**netbox3** comprises t\ :strike:`h`\ ree Python tools designed for working with
`Netbox`_ using the REST API. Checked with Python >= 3.8, Netbox >= v3.6.

- :ref:`NbApi` Request data from Netbox using filter parameters identical to those in the web interface filter form. Filter parameters using the ``OR`` operator.
- :ref:`NbForager` Assemble Netbox objects within itself, represent them as a multidimensional dictionary.
- :ref:`NbBranch` Extract the typed values from a Netbox object dictionary by using a chain of keys.

This project on `GitHub`_.


----------------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

    NbApi <api/nb_api.rst>
    NbForager <foragers/nb_forager.rst>
    NbBranch <branch/nb_branch.rst>
    NbValue <branch/nb_value.rst>
    Examples <examples.rst>


----------------------------------------------------------------------------------------

Quickstart
==========

Install the package from pypi.org

.. code:: bash

    pip install netbox3

or from github.com repository

.. code:: bash

    pip install git+https://github.com/vladimirs-git/netbox3


:py:class:`.NbForager` demonstration.
Assemble Netbox objects within self as a multidimensional dictionary.

Request the main object. All nested objects also are requested.
Assemble multidimensional dictionary.

.. code:: python

    from pprint import pprint

    from netbox3 import NbForager

    HOST = "demo.netbox.dev"
    TOKEN = "1234567890123456789012345678901234567890"
    nbf = NbForager(host=HOST, token=TOKEN, threads=10)

    # Request devices with all nested object: device-roles, tenants, tags, etc.
    nbf.dcim.devices.get(nested=True)
    print(f"{len(nbf.root.dcim.devices)=}")
    print(f"{len(nbf.root.dcim.device_roles)=}")
    print(f"{len(nbf.root.tenancy.tenants)=}")
    print(f"{len(nbf.root.extras.tags)=}")
    # len(nbf.root.dcim.devices)=78
    # len(nbf.root.dcim.device_roles)=10
    # len(nbf.root.tenancy.tenants)=5
    # len(nbf.root.extras.tags)=2


    # Assemble objects within self as multidimensional dictionary.
    tree = nbf.grow_tree()
    pprint(list(tree.dcim.devices.values())[0])
    # {"id": 1,
    #  "name": "dmi01-akron-rtr01",
    #  "rack": {"id": 1,
    #           "site": {"id": 2,
    #                    "tenant": {"id": 5,
    #                               "group": {"id": 1,
    #                                         "name": "Customers",
    #                                         ...
    #           "tenant": {"id": 5,
    #                      "group": {"id": 1,
    #                                "name": "Customers",
    #                                ...
    # ...

Request objects using filtering parameters. Assemble multidimensional dictionary.

.. code:: python

    from pprint import pprint

    from netbox3 import NbForager, NbBranch

    HOST = "demo.netbox.dev"
    TOKEN = "1234567890123456789012345678901234567890"
    nbf = NbForager(host=HOST, token=TOKEN)

    # Request specific devices and all sites from Netbox.
    # Note that the site in the device only contains basic data and
    # does not include tags, region and other extended data.
    nbf.dcim.devices.get(q="PP:B")
    nbf.dcim.sites.get()
    device = nbf.root.dcim.devices[88]
    pprint(device)
    # {"id": 88,
    #  "name": "PP:B117",
    #  "site": {"display": "MDF",
    #           "id": 21,
    #           "name": "MDF",
    #           "slug": "ncsu-065",
    #           "url": "https://demo.netbox.dev/api/dcim/sites/21/"},
    #  ...

    # Assemble objects within self as multidimensional dictionary.
    # Note that the device now includes site region and all other data.
    tree = nbf.grow_tree()
    device = tree.dcim.devices[88]
    pprint(device)
    # {"id": 88,
    #  "name": "PP:B117",
    #  "site": {"display": "MDF",
    #           "id": 21,
    #           "name": "MDF",
    #           "slug": "ncsu-065",
    #           "url": "https://demo.netbox.dev/api/dcim/sites/21/"
    #           "region": {"_depth": 2,
    #                      "display": "North Carolina",
    #                      "id": 40,
    #                      "name": "North Carolina",
    #                      "slug": "us-nc",
    #                      "url": "https://demo.netbox.dev/api/dcim/regions/40/"},
    #           "tenant": {"display": "NC State University",
    #                      "id": 13,
    #                      "name": "NC State University",
    #                      "slug": "nc-state",
    #                      "url": "https://demo.netbox.dev/api/tenancy/tenants/13/"},
    #           ...
    # ...

    # Access site attribute through a device.
    region = device["site"]["region"]["name"]
    print(f"{region=}")  # region="North Carolina"

    # Use NbBranch to ensure the data type if any dictionary in the chain is missing.
    region = NbBranch(device).str("site", "region", "name")
    print(f"{region=}")  # region="North Carolina"


:py:class:`.NbApi` demonstration.
Create, get, update and delete ip-addresses.

.. code:: python

    from netbox3 import NbApi

    HOST = "demo.netbox.dev"
    TOKEN = "1234567890123456789012345678901234567890"
    nb = NbApi(host=HOST, token=TOKEN)

    # Create 2 addresses with different methods (different outputs)
    response = nb.ipam.ip_addresses.create(address="1.2.3.4/24", tags=[2], status="active")
    print(response)  # <Response [201]>
    data = nb.ipam.ip_addresses.create_d(address="1.2.3.4/24", tags=[3], status="reserved")
    print(data)  # {"id": 183, "display": "1.2.3.4/24", ...

    # Get all addresses
    addresses = nb.ipam.ip_addresses.get()
    print(len(addresses))  # 181

    # Get all ip-addresses in global routing
    addresses = nb.ipam.ip_addresses.get(vrf="null")
    print(len(addresses))  # 30

    # Get newly created ip-addresses by complex filter
    # Note, you can use parameters similarly to the ``OR`` operator.
    # Filter addresses in the global routing AND
    # (have either the tag "bravo" OR "charlie") AND
    # (have a status of either active OR reserved).
    addresses = nb.ipam.ip_addresses.get(or_q=["1.2.3", "4.5.6"],
                                         vrf="null",
                                         or_tag=["bravo", "charlie"],
                                         status=["active", "reserved"])
    print(len(addresses))  # 2

    addresses = nb.ipam.ip_addresses.get(address="1.2.3.4/24")
    for address in addresses:
        # Update
        id_ = address["id"]
        response = nb.ipam.ip_addresses.update(id=id_, description="text")
        print(response)  # <Response [200]>
        print(nb.ipam.ip_addresses.get(id=id_)[0]["description"])  # text

        # Delete
        response = nb.ipam.ip_addresses.delete(id=id_)
        print(response)  # <Response [204]>


----------------------------------------------------------------------------------------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


----------------------------------------------------------------------------------------

.. _`Netbox`: https://github.com/netbox-community/netbox
.. _`GitHub`: https://github.com/vladimirs-git/netbox3
