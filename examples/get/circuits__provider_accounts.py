"""Examples NbApi.circuits.provider_accounts.get()."""
import logging

from netbox3 import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.provider_accounts.get()

# WEB UI Filter parameters
objects = nb.circuits.provider_accounts.get(q=["PROVIDER ACCOUNT"])
objects = nb.circuits.provider_accounts.get(tag="tag1")
objects = nb.circuits.provider_accounts.get(or_tag=["tag1", "tag2"])

# Attributes
objects = nb.circuits.provider_accounts.get(provider=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.provider_accounts.get(provider_id=[1, 2])
objects = nb.circuits.provider_accounts.get(account=[1, 2])

# Data Filter parameters
objects = nb.circuits.provider_accounts.get(id=[1, 2])
objects = nb.circuits.provider_accounts.get(name=["PROVIDER ACCOUNT1", "PROVIDER ACCOUNT2"])
objects = nb.circuits.provider_accounts.get(description=["DESCRIPTION1", "DESCRIPTION2"])
