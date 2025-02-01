"""
This module provides classes for transforming DuckDB databases and renaming columns
based on a JSON mapping.

Available classes:
- ColumnTransformer: Handles column renaming and normalization for DuckDB tables.
- DBTransformer: Creates new normalized tables from a raw database table and removes
                  the original table.
"""

from .transform_columns import ColumnTransformer
from .transform_db import DBTransformer

__all__ = ["ColumnTransformer", "DBTransformer"]

__version__ = "0.5.0"
__author__ = "Gutto França"
__email__ = "guttolaudie@gmail.com"
