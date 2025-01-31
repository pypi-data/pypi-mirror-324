# read version from installed package
from importlib.metadata import version
__version__ = version("date_extractor_mds")

from date_extractor_mds.date_extractor_mds import *