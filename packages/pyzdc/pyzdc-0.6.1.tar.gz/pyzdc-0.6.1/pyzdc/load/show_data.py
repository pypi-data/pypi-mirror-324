import logging
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd

from pyzdc.utils.config import DB_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Loader:
    """
    Loader class for loading data from a DuckDB database.

    Attributes:

    Methods:
        __init__(db_path: Path = DB_PATH):
        _validate_db_path() -> None:
            Validate if the DuckDB database file exists.
        load_data(table_name: str = "sinan", limit: Optional[int] = None)
        -> pd.DataFrame:
    """

    def __init__(self, db_path: Path = DB_PATH):
        """
        Initialize the Loader with a database path.

        Parameters:
            db_path (Path): Path to the DuckDB database file.
        """
        self.db_path = db_path
        self._validate_db_path()

    def _validate_db_path(self) -> None:
        """Validate if the DuckDB database file exists."""
        if not self.db_path.exists():
            logging.error(f"Database not found at {self.db_path}")
            raise FileNotFoundError(f"Database not found at {self.db_path}")

    def load_data(
        self, table_name: str = "sinan", limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Load data from a DuckDB database table into a pandas DataFrame.

        Parameters:
            table_name (str): The name of the table to load data from.
                Defaults to "sinan".
            limit (Optional[int]): The maximum number of rows to load.
                If None, all rows are loaded. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the data loaded from the specified
            DuckDB table.

        Raises:
            Exception: If there is an error loading data from the DuckDB database.
        """
        try:
            with duckdb.connect(str(self.db_path)) as conn:
                query = f"SELECT * FROM {table_name}"
                if limit:
                    query += f" LIMIT {limit}"
                logging.info(
                    f"Loading data from table '{table_name}' in DuckDB database."
                )

                data_arrow = conn.execute(query).fetch_arrow_table()
                data: pd.DataFrame = data_arrow.to_pandas()

                logging.info("Data loaded successfully.")
                return data

        except Exception as e:
            logging.error(f"Error loading data from DuckDB: {e}")
            raise


if __name__ == "__main__":
    db_loader = Loader()
    data = db_loader.load_data(table_name="alarms_severities", limit=None)
    print(data.head())
