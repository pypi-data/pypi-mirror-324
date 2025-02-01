"""
This module provides a class for extracting SINAN data and handling it with DuckDB.

Available classes:
- Extractor: A class for extracting SINAN data and inserting it into a DuckDB database.
"""

from .get_raw import Extractor

__all__ = ["Extractor"]

__version__ = "0.6.1"
__author__ = "Gutto França"
__email__ = "guttolaudie@gmail.com"
