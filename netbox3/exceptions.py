"""Exceptions."""


class NbApiError(Exception):
    """Invalid dict key in Netbox data."""


class NbBranchError(Exception):
    """Parsing error in Netbox data."""
