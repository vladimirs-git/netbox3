NbForager diagram
=================
A diagram that helps to understand how to work with this tool is provided.
Your script can retrieve Netbox objects using the NbApi.
For extracting dictionary values, you can utilize NbBranch.
For data caching, NbHandle and NbData can be used.

.. code:: text

    ╔═════════════════════════════════════════════════╗
    ║                  External script                ║  Your script
    ╚═╤═══════════╤════════════════╤════════════╤═════╝
      │           │                │            │
      │  ╔════════V═════════╗ ╔════V═════╗ ╔════V═════╗
      │  ║     NbForager    ╠═╣  NbData  ║ ║ NbBranch ║  Gathers and cache Netbox objects
      │  ╚════════╦═════════╝ ╚══════════╝ ╚══════════╝
    ╔═V═══════════╩═════════╗
    ║           NbApi       ║                            Filter Netbox data form DB
    ╚═════════════╤═════════╝
                  │
    ╔═════════════V═════════╗
    ║    Netbox REST API    ║                            Netbox DB
    ╚═══════════════════════╝

