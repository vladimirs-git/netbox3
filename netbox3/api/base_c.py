# pylint: disable=R0902,R0903

"""Connector Base."""

from __future__ import annotations

import itertools
import json
import logging
import re
import time
from operator import itemgetter
from queue import Queue
from threading import Thread
from typing import Callable
from urllib.parse import urlencode

import requests
from requests import Session, Response
from requests.exceptions import ReadTimeout, ConnectionError as RequestsConnectionError
from vhelpers import vdict, vlist, vparam

from netbox3 import helpers as h
from netbox3.exceptions import NbApiError
from netbox3.types_ import DAny, DStr, LDAny, SStr, LStr, DLInt, DList, LDList
from netbox3.types_ import TLists, OUParam, SeqStr, OSeqStr, LParam


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
    ]
    _reserved_ipam_keys = [
        "overlapped",
        "warnings",
        "nbnets",
        "nbnets__subnets",
    ]

    def __init__(self, **kwargs):
        """Init BaseC.

        :param host: Netbox host name.
        :param token: Netbox token.
        :param scheme: Access method: https or http. Default "https".
        :param port: TCP port. Default 443. NOTE: Not implemented.

        :param verify: Transport Layer Security. True - A TLS certificate required,
            False - Requests will accept any TLS certificate.
        :param limit: Split the query to multiple requests if the response exceeds the limit.
            Default 1000.
        :param url_length: Split the query to multiple requests if the URL length exceeds
            this value. Default 2047.
        :param threads: Threads count. Default 1, loop mode.
        :param interval: Wait this time between requests (seconds).
            Default 0. Useful for request speed shaping.

        :param timeout: Request timeout (seconds). Default 60.
        :param max_retries: Retry the request multiple times if it receives a 500 error
            or timed-out. Default 1.
        :param sleep: Interval before the next retry after receiving a 500 error (seconds).
            Default 10.
        """
        self.host: str = _init_host(**kwargs)
        self.token: str = str(kwargs.get("token") or "")
        self.scheme: str = _init_scheme(**kwargs)
        self.port: int = int(kwargs.get("port") or 0)

        self.verify: bool = _init_verify(**kwargs)
        self.limit: int = int(kwargs.get("limit") or 1000)
        self.timeout: float = float(kwargs.get("timeout") or 60)
        self.max_retries: int = int(kwargs.get("max_retries") or 1)
        self.sleep: float = float(kwargs.get("sleep") or 10)
        self.calls_interval: float = float(kwargs.get("sleep") or 0)
        self.threads: int = _init_threads(**kwargs)
        self.interval: float = float(kwargs.get("interval") or 0.0)
        self.url_length = int(kwargs.get("url_length") or 2047)

        self.default: DAny = {}  # default params
        self._need_split: LStr = [
            "^cf_.+",
            "^q$",
            "^status$",
            "^tag$",
            "^has_primary_ip$",  # dcim/devices, virtualization/virtual-machines
            "^virtual_chassis_member$",  # dcim/devices
            "^assigned_to_interface$",  # ipam/ip-addresses
            "^family$",  # ipam/aggregates, prefixes, ip-addresses
            "^mask_length$",  # ipam/aggregates, prefixes, ip-addresses
            "^ui_visibility$",  # extras/custom-fields
        ]
        self._param_id_map: DAny = self._init_param_id_map()
        self._results: LDAny = []  # cache for received objects from Netbox
        self._session: Session = requests.session()

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.host}>"

    def _init_param_id_map(self) -> DAny:
        """Init a dictionary that maps model name to their corresponding new path.

        This mapping is used to get objects from Netbox by name instead of id.

        :return: Dictionary with mapping data.
        """
        data = {
            # circuits
            "circuit": {"path": "circuits/circuits/", "key": "cid"},
            "provider": {"path": "circuits/providers/", "key": "name"},
            "provider_account": {"path": "circuits/provider-accounts/", "key": "name"},
            # dcim
            "platform": {"path": "dcim/platforms/", "key": "name"},
            "region": {"path": "dcim/regions/", "key": "name"},
            "site": {"path": "dcim/sites/", "key": "name"},
            "site_group": {"path": "dcim/site-groups/", "key": "name"},
            # extras
            "content_type": {"path": "extras/content-types/", "key": "display"},
            "for_object_type": {"path": "extras/content-types/", "key": "display"},
            # ipam
            "export_target": {"path": "ipam/route-targets/", "key": "name"},
            "exporting_vrf": {"path": "ipam/vrfs/", "key": "name"},
            "import_target": {"path": "ipam/route-targets/", "key": "name"},
            "importing_vrf": {"path": "ipam/vrfs/", "key": "name"},
            "present_in_vrf": {"path": "ipam/vrfs/", "key": "name"},
            "rir": {"path": "ipam/rirs/", "key": "name"},
            "vrf": {"path": "ipam/vrfs/", "key": "name"},
            # tenancy
            "tenant": {"path": "tenancy/tenants/", "key": "name"},
            "tenant_group": {"path": "tenancy/tenant-groups/", "key": "name"},
            # virtualization
            "bridge": {"path": "virtualization/interfaces/", "key": "name"},
        }

        group_map = {
            "dcim/sites/": {"group": {"path": "dcim/site-groups/", "key": "name"}},
            "ipam/vlans/": {"group": {"path": "ipam/vlan-groups/", "key": "name"}},
            "tenancy/tenants/": {"group": {"path": "tenancy/tenant-groups/", "key": "name"}},
            "virtualization/clusters/": {
                "group": {"path": "virtualization/cluster-groups/", "key": "name"}
            },
        }
        if data_ := group_map.get(self.path):
            data.update(data_)

        # ipam/ip-addresses/ use parent without map
        parent_map = {
            "dcim/locations/": {"parent": {"path": "dcim/locations/", "key": "name"}},
            "dcim/regions/": {"parent": {"path": "dcim/regions/", "key": "name"}},
            "dcim/site-groups/": {"parent": {"path": "dcim/site-groups/", "key": "name"}},
            "tenancy/tenant-groups/": {"parent": {"path": "tenancy/tenant-groups/", "key": "name"}},
            "virtualization/interfaces/": {
                "parent": {"path": "virtualization/interfaces/", "key": "name"}
            },
        }
        if data_ := parent_map.get(self.path):
            data.update(data_)

        # role
        if self.path == "virtualization/virtual-machines/":
            data.update({"role": {"path": "dcim/device-roles/", "key": "name"}})
        else:
            data.update({"role": {"path": "ipam/roles/", "key": "name"}})

        # type
        if self.path == "circuits/circuits/":
            data.update({"type": {"path": "circuits/circuit-types/", "key": "name"}})

        return data

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

    def _query_params_ld(self, params: LDList) -> LDAny:
        """Retrieve data from the Netbox.

        :param params: Parameters to request from the Netbox.

        :return: A list of the Netbox objects.
        """
        self._results = []
        params_ld: LDList = h.slice_params_ld(
            url=self.url,
            max_len=self.url_length,
            keys=self._slices,
            params=params,
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
        counter = 0
        while counter < self.max_retries:
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
                if counter < self.max_retries:
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
        kwargs = self._change_param_name_to_id(kwargs)
        params_d: DList = _lists_wo_dupl(kwargs)
        params_ld: LDList = _make_combinations(self._need_split, params_d)
        params_ld = self._join_params(*params_ld)
        return params_ld

    def _headers(self) -> DStr:
        """Session headers with token."""
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }
        return headers

    def _join_params(self, *params) -> LDList:
        """Join received and default filtering parameters.

        :param params: Received filtering parameters.
        :return: Joined filtering parameters.
        """
        if not params:
            return [self.default.copy()]

        params_ld: LDList = []
        default_keys = sorted(list(self.default), reverse=True)
        for params_d in params:
            for key in default_keys:
                if params_d.get(key) is None:
                    params_d = {**{key: self.default[key]}, **params_d}
            params_ld.append(params_d)
        return params_ld

    @staticmethod
    def _check_keys(items: LDAny, denied: OSeqStr = None) -> None:
        """Check if denied keys are absent in the data.

        The Netbox REST API returns the object as a dictionary.
        Some of my dirty scripts inject extra key/value pairs into this object.
        I need to make sure that these keys are not used in Netbox.

        :return: True if all denied keys are absent in the data, otherwise if a denied key is
            found in the object.
        """
        if denied is None:
            denied = []

        denied_keys: SStr = set()
        for data in items:
            for key in denied:
                if key in data:
                    denied_keys.add(key)
                    msg = f"Denied {key=} in Netbox {data=}"
                    logging.error(msg)
        if denied_keys:
            raise NbApiError(f"Netbox data contains {denied_keys=}")

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

    # =========================== messages ===========================

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

    # ======================== params helpers ========================

    def _change_param_name_to_id(self, params_d: DAny) -> DAny:
        """Change parameter with name to parameter with id.

        Request all related objects from the Netbox, find the name, and replace it with the ID.
        :param params_d: Parameters that need to update.
        :return: Updated parameters.
        """
        need_delete: LStr = []
        need_add: DLInt = {}
        for name, value in params_d.items():
            values = vlist.to_list(value)
            if name in self._param_id_map:
                path = self._param_id_map[name]["path"]
                key = self._param_id_map[name]["key"]

                response: LDAny = self._query(path=path)

                if ids := [d["id"] for d in response if d[key] in values]:
                    need_delete.append(name)
                    name_id = f"{name}_id"
                    need_add.setdefault(name_id, []).extend(ids)

        params_d_ = {k: v for k, v in params_d.items() if k not in need_delete}
        params_d_.update(need_add)
        return params_d_


# ============================= helpers ==========================


def _init_host(**kwargs) -> str:
    """Init Netbox host name."""
    host = str(kwargs.get("host") or "")
    if not host:
        raise ValueError("Host is required.")
    return host


def _init_scheme(**kwargs) -> str:
    """Init scheme "https" or "http"."""
    scheme = str(kwargs.get("scheme") or "https")
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


def _make_combinations(need_split: SeqStr, params_d: DList) -> LDList:
    """Split the parallel parameters from the kwargs dictionary to valid combinations.

    Need to be split predefined in the need_split list and boolean values in params_d.
    :param need_split: Parameters that need to be split into different requests.
    :param params_d: A dictionary of keyword arguments.
    :return: A list of dictionaries containing the valid combinations.
    """
    keys_need_split: SStr = set()

    keys = list(params_d)
    while keys:
        key = keys.pop()
        # predefined
        for regex in need_split:
            if re.search(regex, key):
                keys_need_split.add(key)
                break
        # boolean
        for value in params_d[key]:
            if isinstance(value, bool):
                keys_need_split.add(key)
                break

    no_need_split_d = {k: v for k, v in params_d.items() if k not in keys_need_split}

    key_no_need_split = ""
    need_split_d: DList = {}
    for key, values in params_d.items():
        if key in keys_need_split:
            for value in values:
                need_split_d.setdefault(key, []).append({key: [value]})
        else:
            key_no_need_split = key

    params_l = list(need_split_d.values())
    if key_no_need_split:
        params_l.append([no_need_split_d])

    params_ld: LDList = []
    combinations = list(itertools.product(*params_l))
    for combination in combinations:
        params_d_ = {}
        for param_d_ in combination:
            params_d_.update(param_d_)
        if params_d_:
            params_ld.append(params_d_)
    return params_ld
