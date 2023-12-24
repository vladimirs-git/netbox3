"""Helper functions."""
import itertools
import urllib
from typing import Any
from urllib.parse import urlencode, ParseResult

from vhelpers import vlist, vparam

from netbox3.types_ import LStr, LDAny, DDDLInt, LValue, LParam, LDList, DList, SeqStr, SStr
from netbox3.types_ import LTInt2, DAny, TValues, TLists, T2Str, T3Str


# =========================== app model id ===========================


def attr_name(obj: Any) -> str:
    """Transform the class name to the attribute name, lowercase without postfix.

    :param obj: The object or name to transform.

    :return: Attribute name.

    :example:
        attr_name("TenantGroupsJ") -> "tenant_groups"
    """
    name = obj.__class__.__name__
    if isinstance(obj, str):
        name = obj
    name = class_to_attr(name)
    if name[:-1].endswith("_"):
        name = name[:-2]
        if name[:-1].endswith("_"):
            name = name[:-2]
    return name


def attr_names(obj: Any) -> LStr:
    """Transform the class names to the attribute names, lowercase without postfix.

    :param obj: The object or name to transform.

    :return: Attribute names.

    :example:
        attr_names(NbForager.tenancy) -> ["tenant_groups", "tenants"]
    """
    attrs = [s for s in dir(obj) if s[0].isupper()]
    methods = [class_to_attr(s)[:-2] for s in attrs]
    return methods


def join_urls(urls: LStr) -> LStr:
    """Join URLs by models with list of IDs in query.

    :param urls: A list of URLs to be joined.

    :return: A list of joined URLs.

    :example:
        urls = ["https://domain.com/api/ipam/vrfs/1", "https://domain.com/api/ipam/vrfs/2"]
        join_urls(urls) -> ["https://domain.com/api/ipam/vrfs?id=1&id=2"]
    """
    items = []
    for url in sorted(urls):
        url_l = url.split("/")
        url_base = "/".join(url_l[:-3])
        app, model, digit = url_l[-3:]
        item = (url_base, app, model, digit)
        items.append(item)

    # create dict
    data_uam: DDDLInt = {}
    for url_base, app, model, _ in items:
        data_uam.setdefault(url_base, {}).setdefault(app, {}).setdefault(model, [])

    # append ids
    for url_base, app, model, digit in items:
        data_uam[url_base][app][model].append(int(digit))

    # join urls
    urls_: LStr = []
    for url_base, data_am in data_uam.items():
        for app, data_m in data_am.items():
            for model, ids in data_m.items():
                params = urlencode({"id": sorted(set(ids))}, doseq=True)
                url = f"{url_base}/{app}/{model}?{params}"
                urls_.append(url)
    return urls_


def model_to_attr(model: str) -> str:
    """Convert model name to attribute name.

    :param model: The model name to be converted.

    :return: The converted attribute name.

    :example:
        model_to_attr("ip-addresses") -> "ip_addresses"
    """
    return "_".join(model.split("-"))


def attr_to_model(attr: str) -> str:
    """Convert attribute name to model name.

    :param attr: The attribute name to be converted.

    :return: The converted model name.

    :example:
        attr_to_model("ip_addresses") -> "ip-addresses"
    """
    return "-".join(attr.split("_"))


def nested_urls(nb_objects: LDAny) -> LStr:
    """Get a list of URLs from a Netbox nested objects.

    :param nb_objects: A list of Netbox objects.

    :return: URLs of nested objects.
    """
    urls: LStr = []
    for nb_object in nb_objects:
        if not isinstance(nb_object, dict):
            continue
        for key, value in nb_object.items():
            if key == "url" and isinstance(value, str):
                urls.append(value)
            elif isinstance(value, list):
                urls_ = nested_urls(value)
                urls.extend(urls_)
            elif isinstance(value, dict):
                if url := value.get("url"):
                    if isinstance(url, str):
                        urls.append(url)
    urls = vlist.no_dupl(urls)
    return sorted(urls)


def path_to_attrs(path: str) -> T2Str:
    """Convert path of app/model to attribute names.

    :param path: Path of app/model.

    :return: Application and model attribute names.

    :example:
        path_to_attrs("ipam/ip-addresses") -> "ipam", "ip_addresses"
    """
    app, model = path.strip("/").split("/")
    model = model_to_attr(model)
    return app, model


def class_to_attr(word: str) -> str:
    """Replace upper character with underscore and lower.

    :param word: The word to be modified.

    :return: The modified word.

    :example: replace_upper("IpAddresses") -> "ip_addresses"
    """
    if not word:
        return ""
    word = word[0].lower() + word[1:]
    new_word = ""
    for char in word:
        if char.isupper():
            new_word += "_" + char.lower()
        else:
            new_word += char
    return new_word


def split_url(url: str) -> T3Str:
    """Split the URL into the application, model, and ID items.

    :param url: The URL to be parsed.

    :return: A tuple containing the application, model, and port (if available).
             If the URL is invalid or does not contain the necessary items, returns empty strings.

    :example:
        split_url("https://demo.netbox.dev/api/ipam/vrfs?id=1") -> ("ipam", "vrfs", "1")
    """
    url_o: ParseResult = urllib.parse.urlparse(url)
    if not url_o.path:
        return "", "", ""
    path = url_o.path.strip("/")
    items = path.split("/")
    if len(items) < 2:
        return "", "", ""
    if items[0] == "api":
        items = items[1:]
    if len(items) < 2 or len(items) > 3:
        return "", "", ""

    app = str(items[0])
    model = str(items[1])
    port = ""
    if len(items) == 3:
        port = str(items[2])
    return app, model, port


def url_to_path(url: str) -> str:
    """Convert URL to path app/model.

    :param url: URL to split.
    :return: Path with application and model.
    :example:
        url_to_path("https://domain.com/api/ipam/vrf/1?id=1") -> "ipam/vrf/"
    """
    app, model, _ = split_url(url)
    if app and model:
        return f"{app}/{model}/"
    raise ValueError(f"{app=} {model=} required.")


# ============================== params ==============================


def join_params(params_ld: LDList, default_get: DList) -> LDList:
    """Join params_ld and default filtering parameters.

    :param params_ld: Filtering parameters.
    :param default_get: Default filtering parameters.
    :return: Joined filtering parameters.
    """
    if not params_ld:
        if not default_get:
            return []
        return [default_get.copy()]

    params_ld_: LDList = []
    for params_d in params_ld.copy():
        if not params_d:
            continue
        default_d = {k: v for k, v in default_get.items() if k not in params_d}
        params_d.update(default_d)
        params_ld_.append(params_d)
    return params_ld_


def make_combinations(need_split: SeqStr, params_d: DList) -> LDList:
    """Split the parallel parameters from the kwargs dictionary to valid combinations.

    Need to be split predefined in the need_split list and boolean values in params_d.
    :param need_split: Parameters that need to be split into different requests.
    :param params_d: A dictionary of keyword arguments.
    :return: A list of dictionaries containing the valid combinations.
    """
    keys_need_split = _get_keys_need_split(need_split, params_d)
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


def change_params_or(params_ld: LDList) -> LDList:
    """Change ``parameter`` with name ``or_{parameter}``.

    :param params_ld: Parameters that need to update.
    :return: Updated parameters.
    """
    params_ld_: LDList = []
    for params_d in params_ld:
        params_d_: DList = {}
        for name, values in params_d.items():
            if name.startswith("or_"):
                name = name.replace("or_", "", 1)
            params_d_[name] = values
        params_ld_.append(params_d_)
    return params_ld_


def _get_keys_need_split(need_split: SeqStr, params_d: DList) -> SStr:
    """Get keys that need to be split.

    :param need_split: Parameters that need to be split into different requests.
    :param params_d: A dictionary of keyword arguments.
    :return: Keys that need to be split.
    """
    keys_need_split: SStr = set()

    keys = list(params_d)
    while keys:
        key = keys.pop(0)
        # predefined
        for need_split_ in need_split:
            if key == need_split_:
                keys_need_split.add(key)
                break
        # or_{parameter}
        if key.startswith("or_"):
            keys_need_split.add(key)

    return keys_need_split


def generate_slices(url: str, max_len: int, key: str, values: LValue, params: LParam) -> LTInt2:
    """Generate start and end indexes of parameters, ready for URL slicing.

    :param url: URL that need to split.
    :param max_len: Maximum length of URL.
    :param key: The key of the parameter that needs to be sliced.
    :param values: The values of the parameter that need to be sliced.
    :param params: Other parameters that need to be mentioned in the URL.

    :return: The start and end indexes of the parameters, ready for URL slicing.
    """
    if len(values) <= 1:
        return [(0, 1)]

    slices: LTInt2 = []
    start = 0
    for end in range(1, len(values) + 1):
        end_ = end + 1
        params_ = [(key, s) for s in values[start:end_]]
        params_ = [*params, *params_]
        url_ = f"{url}?{urlencode(params_)}"
        if end_ < len(values) + 1 and len(url_) < max_len:
            continue
        slices.append((start, end))
        start = end
    return slices


def slice_params_d(url: str, max_len: int, key: str, params_d: DList) -> LDList:
    """Generate sliced parameters, ready for URLs with valid length.

    If the length of the URL exceeds maximum allowed (due to a large number of parameters),
    then need split (slice) the request into multiple parts.
    :param url: URL that need to split.
    :param max_len: Maximum length of URL.
    :param key: The key of the parameter that needs to be sliced.
    :param params_d: Filter parameters, where one of key/value need be sliced.

    :return: Sliced parameters.

    :example:
        slice_params_d(max_len=50, params_d={"address": ["10.0.0.1", "10.0.0.2"], "family": 4}) ->
        [{"address": ["10.0.0.1"], "family": 4}, {"address": ["10.0.0.2"], "family": 4}]
    """
    values: LValue = _validate_values(values=params_d[key])
    params_wo_key: LParam = [(k, v) for k, v in params_d.items() if k != key]

    slices: LTInt2 = generate_slices(
        url=url,
        max_len=max_len,
        key=key,
        values=values,
        params=[*params_wo_key, ("offset", 1000), ("limit", 1000)],
    )

    params_sliced: LDList = []
    for start, end in slices:
        params_l: LParam = params_wo_key + [(key, s) for s in values[start:end]]
        params_sliced_: DList = vparam.to_dict(params_l)
        params_sliced.append(params_sliced_)
    return params_sliced


def slice_params_ld(url: str, max_len: int, keys: LStr, params_ld: LDList) -> LDList:
    """Split params into different lists if slicing is required.

    :param url: URL that need to split.
    :param max_len: Maximum length of URL.
    :param keys: The keys of the parameters that could be sliced.
    :param params_ld: A list of parameters.

    :return: A list of sliced parameters.
    """
    params_ld_: LDList = []

    for params_d in params_ld:
        # no need slice
        key_of_long_value = get_key_of_longest_value(params_d)
        if not key_of_long_value:
            params_ld_.append(params_d)
            continue

        # no need slice
        if key_of_long_value not in keys:
            params_ld_.append(params_d)
            continue

        # need slice
        params_sliced: LDList = slice_params_d(
            url=url,
            max_len=max_len,
            key=key_of_long_value,
            params_d=params_d,
        )
        params_ld_.extend(params_sliced)

    if not params_ld_:
        params_ld_ = [{}]

    return params_ld_


def _validate_values(values: Any) -> LValue:
    """Convert a value to a list and remove duplicates.

    :param values: The value to be converted.

    :return: A list of values.
    """
    if isinstance(values, TValues):
        return [values]
    values_ = _validate_value(values)
    return values_


def _validate_value(value: Any) -> LValue:
    """Check typing, remove duplicate values from list.

    :param value: The value to be validated.

    :return: A valid value.
    """
    if isinstance(value, TValues):
        return [value]
    if not isinstance(value, TLists):
        raise TypeError(f"{value=}, {TValues} expected")

    values: LValue = []
    for value_ in value:
        if not isinstance(value_, TValues):
            raise TypeError(f"{value_=}, {TValues} expected")
        values.append(value_)

    values = vlist.no_dupl(values)
    return values


def get_key_of_longest_value(params_d: DList) -> str:
    """Get the key of the parameter with the longest joined value.

    :param params_d: A dictionary of parameters.

    :return: The key of the parameter with the longest value.
    """
    if not params_d:
        return ""
    lengths_d = {}
    for key, values in params_d.items():
        value = "".join([str(i) for i in values])
        lengths_d[key] = len(value)
    max_key = max(lengths_d, key=lambda k: lengths_d[k])
    return max_key


def generate_offsets(count: int, limit: int, params_d: DAny, /) -> LDAny:
    """Generate a list of dictionaries with offset parameters.

    :param count: The total count of items to be processed.
    :param limit: The maximum limit for each batch.
    :param params_d: A dictionary containing other parameters.

    :return: A list of dictionaries with offset and other parameters.
    """
    if count <= 0 or limit <= 0:
        raise ValueError(f"{count=} {limit=}, value higher that 1 expected.")

    params: LDAny = []
    offset = 0
    while count > 0:
        limit_ = min(count, limit)
        params_d_ = params_d.copy()
        params_d_["limit"] = limit
        params_d_["offset"] = offset
        params.append(params_d_)
        offset += limit_
        count -= limit_

    return params
