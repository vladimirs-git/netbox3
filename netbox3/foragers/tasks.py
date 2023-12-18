"""Task"""
import json
import time
from queue import Queue
from threading import Thread
from typing import List, Tuple, Any, Dict

from pydantic import BaseModel, Field
from requests import Response

from netbox3 import helpers as h
from netbox3.nb_tree import NbTree
from netbox3.types_ import DAny, ULDAny, LDAny, DiDAny


# TODO  test
class Task(BaseModel):
    """Task to request Netbox API with parameters."""

    method: str = Field(description="Method name")
    url: str = Field(description="URL to Netbox objects")
    params: DAny = Field(default={}, description="Parameters to request Netbox object")
    data: DAny = Field(default={}, description="Data to update Netbox object")
    results: LDAny = Field(default=[], description="Result of requested Netbox objects")
    response: Any = Field(default=None, description="Result of completed task")


LTask = List[Task]

DTask = Dict[str, LTask]
LTLTask = List[Tuple[str, LTask]]


class TasksF:
    """TaskF."""

    def __init__(self, forager):
        """Init TaskF."""
        self.forager = forager
        self.tasks: LTask = []

    # ============================= property =============================

    @property
    def url(self) -> str:
        return str(getattr(getattr(self.forager, "connector"), "url"))

    @property
    def threads(self) -> int:
        return int(getattr(self.forager, "threads"))

    @property
    def interval(self) -> int:
        return int(getattr(self.forager, "interval"))

    # ============================= methods ==============================
    def get(self, **kwargs) -> None:
        task = Task(method="get", url=self.url, params=kwargs)
        self.tasks.append(task)

    def update(self, data: ULDAny) -> None:
        """Create Task to update data in Netbox."""
        if isinstance(data, dict):
            data = [data]
        items: LDAny = list(data)
        for data in items:
            task = Task(method="update", url=self.url, data=data)
            self.tasks.append(task)

    def request(self, tasks: LTask):
        if not tasks:
            return
        if self.threads > 1:
            self._run_tasks(tasks)
        else:
            for task in tasks:
                self._run_task(task)
        self._save(tasks)

    def _save(self, tasks: LTask) -> None:
        """Save Netbox objects to NbForager.root.

        :param tasks: Tasks with objects to save.
        """
        for task in tasks:
            if task.method != "get":
                if not isinstance(task.response, Response):
                    continue
                if not task.response.ok:
                    continue
            for data in task.results:
                app, model, digit = h.split_url(data["url"])
                path = f"{app}/{model}"
                model_d: DiDAny = self._get_root_data(path)
                model_d[int(digit)] = data

    def _get_root_data(self, path: str) -> DiDAny:
        """Get data in self root by app/model path.

        :param path: The app/model path.

        :return: The model data.
        """
        app, model = h.path_to_attrs(path)
        data = getattr(getattr(getattr(self.forager, "root"), app), model)
        return data

    def _run_tasks(self, tasks: LTask) -> None:
        """Threading mode, send request to Netbox, save result in Task object."""
        queue: Queue = Queue()
        for task in tasks:
            queue.put(task)

        for idx in range(self.threads):
            if self.interval:
                time.sleep(self.interval)
            thread = Thread(name=f"Thread-{idx}", target=self._run_tasks_queue, args=(queue,))
            thread.start()
        queue.join()

    # noinspection PyProtectedMember
    def _run_tasks_queue(self, queue: Queue) -> None:
        """Run tasks in threaded mode.

        This method dequeues and executes tasks until the queue is empty.
        :param queue: A queue containing app/model, method and data to be requested.
        """
        while not queue.empty():
            task: Task = queue.get()
            self._run_task(task)
            queue.task_done()

    def _run_task(self, task: Task) -> None:
        """Send request to Netbox, save result to Task object."""
        method = task.method
        params = task.params
        data = task.data
        path = h.url_to_path(task.url)
        connector = self._get_connector(path)

        # get
        if method == "get":
            # results
            results = getattr(connector, method)(**params)
            if not isinstance(results, list):
                results = [results]
            task.results = list(results)
            return

        # create, update, delete
        # response
        response = getattr(connector, method)(**data)
        if not isinstance(response, Response):
            raise TypeError(f"{response=}, {Response} expected.")
        task.response = response

        # results
        html: str = response.content.decode("utf-8")
        data: DAny = dict(json.loads(html))
        task.results = [data]

    def _get_connector(self, path: str):
        app, model = h.path_to_attrs(path)
        connector = getattr(getattr(getattr(self.forager, "api"), app), model)
        return connector


# TODO  test
class Tasks:
    """Tasks."""

    def __init__(self, nbf):
        """Init TaskHandler."""
        self.nbf = nbf  # NbForager
        self.tree = NbTree()

    def clear(self) -> None:
        """Clear all Tasks."""
        for app in self.tree.apps():
            for model in getattr(self.tree, app).models():
                tasks: TasksF = getattr(getattr(getattr(self.nbf, app), model), "tasks")
                tasks.tasks.clear()

    def run(self) -> list:
        tasks_d: DTask = self._init_tasks_d()
        self._request(tasks_d)
        responses = self.get_responses()
        self.clear()
        return responses

    def get_responses(self) -> list:
        responses = []
        for app in self.tree.apps():
            for model in getattr(self.tree, app).models():
                tasks: TasksF = getattr(getattr(getattr(self.nbf, app), model), "tasks")
                for task in tasks.tasks:
                    responses.append(task.response)
        return responses

    def _init_tasks_d(self) -> DTask:
        tasks_d: DTask = {
            "get": [],
            "create": [],
            "update": [],
            "delete": [],
        }
        for app in self.tree.apps():
            for model in getattr(self.tree, app).models():
                tasks: TasksF = getattr(getattr(getattr(self.nbf, app), model), "tasks")
                for task in tasks.tasks:
                    tasks_d[task.method].append(task)
        return tasks_d

    def _request(self, tasks_d: DTask) -> None:
        """Request Tasks"""
        forager = self.nbf.circuits.circuit_terminations
        for method, tasks in tasks_d.items():
            if not tasks:
                continue
            if method == "get":
                forager.tasks.request(tasks)
            else:
                forager.tasks.request(tasks)
