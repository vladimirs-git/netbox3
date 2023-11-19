"""Wrapper helpers."""

from functools import wraps

from netbox3.exceptions import NbBranchError


def strict_value(method):
    """Wrap method to check value in strict manner, returned value is mandatory.

    :param method: The method to be decorated.

    :return: The decorated function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap."""
        strict_actual = self.strict
        self.strict = True

        result = method(self, *args, **kwargs)

        self.strict = strict_actual
        if not result:
            keys = "/".join(args)
            raise NbBranchError(f"{keys=} expected in {self._source()}.")

        return result

    return wrapper
