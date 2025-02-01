from typing import Any, Dict
from unittest.mock import patch

import pandas as pd
import pytest

from pyzdc.get_info.get_info import (
    get_alarm_severities,
    get_clinical_signs,
    get_exams,
    get_hospital_info,
    get_notifications,
    get_patient_diseases,
    get_personal_data,
    get_sinan_info,
)


@pytest.fixture
def mock_extractors() -> dict:  # type: ignore
    with (
        patch("pyzdc.get_info.get_info.Extractor") as MockExtractor,
        patch("pyzdc.get_info.get_info.ColumnTransformer") as MockColumnTransformer,
        patch("pyzdc.get_info.get_info.DBTransformer") as MockDBTransformer,
        patch("pyzdc.get_info.get_info.Loader") as MockLoader,
    ):
        mock_extractor = MockExtractor.return_value
        mock_column_transformer = MockColumnTransformer.return_value
        mock_db_transformer = MockDBTransformer.return_value
        mock_loader = MockLoader.return_value

        mock_extractor.extract_parquet.return_value = ["file1.parquet", "file2.parquet"]
        mock_loader.load_data.return_value = pd.DataFrame(
            {"col1": [1, 2], "col2": [3, 4]}
        )

        yield {
            "extractor": mock_extractor,
            "column_transformer": mock_column_transformer,
            "db_transformer": mock_db_transformer,
            "loader": mock_loader,
        }  # type: ignore


def test_get_notifications(mock_extractors: Dict[str, Any]) -> None:
    data = get_notifications()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_personal_data(mock_extractors: Dict[str, Any]) -> None:
    data = get_personal_data()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_clinical_signs(mock_extractors: Dict[str, Any]) -> None:
    data = get_clinical_signs()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_patient_diseases(mock_extractors: Dict[str, Any]) -> None:
    data = get_patient_diseases()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_exams(mock_extractors: Dict[str, Any]) -> None:
    data = get_exams()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_hospital_info(mock_extractors: Dict[str, Any]) -> None:
    data = get_hospital_info()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_alarm_severities(mock_extractors: Dict[str, Any]) -> None:
    data = get_alarm_severities()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]


def test_get_sinan_info(mock_extractors: Dict[str, Any]) -> None:
    data = get_sinan_info()
    assert not data.empty
    assert list(data.columns) == ["col1", "col2"]
