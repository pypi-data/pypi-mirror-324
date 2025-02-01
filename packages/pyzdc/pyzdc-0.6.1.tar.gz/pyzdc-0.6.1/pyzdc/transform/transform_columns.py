import json
import logging
from pathlib import Path
from typing import Dict

import duckdb
import unidecode

from pyzdc.utils.config import DB_PATH, JSON_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ColumnTransformer:
    """
    A class to handle the transformation of column names in a DuckDB database table
    based on a JSON mapping file. It includes functionality to load the JSON mapping,
    remove accents from existing column names, and rename columns according to the
    mapping.

    Attributes:
        db_path (Path): The path to the DuckDB database file.
        json_path (Path): The path to the JSON file containing column mappings.

    Methods:
        load_json() -> Dict[str, str]: Load a JSON file containing column mappings.
        rename_db_columns(table_name: str = "sinan") -> None:
    """
    def __init__(self, db_path: Path = DB_PATH, json_path: Path = JSON_PATH):
        self.db_path = db_path
        self.json_path = json_path / "columns_translated_english.json"
    def load_json(self) -> Dict[str, str]:
        """
        Load a JSON file containing column mappings.
        """
        if not self.json_path.exists():
            logging.error(f"JSON file not found at {self.json_path}")
            raise FileNotFoundError(f"JSON file not found at {self.json_path}")

        try:
            with open(self.json_path, "r") as file:
                columns_mapping = json.load(file)
            logging.info(f"Column mapping loaded successfully from {self.json_path}.")
            return dict(columns_mapping)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while loading JSON: {e}")
            raise

    def rename_db_columns(self, table_name: str = "sinan") -> None:
        """
        Renames columns in a DuckDB table based on a JSON mapping and removes accents.
        """
        if not self.db_path.exists():
            logging.error(f"Database not found at {self.db_path}")
            raise FileNotFoundError(f"Database not found at {self.db_path}")

        column_mapping = self.load_json()

        try:
            conn = duckdb.connect(str(self.db_path))

            conn.begin()

            # Get existing columns and normalize them
            existing_columns = {
                col[0]: unidecode.unidecode(col[0])
                for col in conn.execute(f"DESCRIBE {table_name}").fetchall()
            }

            unmapped_columns = []

            # Remove accents from existing column names
            for col, normalized_col in existing_columns.items():
                if col != normalized_col:
                    conn.execute(
                        f'ALTER TABLE {table_name} RENAME COLUMN "{col}" '
                        f'TO "{normalized_col}"'
                    )
                    logging.info(
                        f"Removed accents from column '{col}' to '{normalized_col}'"
                    )

            for old_name, new_name in column_mapping.items():
                old_name = unidecode.unidecode(old_name)
                if old_name in existing_columns.values():
                    conn.execute(
                        f'ALTER TABLE {table_name} RENAME COLUMN "{old_name}" '
                        f'TO "{new_name}"'
                    )
                    logging.info(
                        f"Renamed column '{old_name}' to '{new_name}'."
                    )
                else:
                    unmapped_columns.append(old_name)

            conn.commit()
            conn.close()

            if unmapped_columns:
                logging.warning(
                    "The following columns were not found in the JSON mapping or "
                    "database "
                    "and were not renamed:"
                )
                for col in unmapped_columns:
                    logging.warning(f" - {col}")
            else:
                logging.info("All columns renamed successfully.")

        except Exception as e:
            logging.error(f"Error renaming columns in DuckDB: {e}")
            if conn: # type: ignore
                conn.rollback()
            raise
