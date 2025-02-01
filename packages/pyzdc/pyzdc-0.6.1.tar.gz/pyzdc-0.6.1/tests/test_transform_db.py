from pathlib import Path
from unittest.mock import MagicMock, patch

import duckdb
import pytest

from pyzdc.transform.transform_db import DBTransformer


@pytest.fixture
def db_path(tmp_path: Path) -> str:
    db_file = tmp_path / "test_db.duckdb"
    conn = duckdb.connect(str(db_file))
    conn.execute("""
    CREATE TABLE sinan (
      notification_type VARCHAR,
      disease_condition_id VARCHAR,
      notification_date DATE,
      notification_week INTEGER,
      notification_year INTEGER,
      notification_state_id VARCHAR,
      notification_city_id VARCHAR,
      notification_region_id VARCHAR,
      notification_health_unit_id VARCHAR,
      symptom_onset_date DATE,
      symptom_onset_week INTEGER,
      year_of_birth INTEGER,
      age INTEGER,
      gender VARCHAR,
      pregnancy_status VARCHAR,
      ethnicity VARCHAR,
      education_level VARCHAR,
      state_of_residence VARCHAR,
      city_of_residence VARCHAR,
      region_of_residence VARCHAR,
      country_of_residence VARCHAR,
      investigation_date DATE,
      occupation_or_activity_field VARCHAR,
      clinical_signs_fever BOOLEAN,
      clinical_signs_myalgia BOOLEAN,
      clinical_signs_headache BOOLEAN,
      clinical_signs_rash BOOLEAN,
      clinical_signs_vomiting BOOLEAN,
      clinical_signs_nausea BOOLEAN,
      clinical_signs_back_pain BOOLEAN,
      clinical_signs_conjunctivitis BOOLEAN,
      clinical_signs_arthritis BOOLEAN,
      clinical_signs_arthralgia BOOLEAN,
      clinical_signs_petechiae BOOLEAN,
      clinical_signs_leukopenia BOOLEAN,
      retro_orbital_pain BOOLEAN,
      diabetes BOOLEAN,
      hematological_diseases BOOLEAN,
      hepatopathies BOOLEAN,
      renal_diseases BOOLEAN,
      hypertension BOOLEAN,
      peptic_ulcer BOOLEAN,
      autoimmune_diseases BOOLEAN,
      laco_test BOOLEAN,
      if_patient_did_laco_test BOOLEAN,
      igm_chikungunya_serum_1_date DATE,
      igm_chikungunya_serum_1_result VARCHAR,
      igm_chikungunya_serum_2_date DATE,
      igm_chikungunya_serum_2_result VARCHAR,
      prnt_test_date DATE,
      prnt_test_result VARCHAR,
      serological_test_igm_dengue_date DATE,
      serological_test_igm_dengue_result VARCHAR,
      ns1_test_date DATE,
      ns1_test_result VARCHAR,
      viral_isolation_date DATE,
      viral_isolation_result VARCHAR,
      rt_pcr_date DATE,
      rt_pcr_result VARCHAR,
      serotype VARCHAR,
      histopathology_result VARCHAR,
      immunohistochemistry_result VARCHAR,
      plasmatic_value FLOAT,
      evidence VARCHAR,
      platelet_count INTEGER,
      fdh_scd_degree VARCHAR,
      hospitalization BOOLEAN,
      hospitalization_date DATE,
      state_of_the_hospital VARCHAR,
      city_of_the_hospital VARCHAR,
      autochthonous_case_of_residence BOOLEAN,
      country_of_the_infection VARCHAR,
      country_of_the_infection_id VARCHAR,
      infection_city_id VARCHAR,
      final_classification VARCHAR,
      classification_criteria VARCHAR,
      work_related_case BOOLEAN,
      clinical_classification_chikungunya VARCHAR,
      evolution_case VARCHAR,
      death_date DATE,
      case_closure_date DATE,
      hypotension_alarm BOOLEAN,
      platelet_alarm BOOLEAN,
      vomiting_alarm BOOLEAN,
      bleeding_alarm BOOLEAN,
      lethargy_alarm BOOLEAN,
      hematocrit_alarm BOOLEAN,
      abdominal_pain_alarm BOOLEAN,
      hepatomegaly_alarm BOOLEAN,
      liquid_alarm BOOLEAN,
      alarm_dengue_date DATE,
      pulse_severity VARCHAR,
      convergence_pressure_severity VARCHAR,
      capilar_enchiment_severity VARCHAR,
      respiratory_insufficiency_liquid_severity VARCHAR,
      tachycardia_severity VARCHAR,
      extremity_coldness_severity VARCHAR,
      hypotension_severity VARCHAR,
      hematemesis_severity VARCHAR,
      melena_severity VARCHAR,
      metrorrhagia_severity VARCHAR,
      bleeding_severity VARCHAR,
      higher_ast_alt_severity VARCHAR,
      myocarditis_severity VARCHAR,
      consciousness_severity VARCHAR,
      other_organs_severity VARCHAR,
      severity_date DATE,
      hemorrhaegic_manifestations BOOLEAN,
      epistaxis BOOLEAN,
      gengival_bleeding BOOLEAN,
      metrorrhagia BOOLEAN,
      petechiae BOOLEAN,
      hematuria BOOLEAN,
      bleeding BOOLEAN,
      complications VARCHAR,
      lot_number VARCHAR,
      system_type VARCHAR,
      duplicated_number VARCHAR,
      typing_date DATE,
      record_enabled_send BOOLEAN,
      computer_id VARCHAR,
      windows_migration BOOLEAN
    );
  """)
    conn.close()
    return str(db_file)


def test_transform_db(db_path: str) -> None:
    from pathlib import Path

    transformer = DBTransformer(db_path=Path(db_path))
    transformer.transform_db()

    conn = duckdb.connect(str(db_path))
    tables = conn.execute("SHOW TABLES").fetchall()
    table_names = [table[0] for table in tables]

    expected_tables = [
        "notifications_info",
        "personal_data",
        "clinical_signs",
        "patient_diseases",
        "exams",
        "hospital_info",
        "alarms_severities",
        "sinan_internal_info",
    ]

    for table in expected_tables:
        assert table in table_names

    assert "sinan" not in table_names

    conn.close()


def test_transform_db_missing_db(tmp_path: Path) -> None:
    missing_db_path = tmp_path / "missing_db.duckdb"
    transformer = DBTransformer(db_path=missing_db_path)

    with pytest.raises(Exception, match="Table with name sinan does not exist"):
        transformer.transform_db()


def test_transform_db_remove_original_table(db_path: str) -> None:
    transformer = DBTransformer(db_path=Path(db_path))
    transformer.transform_db()

    conn = duckdb.connect(str(db_path))
    tables = conn.execute("SHOW TABLES").fetchall()
    table_names = [table[0] for table in tables]

    assert "sinan" not in table_names
    conn.close()


def test_transform_db_query_failure(db_path: str) -> None:
    transformer = DBTransformer(db_path=Path(db_path))

    with patch("duckdb.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.execute.side_effect = Exception("Query failed")

        with pytest.raises(Exception, match="Query failed"):
            transformer.transform_db()

        mock_conn.rollback.assert_called_once()


def test_transform_db_empty_db(tmp_path: Path) -> None:
    empty_db_path = tmp_path / "empty_db.duckdb"
    conn = duckdb.connect(str(empty_db_path))
    conn.close()

    transformer = DBTransformer(db_path=empty_db_path)

    with pytest.raises(Exception, match="Table with name sinan does not exist"):
        transformer.transform_db()


def test_transform_db_rollback_on_failure(db_path: str) -> None:
    transformer = DBTransformer(db_path=Path(db_path))

    with patch("duckdb.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn

        mock_conn.execute.side_effect = [None, Exception("Query failed")]

        with pytest.raises(Exception, match="Query failed"):
            transformer.transform_db()

        mock_conn.rollback.assert_called_once()
