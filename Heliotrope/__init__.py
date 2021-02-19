from collections import namedtuple

__version__ = "3.3.8"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=3, minor=3, micro=8, releaselevel="final", serial=0)
