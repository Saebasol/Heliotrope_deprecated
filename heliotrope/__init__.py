from typing import Literal, NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=4, minor=0, micro=0, releaselevel="alpha", serial=0)

__version__ = f"{version_info.major}.{version_info.minor}.{version_info.micro}-{version_info.releaselevel}"
