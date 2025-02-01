"""
Absfuyu: Core
-------------
Contain type hints and other stuffs

Version: 2.3.1
Date updated: 01/02/2025 (dd/mm/yyyy)
"""

# Module Package
###########################################################################
__all__ = [
    # color
    "CLITextColor",
    # path
    "CORE_PATH",
    "CONFIG_PATH",
    "DATA_PATH",
]

__package_feature__ = ["beautiful", "extra", "res", "full", "dev"]


# Library
###########################################################################
from importlib import import_module
from importlib.resources import files


class CLITextColor:
    """Color code for text in terminal"""

    WHITE = "\x1b[37m"
    BLACK = "\x1b[30m"
    BLUE = "\x1b[34m"
    GRAY = "\x1b[90m"
    GREEN = "\x1b[32m"
    RED = "\x1b[91m"
    DARK_RED = "\x1b[31m"
    MAGENTA = "\x1b[35m"
    YELLOW = "\x1b[33m"
    RESET = "\x1b[39m"


# CORE_PATH = Path(__file__).parent.absolute()
CORE_PATH = files("absfuyu")
CONFIG_PATH = CORE_PATH.joinpath("config", "config.json")
DATA_PATH = CORE_PATH.joinpath("pkg_data")


# tqdm wrapper
try:
    tqdm = import_module("tqdm").tqdm
except ModuleNotFoundError:

    def tqdm(iterable, **kwargs):
        return iterable
