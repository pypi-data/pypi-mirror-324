import logging
import os
import shutil
from pathlib import Path

from pyzdc.utils.config import DB_PATH, PARQUET_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Refresher:
    """
    Refresher class for delete data from a DuckDB database to deal with new data.

    Attributes:

    Methods:
        __init__(db_path: Path = DB_PATH, parquet_path: Path = PARQUET_PATH)
        delete_database() -> None:
            Delete the DuckDB database and Parquet files.
    """

    def __init__(self, db_path: Path = DB_PATH, parquet_path: Path = PARQUET_PATH):
        """
        Initialize the Loader with a database path.

        Parameters:
            db_path (Path): Path to the DuckDB database file.
            parquet_path (Path): Path to the directory for storing Parquet files.
        """
        self.db_path = db_path

        self.parquet_path = parquet_path

    def delete_database(self):
        try:
            if self.db_path.exists():
                os.remove(self.db_path)
                logging.info(f"Deleted database: {self.db_path}")

            if self.parquet_path.exists():
                if self.parquet_path.is_dir():
                    shutil.rmtree(self.parquet_path)
                    logging.info(f"Deleted directory: {self.parquet_path}")
                else:
                    os.remove(self.parquet_path)
                    logging.info(f"Deleted file: {self.parquet_path}")

        except PermissionError as e:
            logging.error(f"Permission denied while deleting files: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while deleting files: {e}")
