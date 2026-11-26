# Entity relationship model

The model uses a star schema with `fact_readmission` at one row per completed inpatient encounter.

- `dim_patient.patient_id` 1-to-many `fact_readmission.patient_id`
- `dim_hospital.hospital_id` 1-to-many `fact_readmission.hospital_id`
- `dim_date.date_key` 1-to-many `fact_readmission.date_key`

The fact table stores encounter dates, length of stay, a 0/1 30-day readmission flag, next inpatient encounter details, age band, reason, region and cost. Keys are text to preserve identifiers.
