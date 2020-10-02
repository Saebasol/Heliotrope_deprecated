from collections import namedtuple

__version__ = "2.5.1"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=2, minor=5, micro=1, releaselevel="final", serial=0)
