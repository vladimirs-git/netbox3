"""Task"""
from typing import List, Tuple

from pydantic import BaseModel, Field

from netbox3.types_ import DList


# TODO  test
class Task(BaseModel):
    """Task to request Netbox API with parameters."""

    url: str = Field(description="URL to Netbox objects")
    # app: str = Field(description="Application name")  # TODO delete if not used
    # model: str = Field(description="Model name")
    method: str = Field(description="Method name")
    params_d: DList = Field(description="Parameters")


LTask = List[Task]
LTLTask = List[Tuple[str, LTask]]


# TODO  test
class Tasks(BaseModel):
    """Tasks by method."""
    delete: LTask = Field(default=[], description="Tasks to delete objects")
    create: LTask = Field(default=[], description="Tasks to create objects")
    update: LTask = Field(default=[], description="Tasks to update objects")
    get: LTask = Field(default=[], description="Tasks to get objects")

    def method_tasks(self) -> LTLTask:
        """Return the tasks in the correct order to run them."""
        return [
            ("delete", self.delete),
            ("create", self.create),
            ("update", self.update),
            ("get", self.get),
        ]
