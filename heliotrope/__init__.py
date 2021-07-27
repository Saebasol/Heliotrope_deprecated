from collections import namedtuple

__version__ = "4.0.2"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=4, minor=0, micro=2, releaselevel="final", serial=0)
