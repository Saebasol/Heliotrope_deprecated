from collections import namedtuple

__version__ = "2.6.1"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=2, minor=6, micro=1, releaselevel="final", serial=0)
