from collections import namedtuple

__version__ = "2.8.4"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=2, minor=8, micro=4, releaselevel="final", serial=0)
