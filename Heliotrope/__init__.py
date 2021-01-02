from collections import namedtuple

__version__ = "3.2.4"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=3, minor=2, micro=4, releaselevel="final", serial=0)
