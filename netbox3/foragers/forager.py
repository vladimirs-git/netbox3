# pylint: disable=R0801

"""Base for Foragers."""

from __future__ import annotations

import logging
import time
from queue import Queue
from threading import Thread
from urllib.parse import urlparse, parse_qs

from vhelpers import vstr

from netbox3 import helpers as h
from netbox3.nb_api import NbApi
from netbox3.nb_tree import NbTree, missed_urls
from netbox3.types_ import LDAny, DiDAny, LStr, DAny, LT2StrDAny


class Forager:
    """Forager methods for different models."""

    def __init__(self, forager_a):
        """Init Forager.

        :param forager_a: Parent forager.
        :type forager_a: CircuitsF or DcimF or IpamF or TenancyF
        """
        self.app = h.attr_name(forager_a)
        self.model = h.attr_name(self)
        self.api: NbApi = forager_a.api
        self.connector = getattr(getattr(self.api, self.app), self.model)
        # data
        self.root: NbTree = forager_a.root
        self.data: DiDAny = getattr(getattr(self.root, self.app), self.model)

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        params = vstr.repr_info(self.count())
        return f"<{name}: {params}>"

    # ============================= property =============================

    @property
    def interval(self) -> int:
        """Wait this time between requests (seconds)."""
        return self.connector.interval

    @property
    def threads(self) -> int:
        """Threads count."""
        return self.connector.threads

    # ============================= methods ==============================

    def count(self) -> int:
        """Count of the Netbox objects in the NbForager.root.{model}.

        :return: Count of the Netbox objects.

        :rtype: int
        """
        return len(self.data)

    def get(self, include_nested: bool = True, **kwargs) -> None:
        """Retrieve data from the Netbox.

        Request data based on the filter parameters (kwargs described in the
        NbApi connector) and save to the NbForager.root.

        :param include_nested: `True` - Request base and nested objects,
            `False` - Request only base objects. Default id `True`
        :type include_nested: bool

        :param kwargs: Filtering parameters.
        :type kwargs: dict

        :return: None. Update self object.
        """
        nb_objects: LDAny = self._get_root_data_from_netbox(**kwargs)
        if not include_nested:
            return
        urls = self._collect_nested_urls(nb_objects)

        # Query nested data from the Netbox
        # threads
        results: LDAny = []
        if self.threads > 1:
            path_params: LT2StrDAny = self._get_path_params(urls)
            self._clear_connector_results(path_params)
            self._query_threads(path_params)
            results_: LDAny = self._pop_connector_results(path_params)
            results.extend(results_)

        # loop
        else:
            for url in urls:
                app, model, _ = h.split_url(url)
                path = f"{app}/{model}/"
                params_d: DAny = parse_qs(urlparse(url).query)
                connector = self._get_connector(path)
                # noinspection PyProtectedMember
                results_ = connector._query_loop(path, params_d)  # pylint: disable=W0212
                results.extend(results_)

        self._save_results(results)

    # ============================= helpers ==============================

    def _get_root_data_from_netbox(self, **kwargs) -> LDAny:
        """Retrieve data from the Netbox.

        Request data based on the kwargs filter parameters and
        save the received objects to the NbForager.root.

        :param kwargs: Filter parameters.

        :return: List of Netbox objects. Update NbForager.root object.
        """
        nb_objects: LDAny = self.connector.get(**kwargs)
        nb_objects = self._validate_ids(nb_objects)
        for nb_object in nb_objects:
            self.data[nb_object["id"]] = nb_object
        return nb_objects

    @staticmethod
    def _validate_ids(nb_objects: LDAny) -> LDAny:
        """Check the IDs in the items. The ID should be a unique integer.

        :param nb_objects: List of dictionaries containing Netbox objects.

        :return: None. Logging an error if the ID does not match the conditions.
        """
        nb_objects_: LDAny = []
        for nb_object in nb_objects:
            id_ = nb_object.get("id")
            if not isinstance(id_, int):
                msg = f"TypeError: {id_=} {int} expected in {nb_object=}."
                logging.error(msg)
                continue
            if id_ in nb_objects:
                msg = f"ValueError: Duplicate {id_=} in nb_objects_ and {nb_object=}."
                logging.error(msg)
                continue
            nb_objects_.append(nb_object)
        return nb_objects_

    def _collect_nested_urls(self, nb_objects: LDAny) -> LStr:
        """Collect nested urls.

        :param nb_objects: List of Netbox objects.

        :return: Nested URLs.
        """
        urls: LStr = h.nested_urls(nb_objects)
        urls = missed_urls(urls=urls, tree=self.root)
        urls = h.join_urls(urls)
        urls = [s for s in urls if h.split_url(s)[0]]
        return urls

    # noinspection PyProtectedMember
    def _get_path_params(self, urls: LStr) -> LT2StrDAny:
        """Get path of app/model and parameters based on the list of URLs.

        :param urls: A list of URLs.

        :return: A list of tuples containing the path and parameters.
        """
        path_params: LT2StrDAny = []
        for url in urls:
            app, model, _ = h.split_url(url)
            path = f"{app}/{model}/"
            connector = self._get_connector(path)
            params_d = parse_qs(urlparse(url).query)
            params_ld: LDAny = h.slice_params_ld(
                url=connector.url,
                max_len=connector.url_length,
                keys=connector._slices,  # pylint: disable=W0212
                params=[params_d],
            )
            for params_d in params_ld:
                path_params.append((path, params_d))
        return path_params

    # noinspection PyProtectedMember
    def _clear_connector_results(self, path_params: LT2StrDAny) -> None:
        """Clear results in connectors by path app/model."""
        for path, _ in path_params:
            connector = self._get_connector(path)
            connector._results.clear()  # pylint: disable=W0212

    def _query_threads(self, path_params: LT2StrDAny) -> None:
        """Retrieve data from Netbox in threaded mode.

        :param path_params: A list of tuples containing the path app/model and parameters.

        :return: None. Save results to self._results.
        """
        queue: Queue = Queue()
        for path, params_d in path_params:
            queue.put((path, params_d))

        for idx in range(self.threads):
            if self.interval:
                time.sleep(self.interval)
            thread = Thread(name=f"Thread-{idx}", target=self._run_queue, args=(queue,))
            thread.start()
        queue.join()

    # noinspection PyProtectedMember
    def _run_queue(self, queue: Queue) -> None:
        """Process tasks from the queue.

        This method dequeues and executes tasks until the queue is empty.
        Each task is expected to be a callable method with its corresponding params_d parameters.
        :param queue: A queue containing path app/model and parameters pairs to be requested.

        :return: None. Update connector._results list.
        """
        while not queue.empty():
            path, params_d = queue.get()
            connector = self._get_connector(path)
            connector._query_data_thread(path=path, params_d=params_d)  # pylint: disable=W0212
            queue.task_done()

    # noinspection PyProtectedMember
    def _pop_connector_results(self, path_params: LT2StrDAny) -> LDAny:
        """Get results from connectors by path app/model and delete cached results."""
        results: LDAny = []
        for path, _ in path_params:
            connector = self._get_connector(path)
            results.extend(connector._results)  # pylint: disable=W0212
            connector._results.clear()  # pylint: disable=W0212
        return results

    def _get_connector(self, path: str):
        """Get connector by app/model path.

        :param path: The app/model path.

        :return: The connector object.

        :rtype:  DeviceRolesC or DeviceTypesC or LocationsC or RacksC or etc.
        """
        app, model = h.path_to_attrs(path)
        connector = getattr(getattr(self.api, app), model)
        return connector

    def _save_results(self, results):
        # save
        for data in results:
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
        data = getattr(getattr(self.root, app), model)
        return data
