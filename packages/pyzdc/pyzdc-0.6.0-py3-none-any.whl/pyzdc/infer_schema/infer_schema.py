import logging
from pathlib import Path
import warnings
import pandas as pd
import pandera as pa
from pysus.ftp.databases.sinan import SINAN # type: ignore
from pyzdc.utils.config import RAW_DATA_PATH, SCHEMA_PATH

warnings.filterwarnings("ignore", category=SyntaxWarning, module="stringcase")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_to_infer_schema(
    disease: str, year: int, file_path: Path = RAW_DATA_PATH
) -> pd.DataFrame:
    """
    Extract data for a specific disease and year, saving it in Parquet format
    if not already present.

    Args:
        disease (str): The name of the disease (e.g., "CHIK", "DENG", "ZIKA").
        year (int): The year of the data to extract.
        file_path (Path): The path to save the raw data files.
            Defaults to RAW_DATA_PATH.

    Returns:
        pd.DataFrame: The extracted data as a Pandas DataFrame.

    Raises:
        ValueError: If the disease or year is invalid.
        Exception: If any unexpected error occurs during the data extraction process.
    """
    year_str = str(year)[2:]
    file_name = file_path / f"{disease}BR{year_str}.parquet"

    if file_name.exists():
        logging.info(f"File located in {file_name} already exists. Loading file.")
        data = pd.read_parquet(file_name)
        return data

    try:
        sinan = SINAN().load()
        file = sinan.get_files(disease, year)
        sinan.download(file, local_dir=str(file_path))
        logging.info(f"File saved in {file_name}.")
        data = pd.read_parquet(file_name)
        return data
    except Exception as e:
        logging.error(f"Error extracting data for {disease} in {year}: {e}")
        raise


def infer_and_save_schema(
    data: pd.DataFrame,
    schema_name: str,
    schema_path: Path = SCHEMA_PATH
) -> None:
    """
    Infers a schema from a Pandas DataFrame using Pandera and saves it as a
    Python script.

    Args:
        data (pd.DataFrame): The data to infer the schema from.
        schema_name (str): The name of the schema file (without extension).
        schema_path (Path): The path to save the schema file. Defaults to SCHEMA_PATH.

    Returns:
        None

    Raises:
        Exception: If any unexpected error occurs during schema inference or saving.
    """
    try:
        schema = pa.infer_schema(data)
        schema_file = schema_path / f"{schema_name}.py"
        with open(schema_file, "w", encoding="utf-8") as file:
            file.write(schema.to_script())  # type: ignore
        logging.info(f"Schema inferred and saved to {schema_file}.")
    except Exception as e:
        logging.error(f"Error inferring or saving schema: {e}")
        raise


if __name__ == "__main__":
    disease = "CHIK"
    year = 2023

    logging.info(f"Extracting data for disease: {disease}, year: {year}.")
    data = extract_to_infer_schema(disease, year)

    logging.info(f"Inferring schema for disease: {disease}.")
    infer_and_save_schema(data, schema_name=f"{disease}_schema")
