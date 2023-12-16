"""Demo NbApi.extras.custom_fields.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.extras.custom_fields.get()

# WEB UI Filter parameters
objects = nb.extras.custom_fields.get(q=["cf1", "cf2"])

# Attributes
objects = nb.extras.custom_fields.get(type=["integer", "decimal"])
objects = nb.extras.custom_fields.get(content_type_id=[20, 69])
objects = nb.extras.custom_fields.get(group_name=["group1", "group2"])
objects = nb.extras.custom_fields.get(weight=[101, 102])
objects = nb.extras.custom_fields.get(required=True)
objects = nb.extras.custom_fields.get(choice_set=["cs1", "cs2"])
objects = nb.extras.custom_fields.get(choice_set_id=[1, 2])
objects = nb.extras.custom_fields.get(ui_visibility=["read-only", "read-write"])
objects = nb.extras.custom_fields.get(is_cloneable=True)

# Data Filter parameters
objects = nb.extras.custom_fields.get(id=[1, 2])
objects = nb.extras.custom_fields.get(name=["custom_field_a", "custom_field_b"])
