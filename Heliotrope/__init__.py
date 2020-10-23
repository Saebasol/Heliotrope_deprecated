from collections import namedtuple

__version__ = "2.8.5"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=2, minor=8, micro=5, releaselevel="final", serial=0)
