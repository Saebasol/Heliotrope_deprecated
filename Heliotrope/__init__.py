from collections import namedtuple

__version__ = "2.8.3"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=2, minor=8, micro=3, releaselevel="final", serial=0)
