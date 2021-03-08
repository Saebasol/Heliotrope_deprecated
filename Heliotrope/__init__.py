from collections import namedtuple

__version__ = "3.5.0"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=3, minor=5, micro=0, releaselevel="final", serial=0)
