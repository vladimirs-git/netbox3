netbox3
========

Philosophy
==========
I am deeply engaged with the Netbox API. I have authored tons of Python scripts, each
with a common purpose: retrieving objects from the Netbox database and joining them into
a cohesive structure that mirrors the database itself. Retrieving and joining, retrieving
and joining, with some additional processing. The primary goal of this project is to
simplify the complexities inherent in these retrieval and joining operations.

Viewed through the lens of Netbox3, the Netbox database resembles the root of a tree,
with its branches intricately intertwined. The Netbox REST API provides data in a
simplified form, akin to timber. A significant aspect of my scripts involves intertwining
data to mirror the root structure. Netbox3 is designed to assist me in cultivating
a data tree rooted in Netbox.


----------------------------------------------------------------------------------------

Overview
========

**netbox3** comprises three Python tools designed for working with
`Netbox`_ using the REST API. Checked with Python >= 3.8, Netbox >= v3.6.

- `NbApi`_ Request data from Netbox using filter parameters identical to those in the web interface filter form. Filter parameters using the ``OR`` operator.
- `NbForager`_ Join Netbox objects within itself, represent them as a multidimensional dictionary.
- `NbBranch`_ Extract the typed values from a Netbox object dictionary by using a chain of keys.

The full documented on `Read the Docs`_.


----------------------------------------------------------------------------------------

Quickstart
==========

Install the package from pypi.org

.. code:: bash

    pip install netbox3


or from github.com repository

.. code:: bash

    pip install git+https://github.com/vladimirs-git/netbox3


NbForager demonstration.
Join Netbox objects within self as a multidimensional dictionary.

.. code:: python

    from pprint import pprint

    from netbox3 import NbForager

    HOST = "demo.netbox.dev"
    TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
    nbf = NbForager(host=HOST, token=TOKEN)

    # Get only 3 devices and sites from Netbox.
    # Note that the site in the device only contains basic data and
    # does not include tags, region and other extended data.
    nbf.dcim.devices.get(max_limit=3)
    nbf.dcim.sites.get()
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


NbApi demonstration.
Create, get, update and delete ip-addresses.

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


----------------------------------------------------------------------------------------

.. _`Netbox`: https://github.com/netbox-community/netbox
.. _`Read the Docs`: https://netbox3.readthedocs.io/en/latest/
.. _`NbApi`: https://netbox3.readthedocs.io/en/latest/api/nb_api.html#nbapi
.. _`NbForager`: https://netbox3.readthedocs.io/en/latest/foragers/nb_forager.html#nbforager
.. _`NbBranch`: https://netbox3.readthedocs.io/en/latest/branch/nb_branch.html#nbbranch
