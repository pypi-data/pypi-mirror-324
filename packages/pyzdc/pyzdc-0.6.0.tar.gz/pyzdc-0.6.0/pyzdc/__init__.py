"""
This module initializes the pyzdc package and exposes the main data-fetching
functions for retrieving and transforming data related to health notifications.

Available functions:
- get_notifications
- get_personal_data
- get_clinical_signs
- get_patient_diseases
- get_exams
- get_hospital_info
- get_alarm_severities
- get_sinan_info
- get_data_from_table
- get_years
"""

from .get_info import (
    get_alarm_severities,
    get_clinical_signs,
    get_data_from_table,
    get_exams,
    get_hospital_info,
    get_notifications,
    get_patient_diseases,
    get_personal_data,
    get_sinan_info,
    get_years,
)

__all__ = [
    "get_notifications",
    "get_personal_data",
    "get_clinical_signs",
    "get_patient_diseases",
    "get_exams",
    "get_hospital_info",
    "get_alarm_severities",
    "get_sinan_info",
    "get_data_from_table",
    "get_years",
]

__version__ = "0.5.1"
__author__ = "Gutto França"
__email__ = "guttolaudie@gmail.com"
