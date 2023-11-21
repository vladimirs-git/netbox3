"""Get all objects from the Netbox."""
import logging
from datetime import datetime

from netbox3 import NbApi
from netbox3.api import APPS
from netbox3.types_ import LStr

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1a8424035853e078f9a65e06de9247249d26d5a1"
api = NbApi(host=HOST, token=TOKEN)

start = datetime.now()
status = api.status.get()
logging.info("version=%s", status["netbox-version"])

for apps in APPS:
    app_o = getattr(api, apps)
    models: LStr = [s for s in dir(app_o) if s[0].islower()]
    for model in models:
        model_o = getattr(app_o, model)
        objects = model_o.get()
        msg = f"{apps} {model} {len(objects)}\n"
        logging.info(msg)

seconds = (datetime.now() - start).seconds
print(f"{seconds=}")
