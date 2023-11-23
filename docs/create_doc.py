"""Create documentation sections."""
import logging
from pathlib import Path

from pydantic import BaseModel, Field

from netbox3.api import APPS
from netbox3.nb_forager import NbForager
from netbox3.types_ import DAny, LStr

NBF = NbForager(host="netbox")


class Methods(BaseModel):
    """Names of application, model, methods."""

    app: str = Field(description="Application name")
    connector: str = Field(description="Connector class name")
    forager: str = Field(description="Forager class name")
    model: str = Field(description="Model name")
    path: str = Field(description="Model path")
    c_methods: LStr = Field(description="Connector method names")
    f_methods: LStr = Field(description="Forager method names")


def create_connectors() -> None:
    """Create api/{class_name}.rst files for connectors."""
    data: DAny = _get_app_models()
    for app, model_lo in data.items():
        connector = model_lo[0].connector
        header = f"{app.capitalize()} connectors"
        underline = "=" * len(header)
        lines = [header, underline, ""]
        for model_o in model_lo:
            path_ = f"**{model_o.path}**"
            pattern = ".. py:function:: NbApi.{}.{}.{}"
            c_methods = [pattern.format(app, model_o.model, s) for s in model_o.c_methods]
            lines.extend([path_, "", *c_methods, "", ""])

        text = "\n".join(lines)
        path = Path("api", f"{connector}.rst")
        path.write_text(text)
        logging.info("created %s", path)


def create_foragers() -> None:
    """Create foragers/{class_name}.rst files for foragers."""
    data: DAny = _get_app_models()
    data = {k: v for k, v in data.items() if k in dir(NBF)}
    for app, model_lo in data.items():
        forager = model_lo[0].forager
        header = f"{app.capitalize()} forager"
        underline = "=" * len(header)
        lines = [header, underline, ""]
        for model_o in model_lo:
            path_ = f"**{model_o.path}**"
            pattern = ".. py:function:: NbForager.{}.{}.{}"
            f_methods = [pattern.format(app, model_o.model, s) for s in model_o.f_methods]
            lines.extend([path_, "", *f_methods, "", ""])

        text = "\n".join(lines)
        path = Path("foragers", f"{forager}.rst")
        path.write_text(text)
        logging.info("created %s", path)


def _get_app_models() -> DAny:
    """Get names of application, model, method from NbApi."""
    data = {}
    for app in APPS:
        app_o = getattr(NBF.api, app)
        models = [s for s in dir(app_o) if s[0].islower()]

        for model in models:
            c_methods: LStr = []  # connector methods
            connector_o = getattr(app_o, model)
            attrs = [s for s in dir(connector_o) if s[0].islower()]
            for method in attrs:
                if not callable(getattr(connector_o, method)):
                    continue
                param = "(**data)"
                if method == "delete":
                    param = "(id)"
                elif method == "get":
                    param = "(**params)"
                c_methods.append(f"{method}{param}")

            f_methods: LStr = []  # forager methods
            for method in ["get(**params)", "count()"]:
                if not hasattr(NBF, app):
                    continue
                if not hasattr(getattr(NBF, app), model):
                    continue
                f_methods.append(method)

            methods_o = Methods(
                app=app,
                model=model,
                path=app + "/" + "-".join(model.split("_")) + "/",
                connector=app_o.__class__.__name__,
                c_methods=c_methods,
                forager=app_o.__class__.__name__[:-1] + "F",
                f_methods=f_methods,
            )
            data.setdefault(app, []).append(methods_o)
    return data


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    create_connectors()
    create_foragers()
