from importlib.metadata import version, PackageNotFoundError
from gsnapshot import *

try:
    __version__ = version('gsnapshot')
except PackageNotFoundError:
    __version__ = "unknown version"

