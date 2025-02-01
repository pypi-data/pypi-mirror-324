import logging
from pathlib import Path

import duckdb

from pyzdc.utils.config import DB_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DBTransformer:
    """
    A class used to transform a database by creating new tables with normalized
    structures

    Attributes
    ----------
    db_path : Path
        The path to the database file.

    Methods
    -------
    transform_db()
    """
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def transform_db(self) -> None:
        """
        Transforms the database by creating new tables with normalized structures
        and dropping the original raw table.
        """
        create_tables_queries = [
            """
        CREATE TABLE sinan_id AS
        SELECT row_number() OVER () AS notification_id, *
        FROM sinan;

        DROP TABLE sinan;

        ALTER TABLE sinan_id RENAME TO sinan;
        """,
            """
        CREATE TABLE notifications_info AS
        SELECT
            notification_id,
            notification_type,
            disease_condition_id,
            notification_date,
            notification_week,
            notification_year,
            notification_state_id,
            notification_city_id,
            notification_region_id,
            notification_health_unit_id
        FROM sinan;
        """,
            """
        CREATE TABLE personal_data AS
        SELECT
            notification_id,
            symptom_onset_date,
            symptom_onset_week,
            year_of_birth,
            age,
            gender,
            pregnancy_status,
            ethnicity,
            education_level,
            state_of_residence,
            city_of_residence,
            region_of_residence,
            country_of_residence,
            investigation_date,
            occupation_or_activity_field
        FROM sinan;
        """,
            """
        CREATE TABLE clinical_signs AS
        SELECT
            notification_id,
            clinical_signs_fever,
            clinical_signs_myalgia,
            clinical_signs_headache,
            clinical_signs_rash,
            clinical_signs_vomiting,
            clinical_signs_nausea,
            clinical_signs_back_pain,
            clinical_signs_conjunctivitis,
            clinical_signs_arthritis,
            clinical_signs_arthralgia,
            clinical_signs_petechiae,
            clinical_signs_leukopenia,
            retro_orbital_pain
        FROM sinan;
        """,
            """
        CREATE TABLE patient_diseases AS
        SELECT
            notification_id,
            diabetes,
            hematological_diseases,
            hepatopathies,
            renal_diseases,
            hypertension,
            peptic_ulcer,
            autoimmune_diseases
        FROM sinan;
        """,
            """
        CREATE TABLE exams AS
        SELECT
            notification_id,
            laco_test,
            if_patient_did_laco_test,
            igm_chikungunya_serum_1_date,
            igm_chikungunya_serum_1_result,
            igm_chikungunya_serum_2_date,
            igm_chikungunya_serum_2_result,
            prnt_test_date,
            prnt_test_result,
            serological_test_igm_dengue_date,
            serological_test_igm_dengue_result,
            ns1_test_date,
            ns1_test_result,
            viral_isolation_date,
            viral_isolation_result,
            rt_pcr_date,
            rt_pcr_result,
            serotype,
            histopathology_result,
            immunohistochemistry_result,
            plasmatic_value,
            evidence,
            platelet_count,
            fdh_scd_degree
        FROM sinan;
        """,
            """
        CREATE TABLE hospital_info AS
        SELECT
            notification_id,
            hospitalization,
            hospitalization_date,
            state_of_the_hospital,
            city_of_the_hospital,
            autochthonous_case_of_residence,
            country_of_the_infection,
            country_of_the_infection_id,
            infection_city_id,
            final_classification,
            classification_criteria,
            work_related_case,
            clinical_classification_chikungunya,
            evolution_case,
            death_date,
            case_closure_date
        FROM sinan;
        """,
            """
        CREATE TABLE alarms_severities AS
        SELECT
            notification_id,
            hypotension_alarm,
            platelet_alarm,
            vomiting_alarm,
            bleeding_alarm,
            lethargy_alarm,
            hematocrit_alarm,
            abdominal_pain_alarm,
            lethargy_alarm,
            hepatomegaly_alarm,
            liquid_alarm,
            alarm_dengue_date,
            pulse_severity,
            convergence_pressure_severity,
            capilar_enchiment_severity,
            respiratory_insufficiency_liquid_severity,
            tachycardia_severity,
            extremity_coldness_severity,
            hypotension_severity,
            hematemesis_severity,
            melena_severity,
            metrorrhagia_severity,
            bleeding_severity,
            higher_ast_alt_severity,
            myocarditis_severity,
            consciousness_severity,
            other_organs_severity,
            severity_date,
            hemorrhaegic_manifestations,
            epistaxis,
            gengival_bleeding,
            metrorrhagia,
            petechiae,
            hematuria,
            bleeding,
            complications
        FROM sinan;
        """,
            """
        CREATE TABLE sinan_internal_info AS
        SELECT
            notification_id,
            lot_number,
            system_type,
            duplicated_number,
            typing_date,
            record_enabled_send,
            computer_id,
            windows_migration
        FROM sinan;
        """,
        ]

        conn = None
        try:
            conn = duckdb.connect(str(self.db_path))
            for query in create_tables_queries:
                conn.execute(query)

            conn.execute("DROP TABLE IF EXISTS sinan")
            conn.close()

            logging.info("Database transformed successfully!")
        except duckdb.CatalogException as ce:
            logging.error(f"Catalog Error during transformation: {ce}")
            raise ce
        except Exception as e:
            logging.error(f"Error during database transformation: {e}")
            if conn: # type: ignore
                conn.rollback()
                conn.close()
            raise
