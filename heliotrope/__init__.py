from collections import namedtuple

__version__ = "4.0.0-beta"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=4, minor=0, micro=0, releaselevel="beta", serial=0)
