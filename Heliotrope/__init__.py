from collections import namedtuple

__version__ = "3.0.0"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=3, minor=0, micro=0, releaselevel="final", serial=0)
