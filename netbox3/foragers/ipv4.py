"""IPv4"""
from ciscoconfparse import IPv4Obj  # type: ignore


class IPv4(IPv4Obj):
    """IPv4, support prefixlen for ip-address."""

    @property
    def ip(self) -> str:
        """IPv4 address without prefixlen, A.B.C.D."""
        return self.exploded

    @property
    def ipv4(self) -> str:
        """IPv4 address with prefixlen, A.B.C.D/LEN."""
        return self.as_cidr_addr

    @property
    def net(self) -> str:
        """IPv4 network with prefixlen, A.B.C.D/LEN."""
        return self.as_cidr_net
