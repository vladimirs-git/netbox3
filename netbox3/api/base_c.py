# pylint: disable=R0902,R0903

"""Connector Base."""

from __future__ import annotations

import json
import logging
import re
import time
import urllib
from operator import itemgetter
from queue import Queue
from threading import Thread
from typing import Callable
from urllib.parse import urlencode, ParseResult

import requests
from requests import Session, Response
from requests.exceptions import ReadTimeout, ConnectionError as RequestsConnectionError
from vhelpers import vdict, vlist, vparam

from netbox3 import helpers as h
from netbox3.api import param_path
from netbox3.api.param_path import ParamPath, DParamPath
from netbox3.exceptions import NbApiError
from netbox3.types_ import DAny, DStr, LDAny, LStr, DLInt, DList, LDList, DLStr, DDAny, DSStr
from netbox3.types_ import TLists, OUParam, LParam


class BaseC:
    """Connector Base."""

    path = ""
    _slices = [
        "id",
        "name",
        "slug",
        "display",
        "prefix",
        "address",
        "cid",
        "vid",
        "asn",
    ]
    _init_params = [
        "host",
        "token",
        "scheme",
        "port",
        "verify",
        "limit",
        "url_length",
        "threads",
        "interval",
        "timeout",
        "max_retries",
        "sleep",
        "default_get",
        "loners",
    ]
    _reserved_keys: DSStr = {
        "ipam/": {
            # evonetbox
            "overlapped",
            "warnings",
            "nbnets",
            "nbnets__subnets",
            # NbForager
            "ipv4",
            "aggregate",
            "super_prefix",
            "sub_prefixes",
            "ip_addresses",
        }
    }

    def __init__(self, **kwargs):
        """Init BaseC.

        :param str host: Netbox host name.

        :param str token: Netbox token.

        :param str scheme: Access method: `https` or `http`. Default is `https`.

        :param int port: ``Not implemented`` TCP port. Default is `443`.

        :param bool verify: Transport Layer Security.
            `True` - A TLS certificate required,
            `False` - Requests will accept any TLS certificate.
            Default is `True`.

        :param int limit: Split the query to multiple requests
            if the count of objects exceeds this value. Default is `1000`.

        :param int url_length: Split the query to multiple requests
            if the URL length exceeds maximum length due to a long list of
            GET parameters. Default is `2047`.

        :param int threads: Threads count. <=1 is loop mode, >=2 is threading mode.
            Default id `1`.

        :param float interval: Wait this time between the threading requests (seconds).
            Default is `0`. Useful to optimize session spikes and achieve
            script stability in Docker with limited resources.

        :param int timeout: Session timeout (seconds). Default is `60`.

        :param int max_retries: Retries the request multiple times if the Netbox API
            does not respond or responds with a timeout. Default is `0`.

        :param int sleep: Interval (seconds) before the next retry after
            session timeout reached. Default is `10`.

        :param dict default_get: Set default filtering parameters.

        :param dict loners: Set :ref:`Filtering parameters in an OR manner`.
        """
        self.host: str = _init_host(**kwargs)
        self.token: str = str(kwargs.get("token") or "")
        self.scheme: str = _init_scheme(**kwargs)
        self.port: int = int(kwargs.get("port") or 0)
        self.verify: bool = _init_verify(**kwargs)
        self.limit: int = int(kwargs.get("limit") or 1000)
        self.url_length = int(kwargs.get("url_length") or 2047)
        # Multithreading
        self.threads: int = _init_threads(**kwargs)
        self.interval: float = float(kwargs.get("interval") or 0.0)
        # Errors processing
        self.timeout: float = float(kwargs.get("timeout") or 60)
        self.max_retries: int = int(kwargs.get("max_retries") or 0)
        self.sleep: float = float(kwargs.get("sleep") or 10)
        # Settings
        self.default_get: DDAny = dict(kwargs.get("default_get") or {})
        self.loners: DLStr = dict(kwargs.get("loners") or {})

        self._default_get: DList = self._init_default_get()
        self._loners: LStr = self._init_loners()
        self._results: LDAny = []  # cache for received objects from Netbox
        self._session: Session = requests.session()

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.host}>"

    # ============================= property =============================

    @property
    def url(self) -> str:
        """Base URL with the application and model path."""
        return f"{self.url_base}{self.path}"

    @property
    def url_base(self) -> str:
        """Base URL without the application and model path."""
        return f"{self.scheme}://{self.host}/api/"

    # ============================== query ===============================

    def _query(self, path: str, params: OUParam = None) -> LDAny:
        """Retrieve data from the Netbox.

        :param path: Section of the URL that points to the model.
        :param params: Parameters to request from the Netbox.

        :return: A list of the Netbox objects.

        :example:
            query(path="ipam/ip-addresses/", params=[("status", "active")]) ->
            [{"id": 1, "address": "", ...}, ...]
        """
        if params is None:
            params = []
        params_d = vparam.to_dict(params)
        return self._query_loop(path, params_d)

    def _query_params_ld(self, params_ld: LDList) -> LDAny:
        """Retrieve data from the Netbox.

        :param params_ld: Parameters to request from the Netbox.

        :return: A list of the Netbox objects.
        """
        self._results = []

        # slice params
        params_ld = h.slice_params_ld(
            url=self.url,
            max_len=self.url_length,
            keys=self._slices,
            params_ld=params_ld,
        )

        # threads
        if self.threads > 1:
            counts_w_params: LDAny = self._query_pages_count(params_ld)
            params_ld_: LDAny = self._slice_params_counters(counts_w_params)
            self._query_threads(method=self._query_data_thread, params_ld=params_ld_)
        # loop
        else:
            for params_d in params_ld:
                results_: LDAny = self._query_loop(self.path, params_d)
                self._results.extend(results_)

        # save
        results: LDAny = sorted(self._results, key=itemgetter("id"))
        results = vlist.no_dupl(results)
        self._results = []
        return results

    def _query_count(self, path: str, params_d: DAny) -> None:
        """Retrieve counters of interested objects from the Netbox.

        :param path: Section of the URL that points to the model.
        :param params_d: Parameters to request from the Netbox.

        :return: None. Update self object.
        """
        params_d_ = params_d.copy()
        params_d_["brief"] = 1
        params_d_["limit"] = 1
        params_l: LParam = vparam.from_dict(params_d_)
        url = f"{self.url_base}{path}?{urlencode(params_l)}"
        response: Response = self._retry_requests(url)

        count = 0
        if response.ok:
            html: str = response.content.decode("utf-8")
            data: DAny = json.loads(html)
            count = int(data["count"])

        result = {"count": count, "params_d": params_d}
        self._results.append(result)

    def _query_loop(self, path: str, params_d: DList) -> LDAny:
        """Retrieve data from Netbox in loop mode.

        If the number of items in the result exceeds the limit, iterate through the offset
        in a loop mode.

        :param path: Section of the URL that points to the model.
        :param params_d: Parameters to request from the Netbox.

        :return: Netbox objects. Update self _results.
        """
        offset = 0
        max_limit: int = self._set_limit(params_d)
        params_l: LParam = vparam.from_dict(params_d)

        results: LDAny = []
        while True:
            params_i = [*params_l, ("offset", offset)]
            url = f"{self.url_base}{path}?{urlencode(params_i)}"
            response: Response = self._retry_requests(url)
            if response.ok:
                html: str = response.content.decode("utf-8")
                data: DAny = json.loads(html)
                results_: LDAny = list(data["results"])
                results.extend(results_)
            else:
                results_ = []

            # stop requests if limit reached
            if self.limit != len(results_):
                break
            if max_limit and max_limit <= len(results):
                break

            # next iteration
            if self.interval:
                time.sleep(self.interval)
            offset += self.limit

        return results

    def _set_limit(self, params_d: DList) -> int:
        """Update limit valur in params_d based on limit and max_limit

        :return: Max limit value, update params_d["limit"] value
        """
        limit = 0
        if limit_ := vdict.pop("limit", params_d) or []:
            limit = int(limit_[0])
        if not limit:
            limit = self.limit
        max_limit = 0
        if max_limit_ := vdict.pop("max_limit", params_d) or []:
            max_limit = int(max_limit_[0])
        if max_limit and max_limit < limit:
            limit = max_limit
        params_d["limit"] = [limit]
        return max_limit

    def _query_data_thread(self, path: str, params_d: DAny) -> None:
        """Retrieve data from the Netbox.

        If the number of items in the result exceeds the limit, iterate through the offset
        in a loop mode.

        :param path: Section of the URL that points to the model.
        :param params_d: Parameters to request from the Netbox.

        :return: Netbox objects. Update self _results.
        """
        params_l: LParam = vparam.from_dict(params_d)
        url = f"{self.url_base}{path}?{urlencode(params_l)}"
        response: Response = self._retry_requests(url)
        if response.ok:
            html: str = response.content.decode("utf-8")
            data: DAny = json.loads(html)
            results_: LDAny = list(data["results"])
            self._results.extend(results_)

    def _query_pages_count(self, params_ld: LDList) -> LDAny:
        """Retrieve counters of interested objects from Netbox in threaded mode.

        :param params_ld: Parameters to request from the Netbox.

        :return: List of dict with counters and parameters of interested objects.
        """
        self._results = []
        self._query_threads(method=self._query_count, params_ld=params_ld)
        results: LDAny = self._results
        self._results = []
        return results

    def _query_threads(self, method: Callable, params_ld: LDAny) -> None:
        """Retrieve data from Netbox in threaded mode.

        :param method: Method that need call with parameters.
        :param params_ld: Parameters to request from the Netbox.

        :return: None. Save results to self._results.
        """
        queue: Queue = Queue()
        for params_d in params_ld:
            queue.put((method, params_d))

        for idx in range(self.threads):
            if self.interval:
                time.sleep(self.interval)
            thread = Thread(name=f"Thread-{idx}", target=self._run_queue, args=(queue,))
            thread.start()
        queue.join()

    def _run_queue(self, queue: Queue) -> None:
        """Process tasks from the queue.

        This method dequeues and executes tasks until the queue is empty.
        Each task is expected to be a callable method with its corresponding params_d parameters.

        :param queue: A queue containing (method, params_d) pairs to be executed.

        :return: None. Update self _results list.
        """
        while not queue.empty():
            method, params_d = queue.get()
            method(self.path, params_d)
            queue.task_done()

    # ============================== helper ==============================

    def _get_d(self) -> DAny:
        """Get dictionary from the Netbox.

        :return: Dictionary.

        :raise: ConnectionError if status_code is not 200.
        """
        response: Response = self._retry_requests(url=self.url)
        if response.ok:
            html: str = response.content.decode("utf-8")
            return dict(json.loads(html))

        # error
        msg = self._msg_status_code(response)
        raise ConnectionError(f"Netbox server error: {msg}")

    def _get_l(self) -> LDAny:
        """Get list from the Netbox.

        :return: List of dictionary.

        :raise: ConnectionError if status_code is not 200.
        """
        response: Response = self._retry_requests(url=self.url)
        if response.ok:
            html: str = response.content.decode("utf-8")
            return list(json.loads(html))

        # error
        msg = self._msg_status_code(response)
        raise ConnectionError(f"Netbox server error: {msg}")

    def _retry_requests(self, url: str) -> Response:
        """Retry multiple requests if the session times out.

        Multiple requests are useful if Netbox is overloaded and cannot process the request
        right away, but can do so after a sleep interval.

        :param url: The URL that needs to be requested.

        :return: The response.

        :raise: ConnectionError if the limit of retries is reached.
        """
        max_retries = self.max_retries + 1
        counter = 0
        while counter < max_retries:
            counter += 1
            try:
                response: Response = self._session.get(
                    url=url,
                    headers=self._headers(),
                    verify=self.verify,
                    timeout=self.timeout,
                )
            except ReadTimeout:
                attempts = f"{counter} of {self.max_retries}"
                msg = f"Session timeout={self.timeout!r}sec reached, {attempts=}."
                logging.warning(msg)
                if counter < max_retries:
                    msg = f"Next attempt after sleep={self.sleep}sec."
                    logging.warning(msg)
                    time.sleep(self.sleep)
                continue
            except RequestsConnectionError as ex:
                raise ConnectionError(f"Netbox connection error: {ex}") from ex

            if response.ok:
                return response
            msg = self._msg_status_code(response)
            msg.lstrip(".")
            if self._is_status_code_5xx(response):
                raise ConnectionError(f"Netbox server error: {msg}.")
            if self._is_status_code_403_credentials_error(response):
                raise ConnectionError(f"Netbox credentials error: {msg}.")
            if self._is_status_code_400(response):
                logging.warning(msg)
                return response
            raise ConnectionError(f"ConnectionError: {msg}.")

        msg = f"max_retries={self.max_retries!r} reached."
        logging.warning(msg)
        response = Response()
        response.status_code = 504  # Gateway Timeout
        response._content = str.encode(msg)  # pylint: disable=protected-access
        return response

    def _validate_params(self, **kwargs) -> LDList:
        """Validate and update params.

        Remove duplicates, convert single items to list, replace {name} to {name}_id,
        split the parallel parameters into separate items.
        :param kwargs: Filter parameters to update.

        :return: Updated parameters.
        """
        params_d: DList = _lists_wo_dupl(kwargs)
        params_d = self._change_params_name_to_id(params_d)
        params_ld: LDList = h.make_combinations(self._loners, params_d)
        params_ld = h.change_params_or(params_ld)
        params_ld = h.join_params(params_ld, self._default_get)
        return params_ld

    def _headers(self) -> DStr:
        """Session headers with token."""
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }
        return headers

    def _check_keys(self, items: LDAny) -> None:
        """Check if reserved keys are present in the data.

        The Netbox REST API returns the object as a dictionary.
        NbForager inject extra key/value pairs into Netbox object.
        Need to make sure that these keys are not used in Netbox REST API.

        :return: None.
        :raise NbApiError: Reserved key is found in the Netbox object.
        """
        for data in items:
            url_o: ParseResult = urllib.parse.urlparse(data["url"])
            for path, reserved_keys in self._reserved_keys.items():
                if url_o.path.find(path) > -1:
                    if keys := reserved_keys.intersection(data):
                        raise NbApiError(f"NbForager reserved {keys=} detected in {self.url}.")

    def _slice_params_counters(self, results: LDAny) -> LDAny:
        """Generate sliced parameters based on counts in results.

        To request data in threading mode need have all params with offsets.
        :param results: List of dicts with params_d and related counts of objects.
        :return: Sliced parameters.
        """
        params: LDAny = []
        for result in results:
            count = result["count"]
            params_d = result["params_d"]
            if not result["count"]:
                continue
            if count <= self.limit:
                params.append(params_d)
                continue
            params_: LDAny = h.generate_offsets(count, self.limit, params_d)
            params.extend(params_)
        return params

    # ============================== is ==============================

    @staticmethod
    def _is_status_code_4xx(response: Response) -> bool:
        """Return True if status_code 4xx."""
        if 400 <= response.status_code < 500:
            return True
        return False

    @staticmethod
    def _is_status_code_5xx(response: Response) -> bool:
        """Return True if status_code 5xx."""
        if 500 <= response.status_code < 600:
            return True
        return False

    @staticmethod
    def _is_status_code_403_credentials_error(response: Response) -> bool:
        """Return True if invalid credentials."""
        if response.status_code == 403:
            if re.search("Invalid token", response.text, re.I):
                return True
        return False

    @staticmethod
    def _is_status_code_400(response: Response) -> bool:
        """Return True if the object (tag) absent in Netbox."""
        if response.status_code == 400:
            return True
        return False

    # =========================== helpers ===========================

    def _init_default_get(self) -> DList:
        """Init default filtering parameters."""
        params_d_: DList = {}
        for path, params_d in self.default_get.items():
            if path == self.path:
                params_d_ = _lists_wo_dupl(params_d)
                break
        return params_d_

    def _init_loners(self) -> LStr:
        """Init loners filtering parameters."""
        default: DLStr = {
            "any": ["^q$"],
            "ipam/aggregates/": ["^prefix$"],
            "ipam/prefixes/": ["^within_include$"],
            "extras/content-types/": ["id", "app_label", "model"],
        }
        loners_d: DAny = self.loners or default

        loners: LStr = list(loners_d.get("any") or [])
        for path, loners_ in loners_d.items():
            if self.path == path:
                loners.extend(list(loners_))
        return loners

    def _change_params_name_to_id(self, params_d: DList) -> DList:
        """Change parameter with name to parameter with id.

        Request all related objects from the Netbox, find the name, and replace it with the ID.
        :param params_d: Parameters that need to update.
        :return: Updated parameters.
        """
        need_delete: LStr = []
        need_add: DLInt = {}

        mapping_d: DParamPath = param_path.data(self.path)
        need_change: DList = param_path.need_change(params_d, mapping_d)

        for name, values in need_change.items():
            param_path_: ParamPath = mapping_d[name]
            path = param_path_.path
            key = param_path_.key

            response: LDAny = self._query(path)

            if ids := [d["id"] for d in response if d[key] in values]:
                need_delete.append(name)
                name_id = f"{name}_id"
                need_add.setdefault(name_id, []).extend(ids)

        params_d_: DList = {k: v for k, v in params_d.items() if k not in need_delete}
        params_d_.update(need_add)
        return params_d_

    @staticmethod
    def _msg_status_code(response: Response) -> str:
        """Return message ready for logging ConnectionError."""
        if not hasattr(response, "status_code"):
            return ""
        status_code, text, url = response.status_code, response.text, response.url

        pattern = "Page Not Found."
        if re.search(f"<title>{pattern}.+", text):
            text = pattern

        return f"{status_code=} {text=} {url=}"


# ============================= helpers ==========================


def _init_host(**kwargs) -> str:
    """Init Netbox host name."""
    host = str(kwargs.get("host") or "")
    if not host:
        raise ValueError("Host is required.")
    return host


def _init_scheme(**kwargs) -> str:
    """Init scheme: https or http."""
    scheme = str(kwargs.get("scheme") or "")
    expected = ["https", "http"]
    if scheme not in expected:
        raise ValueError(f"{scheme=}, {expected=}")
    return scheme


def _init_threads(**kwargs) -> int:
    """Init threads count, default 1."""
    threads = int(kwargs.get("threads") or 1)
    threads = max(threads, 1)
    return int(threads)


def _init_verify(**kwargs) -> bool:
    """Init verify. False - Requests will accept any TLS certificate."""
    verify = kwargs.get("verify")
    if verify is None:
        return True
    return bool(verify)


def _lists_wo_dupl(kwargs: DAny) -> DList:
    """Convert single values to list and remove duplicate values from params.

    :param kwargs: A dictionary containing the parameters with single or multiple values.
    :return: A dictionary with list of values where duplicates removed.
    """
    params_d: DAny = {}
    for key, value in kwargs.items():
        if isinstance(value, TLists):
            params_d[key] = vlist.no_dupl(list(value))
        else:
            params_d[key] = [value]
    return params_d
