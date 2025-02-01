from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_PATH / "data"
PARQUET_PATH = DATA_PATH / "parquet"
RAW_DATA_PATH = DATA_PATH / "raw"
DB_PATH = DATA_PATH / "db" / "db.db"
JSON_PATH = DATA_PATH / "json"
SCHEMA_PATH = BASE_PATH / "schemas"
