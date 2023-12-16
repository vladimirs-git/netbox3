
.. contents::


----------------------------------------------------------------------------------------

NbApi
=====

.. autoclass:: netbox3.NbApi
  :members:
  :exclude-members:
    default_active,
    host,
    url,


----------------------------------------------------------------------------------------

Connector methods
-----------------

.. autoclass:: netbox3.api.connector.Connector
  :members:
    create,
    create_d,
    delete,
    get,
    update,
    update_d,
  :class-doc-from: class


----------------------------------------------------------------------------------------

Connector ipam.ip_addresses.get()
---------------------------------

.. autoclass:: netbox3.api.ip_addresses.IpAddressesC.get
  :undoc-members:


----------------------------------------------------------------------------------------

Extended filtering parameters
-----------------------------
The mapped filtering parameters are identical to those in the web interface filter form and simplify
the searching in Netbox. How it works? NbApi need be initialized with ``extended_get=True``
(default).  When you are filtering by ``{parameter}``, the first step is for NbApi to request all
objects of the interested model, and then translate the interested ``{parameter}`` to
``{parameter}_id`` for the second request.

.. note::

    In case the model has a large number of objects, searching by the mapped parameter could be slow.

=================  ================================  ====================  ==============================  =======
NbApi                                                REST API
---------------------------------------------------  -------------------------------------------------------------
Parameter          Path                              Parameter             Path                            Key
=================  ================================  ====================  ==============================  =======
circuit            any                               circuit_id            circuits/circuits/              cid
provider           any                               provider_id           circuits/providers/             name
provider_account   any                               provider_account_id   circuits/provider-accounts/     name
device_type        any                               device_type_id        dcim/device-types/              model
location           any                               location_id           dcim/locations/                 name
manufacturer       any                               manufacturer_id       dcim/manufacturers/             name
platform           any                               platform_id           dcim/platforms/                 name
rack               any                               rack_id               dcim/racks/                     name
region             any                               region_id             dcim/regions/                   name
site               any                               site_id               dcim/sites/                     name
site_group         any                               site_group_id         dcim/site-groups/               name
content_type       any                               content_type_id       extras/content-types/           display
for_object_type    any                               for_object_type_id    extras/content-types/           display
export_target      any                               export_target_id      ipam/route-targets/             name
exporting_vrf      any                               exporting_vrf_id      ipam/vrfs/                      name
import_target      any                               import_target_id      ipam/route-targets/             name
importing_vrf      any                               importing_vrf_id      ipam/vrfs/                      name
present_in_vrf     any                               present_in_vrf_id     ipam/vrfs/                      name
rir                any                               rir_id                ipam/rirs/                      name
vrf                any                               vrf_id                ipam/vrfs/                      name
tenant             any                               tenant_id             tenancy/tenants/                name
tenant_group       any                               tenant_group_id       tenancy/tenant-groups/          name
bridge             any                               bridge_id             virtualization/interfaces/      name
group              dcim/sites/                       group_id              dcim/site-groups/               name
group              ipam/vlans/                       group_id              ipam/vlan-groups/               name
group              tenancy/tenants/                  group_id              tenancy/tenant-groups/          name
group              virtualization/clusters/          group_id              virtualization/cluster-groups/  name
parent             dcim/locations/                   parent_id             dcim/locations/                 name
parent             dcim/regions/                     parent_id             dcim/regions/                   name
parent             dcim/site-groups/                 parent_id             dcim/site-groups/               name
parent             tenancy/tenant-groups/            parent_id             tenancy/tenant-groups/          name
parent             virtualization/interfaces/        parent_id             virtualization/interfaces/      name
role               dcim/devices/                     role_id               dcim/device-roles/              name
role               dcim/racks/                       role_id               dcim/rack-roles/                name
role               ipam/                             role_id               ipam/roles/                     name
role               virtualization/virtual-machines/  role_id               dcim/device-roles/              name
type               circuits/circuits/                type_id               circuits/circuit-types/         name
=================  ================================  ====================  ==============================  =======


----------------------------------------------------------------------------------------

Filtering parameters in an OR manner
------------------------------------
Netbox REST API processes filtering parameters in different manners. They can be
processed using ``OR``, ``AND`` or ``loners``, where ``loners`` means only one parameter
can be processed (processing only the last in the list). Viewed through the lens of
Netbox3, ``loners`` is useless and could be processed using an ``OR`` operator.
If you meet the ``loners`` parameters, the Netbox API may return improperly filtered
objects `#14305`_. I have not checked all endpoints, so if you encounter this issue,
please let me know so that I can fix it in NbApi. As a workaround, you can use
``or_{parameter}`` in filtering parameters or set custom ``loners`` to change NbApi
default behavior.

======================  ================================================================
Path                    Parameter
======================  ================================================================
any                     q
ipam/aggregates         prefix
ipam/aggregates         within_include
extras/content-types    app_label, id, model
======================  ================================================================

`Example of how to change loners`_


----------------------------------------------------------------------------------------

.. _`Example of how to change loners`: https://github.com/vladimirs-git/netbox3/tree/main/demo/api/api__loners.py
.. _`#14305`: https://github.com/netbox-community/netbox/discussions/14305
.. _`Schema ip_addresses`: https://demo.netbox.dev/api/schema/swagger-ui/#/ipam/ipam_ip_addresses_list
.. _`Schema`: https://demo.netbox.dev/api/schema/swagger-ui