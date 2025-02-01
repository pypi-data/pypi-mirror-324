import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import duckdb
import pandas as pd
import pytest

from pyzdc.load.show_data import Loader


@pytest.fixture
def loader() -> Loader:  # type: ignore
    temp_path = Path(tempfile.mktemp(suffix=".duckdb"))
    conn = duckdb.connect(str(temp_path))
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})  # noqa: F841
    conn.execute("CREATE TABLE sinan AS SELECT * FROM df")
    conn.close()
    yield Loader(db_path=temp_path)  # type: ignore
    temp_path.unlink()


def test_validate_db_path_exists(loader: Loader) -> None:
    with patch.object(Path, "exists", return_value=True):
        loader._validate_db_path()


def test_validate_db_path_not_exists(loader: Loader) -> None:
    with patch.object(Path, "exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            loader._validate_db_path()


def test_load_data(loader: Loader) -> None:
    result = loader.load_data(table_name="sinan", limit=10)
    assert not result.empty
    assert len(result) == 2
    assert "col1" in result.columns
    assert "col2" in result.columns


def test_load_data_no_limit(loader: Loader) -> None:
    result = loader.load_data(table_name="sinan")
    assert not result.empty
    assert len(result) == 2
    assert "col1" in result.columns
    assert "col2" in result.columns


@patch("pyzdc.load.show_data.duckdb.connect")
def test_load_data_exception(mock_connect: MagicMock, loader: Loader) -> None:
    mock_connect.side_effect = Exception("Connection error")

    with pytest.raises(Exception, match="Connection error"):
        loader.load_data(table_name="sinan")
