import logging
import os
import shutil
from pathlib import Path
from typing import Union

import duckdb
import pandas as pd
from pysus.ftp.databases.sinan import SINAN  # type: ignore

from pyzdc.utils.config import DB_PATH, PARQUET_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Extractor:
    """
    A class used to extract data for specific diseases and insert it into a DuckDB
    database.

    Attributes:

    Methods:
        extract_parquet(disease: str, years: Union[int, list[int]]) -> list[Path]:

        insert_parquet_to_duck(files: list[Path]) -> None:
    """

    def __init__(self, db_path: Path = DB_PATH, parquet_path: Path = PARQUET_PATH):
        """
        Initialize the Extractor with paths for the DuckDB database and Parquet files.

        Parameters:
            db_path (Path): Path to the DuckDB database file.
            parquet_path (Path): Path to the directory for storing Parquet files.
        """
        self.db_path = db_path
        self.parquet_path = parquet_path

        if not self.db_path.exists():
            logging.info(f"Ensuring the database path exists: {self.db_path}")
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.db_path.touch(exist_ok=True)
            logging.info(f"Database file created at {self.db_path}")

    def extract_parquet(self, disease: str, years: Union[int, list[int]]) -> list[Path]:
        """
        Extracts parquet files for a given disease and years.

        Parameters:
            disease (str): The disease to extract data for. Must be one of
                ["ZIKA", "CHIK", "DENG"].
            years (Union[int, list[int]]): The year or list of years to
                extract data for.

        Returns:
            list[Path]: A list of Paths to the extracted parquet files.

        Raises:
            ValueError: If an invalid disease is provided.
        """
        valid_diseases = ["ZIKA", "CHIK", "DENG"]
        if disease not in valid_diseases:
            logging.error(
                f"Invalid disease '{disease}' provided. Only {valid_diseases} "
                "are supported."
            )
            raise ValueError(
                f"Invalid disease '{disease}'. Please use one of the following: "
                f"{valid_diseases}"
            )

        if isinstance(years, int):
            years = [years]

        file_paths = []
        for year in years:
            year_suffix = str(year)[2:]
            file_name = self.parquet_path / f"{disease}BR{year_suffix}.parquet"

            if not file_name.exists():
                sinan = SINAN().load()
                file = sinan.get_files(disease, year)
                sinan.download(file, local_dir=str(self.parquet_path))
                logging.info(f"File saved in {file_name}")

            file_paths.append(file_name)

        pysus_dir = Path.home() / "pysus"
        if pysus_dir.exists() and pysus_dir.is_dir():
            try:
                shutil.rmtree(pysus_dir)
                logging.info(f"Removed directory {pysus_dir}")
            except Exception as e:
                logging.error(f"Error removing directory {pysus_dir}: {e}")

        return file_paths

    def insert_parquet_to_duck(self, files: list[Path]) -> None:
        """
        Inserts data from a list of Parquet files into a DuckDB database.

        Parameters:
            files (list[Path]): A list of Path objects pointing to the Parquet files
                to be inserted.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the database operations,
            it logs the error and closes the connection.
        """
        duck_path = self.db_path
        if not duck_path.parent.exists():
            logging.info(f"Directory {duck_path.parent} does not exist. Creating it.")
            duck_path.parent.mkdir(parents=True, exist_ok=True)

        if duck_path.exists():
            logging.info(
                f"Database already exists at {duck_path}, it will be overwritten."
            )
            os.remove(duck_path)

        conn = None

        try:
            conn = duckdb.connect(str(duck_path))

            for i, file in enumerate(files):
                logging.info(f"Inserting data from {file} into the database.")
                data = pd.read_parquet(file)

                conn.register("temp_table", data)

                if i == 0:
                    conn.execute("CREATE TABLE sinan AS SELECT * FROM temp_table")
                else:
                    conn.execute("INSERT INTO sinan SELECT * FROM temp_table")

                conn.unregister("temp_table")
                del data

            conn.close()
            logging.info("All data inserted into the database successfully.")
        except Exception as e:
            logging.error(f"Error: {e}")
            if conn:
                conn.close()


if __name__ == "__main__":
    extractor = Extractor()
    years = [2022, 2023]
    files = extractor.extract_parquet("CHIK", years)
    extractor.insert_parquet_to_duck(files)
