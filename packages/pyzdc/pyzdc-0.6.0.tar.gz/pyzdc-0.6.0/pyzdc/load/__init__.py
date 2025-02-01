"""
This module provides utilities for interacting with a DuckDB database.

Available classes:
- Loader: A class for loading data from a DuckDB table into a pandas DataFrame.
"""

from .show_data import Loader
from .refresh_data import Refresher

__all__ = ["Loader", "Refresher"]

__version__ = "0.5.0"
__author__ = "Gutto França"
__email__ = "guttolaudie@gmail.com"
