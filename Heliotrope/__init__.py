from collections import namedtuple

__version__ = "1.5.0"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=1, minor=1, micro=1, releaselevel="final", serial=0)
