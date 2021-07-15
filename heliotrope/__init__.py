from collections import namedtuple

__version__ = "4.0.1"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=4, minor=0, micro=1, releaselevel="final", serial=0)
