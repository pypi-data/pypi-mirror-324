from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from pyzdc.extract.get_raw import Extractor


@pytest.fixture
def extractor() -> Extractor:
    return Extractor(
        db_path=Path("/tmp/test_db.duckdb"), parquet_path=Path("/tmp/parquet")
    )


def test_invalid_disease(extractor: Extractor) -> None:
    with pytest.raises(ValueError):
        extractor.extract_parquet("INVALID", 2022)


@patch("pyzdc.extract.get_raw.pd.read_parquet")
@patch("pyzdc.extract.get_raw.duckdb.connect")
def test_insert_parquet_to_duck(
    mock_connect: MagicMock, mock_read_parquet: MagicMock, extractor: Extractor
) -> None:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_read_parquet.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    files = [Path("/tmp/parquet/CHIKBR22.parquet")]
    extractor.insert_parquet_to_duck(files)

    mock_connect.assert_called_once_with("/tmp/test_db.duckdb")
    mock_conn.register.assert_called_once_with(
        "temp_table", mock_read_parquet.return_value
    )
    mock_conn.execute.assert_any_call("CREATE TABLE sinan AS SELECT * FROM temp_table")
    mock_conn.unregister.assert_called_once_with("temp_table")
    mock_conn.close.assert_called_once()


@patch("pyzdc.extract.get_raw.shutil.rmtree")
@patch("pyzdc.extract.get_raw.SINAN")
def test_extract_parquet_pysus_removal_error(
    mock_sinan: MagicMock, mock_rmtree: MagicMock, extractor: Extractor
) -> None:
    mock_rmtree.side_effect = OSError("Permission denied")
    mock_sinan_instance = MagicMock()
    mock_sinan.return_value = mock_sinan_instance
    mock_sinan_instance.load.return_value = mock_sinan_instance
    mock_sinan_instance.get_files.return_value = "mock_file"
    mock_sinan_instance.download.return_value = None

    pysus_path = Path.home() / "pysus"
    with patch(
        "pathlib.Path.exists", side_effect=lambda: pysus_path == Path.home() / "pysus"
    ):
        extractor.extract_parquet("ZIKA", 2023)

    mock_rmtree.assert_called_once_with(pysus_path)


@patch("pyzdc.extract.get_raw.os.remove")
@patch("pyzdc.extract.get_raw.duckdb.connect")
@patch("pyzdc.extract.get_raw.pd.read_parquet")
def test_insert_parquet_to_duck_overwrite_db(
    mock_read_parquet: MagicMock,
    mock_connect: MagicMock,
    mock_remove: MagicMock,
    extractor: Extractor,
) -> None:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_read_parquet.return_value = pd.DataFrame({"col1": [1], "col2": [2]})

    with patch("pathlib.Path.exists", return_value=True):
        extractor.insert_parquet_to_duck([Path("/tmp/parquet/DENG.parquet")])

    mock_remove.assert_called_once_with(Path("/tmp/test_db.duckdb"))
    mock_connect.assert_called_once_with("/tmp/test_db.duckdb")
    mock_conn.close.assert_called_once()


@patch("pyzdc.extract.get_raw.Path.exists", side_effect=[False, False, True])
@patch("pyzdc.extract.get_raw.shutil.rmtree")
@patch("pyzdc.extract.get_raw.SINAN")
def test_extract_parquet_multiple_years(
    mock_sinan: MagicMock,
    mock_rmtree: MagicMock,
    mock_exists: MagicMock,
    extractor: Extractor,
) -> None:
    mock_sinan_instance = MagicMock()
    mock_sinan.return_value = mock_sinan_instance
    mock_sinan_instance.load.return_value = mock_sinan_instance
    mock_sinan_instance.get_files.return_value = "mock_file"
    mock_sinan_instance.download.return_value = None

    files = extractor.extract_parquet("CHIK", [2022, 2023])

    assert len(files) == 2
    assert files[0].name == "CHIKBR22.parquet"
    assert files[1].name == "CHIKBR23.parquet"
    mock_rmtree.assert_called_once_with(Path.home() / "pysus")


@patch("pyzdc.extract.get_raw.SINAN")
def test_extract_parquet_download_error(
    mock_sinan: MagicMock, extractor: Extractor
) -> None:
    mock_sinan_instance = MagicMock()
    mock_sinan.return_value = mock_sinan_instance
    mock_sinan_instance.load.return_value = mock_sinan_instance
    mock_sinan_instance.download.side_effect = Exception("Download failed")

    with pytest.raises(Exception, match="Download failed"):
        extractor.extract_parquet("DENG", 2023)


@patch("pyzdc.extract.get_raw.os.remove")
@patch("pyzdc.extract.get_raw.duckdb.connect")
@patch("pyzdc.extract.get_raw.Path.mkdir")
def test_insert_parquet_to_duck_create_db_dir(
    mock_mkdir: MagicMock,
    mock_connect: MagicMock,
    mock_remove: MagicMock,
    extractor: Extractor,
) -> None:
    with patch("pathlib.Path.exists", side_effect=[False, True, True]):
        extractor.insert_parquet_to_duck([Path("/tmp/parquet/DENG.parquet")])

    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_remove.assert_called_once_with(Path("/tmp/test_db.duckdb"))
    mock_connect.assert_called_once()


@patch("pyzdc.extract.get_raw.SINAN")
def test_extract_parquet_existing_file(
    mock_sinan: MagicMock, extractor: Extractor
) -> None:
    with patch("pathlib.Path.exists", return_value=True):
        files = extractor.extract_parquet("ZIKA", 2023)

    assert len(files) == 1
    assert files[0].name == "ZIKABR23.parquet"
    mock_sinan.assert_not_called()
