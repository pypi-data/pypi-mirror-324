# read version from installed package
from importlib.metadata import version
__version__ = version("dsci524_group29_webscraping")

# Import core functions or modules to expose them at the package level
from .save_data import save_data
from .parse_content import parse_content
from .fetch_html import fetch_html