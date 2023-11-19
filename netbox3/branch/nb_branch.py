# pylint: disable=R0904

"""NbBranch."""
from typing import Type

from vhelpers import vstr

from netbox3 import wrappers
from netbox3.exceptions import NbBranchError
from netbox3.types_ import DAny, SeqStr, LStr


class NbBranch:
    """Extracts a value from a Netbox object using a chain of keys and returns
    the typed value. Netbox object has None instead of a dictionary when
    a related object is absent, which is why it is necessary to constantly
    check the data type. NbBranch returns the desired value with the expected
    data type, even if the data is missing.
    """

    def __init__(self, data: DAny, strict: bool = False, **kwargs):
        """Init NbBranch.

        :param data: Netbox object.
        :type data: dict

        :param strict: True - if data is invalid raise NbBranchError,
            False - if data is invalid return empty data with proper type.
        :type strict: bool

        :param version: Netbox version.
            Designed for compatibility with different versions.
        :type version: str
        """
        self.data = _init_data(data)
        self.strict = strict
        self.version = str(kwargs.get("version") or "0")

    def __repr__(self):
        """__repr__."""
        data = None
        if isinstance(self.data, dict):
            params_d = {}
            if name := self.data.get("name"):
                params_d["name"] = str(name)
            elif address := self.data.get("address"):
                params_d["address"] = str(address)
            elif prefix := self.data.get("name"):
                params_d["prefix"] = str(prefix)
            elif id_ := self.data.get("id"):
                params_d["id"] = str(id_)
            data = vstr.repr_params(**params_d)

        name = self.__class__.__name__
        return f"<{name}: {data}>"

    # ====================== universal get methods =======================

    def dict(self, *keys) -> dict:
        """Get dictionary value by keys.

        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: Dictionary value or an empty dictionary if the value is absent.
        :rtype: dict

        :raise NbBranchError: If strict=True and the value is not a dictionary or key is absent.
        """
        return self._get_keys(type_=dict, keys=keys, data=self.data)

    def int(self, *keys) -> int:
        """Get integer value by keys.

        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: Integer value or 0 if the value is absent.
        :rtype: int

        :raise NbBranchError: If strict=True and the value is not a digit or key is absent.
        """
        data = self.data
        try:
            for key in keys:
                data = data[key]
        except (KeyError, TypeError) as ex:
            if self.strict:
                type_ = type(ex).__name__
                raise NbBranchError(f"{type_}: {ex}, {keys=} in {self._source()}") from ex
            return 0

        if isinstance(data, int):
            return data

        if isinstance(data, str) and data.isdigit():
            return int(data)

        if self.strict:
            raise NbBranchError(f"{keys=} {int} expected in {self._source()}.")
        return 0

    def list(self, *keys) -> list:
        """Get list value by keys.

        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: List value or an empty list if the value is absent.
        :rtype: list

        :raise NbBranchError: If strict=True and the value is not a list or key is absent.
        """
        return self._get_keys(type_=list, keys=keys, data=self.data)

    def str(self, *keys) -> str:
        """Get string value by keys.

        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: String value or an empty string if the value is absent.
        :rtype: str

        :raise NbBranchError: If strict=True and the value is not a string or key is absent.
        """
        return self._get_keys(type_=str, keys=keys, data=self.data)

    @wrappers.strict_value
    def strict_dict(self, *keys) -> dict:
        """Get dictionary value by keys in strict manner, value is mandatory.

        Useful when strict=False, but you need to obtain a value in a strict manner.
        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: Dictionary value.
        :rtype: dict

        :raise NbBranchError: If the value is not a dictionary or key is absent or value is empty.
        """
        return self.dict(*keys)

    @wrappers.strict_value
    def strict_int(self, *keys) -> int:
        """Get integer value by keys in strict manner, value is mandatory.

        Useful when strict=False, but you need to obtain a value in a strict manner.
        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: Integer value.
        :rtype: int

        :raise NbBranchError: If the value is not a int or key is absent or value is 0.
        """
        return self.int(*keys)

    @wrappers.strict_value
    def strict_list(self, *keys) -> list:
        """Get string value by keys in strict manner, value is mandatory.

        Useful when strict=False, but you need to obtain a value in a strict manner.
        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: List value.
        :rtype: list

        :raise NbBranchError: If the value is not a list or key is absent or value is empty.
        """
        return self.list(*keys)

    @wrappers.strict_value
    def strict_str(self, *keys) -> str:
        """Get string value by keys in strict manner, value is mandatory.

        :param keys: Chaining dictionary keys to retrieve the desired value.

        :return: String value.
        :rtype: str

        :raise NbBranchError: If the value is not a string or key is absent or value is absent.
        """
        return self.str(*keys)

    def _get_keys(self, type_: Type, keys: SeqStr, data: dict):
        """Retrieve values from data using keys and check their data types.

        :param type_: Data type.
        :param keys: Chaining dictionary keys to retrieve the desired value.
        :param data: Dictionary.

        :return: Value with proper data type.

        :raise NbBranchError: If strict=True and key absent or type not match.
        """
        try:
            for key in keys:
                data = data[key]
        except (KeyError, TypeError) as ex:
            if self.strict:
                ex_type = type(ex).__name__
                raise NbBranchError(f"{ex_type}: {ex}, {keys=} in {self._source()}.") from ex
            return type_()

        if not isinstance(data, type_):
            if self.strict:
                ex_type = "TypeError"
                raise NbBranchError(f"{ex_type}: {keys=} {type_} expected in {self._source()}.")
            return type_()

        return data

    def tags(self) -> LStr:
        """Get tag slugs from the data.

        :return: List og tag slugs.
        :rtype: lstr
        """
        tags_ = self.list("tags")
        if not tags_:
            return []

        tags: LStr = []
        for tag_d in tags_:
            if tag := self._get_keys(type_=str, keys=["slug"], data=tag_d):
                tags.append(tag)
        return tags

    def _source(self) -> str:
        """Return URL of source object or data."""
        if isinstance(self.data, dict):
            if url := self.data.get("url"):
                return str(url)
        return str(self.data)


def _init_data(data: DAny) -> DAny:
    """Init data."""
    if data is None:
        return {}
    if isinstance(data, dict):
        return data
    raise TypeError(f"{data=} {dict} expected.")
