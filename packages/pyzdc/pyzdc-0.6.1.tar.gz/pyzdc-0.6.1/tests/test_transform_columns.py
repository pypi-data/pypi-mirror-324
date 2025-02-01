import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import duckdb
import pytest

from pyzdc.transform.transform_columns import ColumnTransformer


@pytest.fixture
def setup_db(tmp_path: Path) -> Path:  # type: ignore
    db_path = tmp_path / "test.db"
    conn = duckdb.connect(str(db_path))
    conn.execute("CREATE TABLE sinan (col1 VARCHAR, col2 VARCHAR)")
    conn.execute("INSERT INTO sinan VALUES ('áéíóú', 'çñ')")
    conn.close()
    return db_path


@pytest.fixture
def setup_json(tmp_path: Path) -> Path:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        json.dump({"col1": "vowels", "col2": "consonants"}, f)
    return json_path


def test_load_json_success(setup_json: Path) -> None:
    transformer = ColumnTransformer(json_path=setup_json.parent)
    result = transformer.load_json()
    assert result == {"col1": "vowels", "col2": "consonants"}


def test_load_json_file_not_found(tmp_path: Path) -> None:
    transformer = ColumnTransformer(json_path=tmp_path)
    with pytest.raises(FileNotFoundError):
        transformer.load_json()


def test_load_json_invalid_json(tmp_path: Path) -> None:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        f.write("invalid json")
    transformer = ColumnTransformer(json_path=tmp_path)
    with pytest.raises(json.JSONDecodeError):
        transformer.load_json()


def test_load_json_unexpected_error(setup_json: Path) -> None:
    transformer = ColumnTransformer(json_path=setup_json.parent)
    with patch("builtins.open", side_effect=OSError("Unexpected error")):
        with pytest.raises(OSError, match="Unexpected error"):
            transformer.load_json()


def test_rename_db_columns(setup_db: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(db_path=setup_db, json_path=setup_json.parent)
    transformer.rename_db_columns()
    conn = duckdb.connect(str(setup_db))
    result = conn.execute("DESCRIBE sinan").fetchall()
    conn.close()
    result_column_names = [row[0] for row in result]
    expected_columns = ["vowels", "consonants"]
    assert result_column_names == expected_columns


def test_rename_db_columns_db_not_found(tmp_path: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(
        db_path=tmp_path / "non_existent.db", json_path=setup_json.parent
    )
    with pytest.raises(FileNotFoundError):
        transformer.rename_db_columns()


def test_rename_db_columns_unmapped_columns(setup_db: Path, tmp_path: Path) -> None:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        json.dump({"nonexistent": "newname"}, f)

    transformer = ColumnTransformer(db_path=setup_db, json_path=tmp_path)
    with patch("logging.warning") as mock_warning:
        transformer.rename_db_columns()
        mock_warning.assert_called_with(" - nonexistent")


def test_rename_db_columns_table_not_found(setup_db: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(db_path=setup_db, json_path=setup_json.parent)
    with pytest.raises(Exception, match="Table does not exist"):
        with patch("duckdb.connect") as mock_connect:
            mock_conn = mock_connect.return_value
            mock_conn.execute.side_effect = Exception("Table does not exist")
            transformer.rename_db_columns("nonexistent_table")


def test_rename_db_columns_sql_error(setup_db: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(db_path=setup_db, json_path=setup_json.parent)
    with patch("duckdb.connect") as mock_conn:
        mock_conn.return_value.execute.side_effect = Exception("SQL logic error")
        with pytest.raises(Exception, match="SQL logic error"):
            transformer.rename_db_columns()


def test_rename_db_columns_no_matches(setup_db: Path, tmp_path: Path) -> None:
    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        json.dump({"unmatched_col": "new_name"}, f)

    transformer = ColumnTransformer(db_path=setup_db, json_path=tmp_path)
    with patch("logging.warning") as mock_warning:
        transformer.rename_db_columns()
        mock_warning.assert_any_call(
            "The following columns were not found in the JSON mapping or database "
            "and were not renamed:"
        )
        mock_warning.assert_any_call(" - unmatched_col")


def test_rename_db_columns_rollback_on_error(setup_db: Path, setup_json: Path) -> None:
    transformer = ColumnTransformer(db_path=setup_db, json_path=setup_json.parent)
    with patch("duckdb.connect") as mock_conn:
        mock_conn.return_value.execute.side_effect = Exception("Mocked error")
        mock_conn.return_value.rollback = MagicMock()

        with pytest.raises(Exception, match="Mocked error"):
            transformer.rename_db_columns()

        mock_conn.return_value.rollback.assert_called_once()


def test_rename_db_columns_no_accents(setup_db: Path, tmp_path: Path) -> None:
    conn = duckdb.connect(str(setup_db))
    conn.execute("CREATE TABLE no_accents (vowels VARCHAR, consonants VARCHAR)")
    conn.close()

    json_path = tmp_path / "columns_translated_english.json"
    with open(json_path, "w") as f:
        json.dump({}, f)  # JSON vazio para evitar erro de arquivo ausente

    transformer = ColumnTransformer(db_path=setup_db, json_path=tmp_path)
    with patch("logging.info") as mock_info:
        transformer.rename_db_columns("no_accents")
        mock_info.assert_any_call("All columns renamed successfully.")
