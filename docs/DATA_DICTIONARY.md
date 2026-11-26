# Data dictionary

| Table / file | Field | Description |
|---|---|---|
| dim_patient | patient_id | Synthetic patient key |
| dim_patient | birth_date | Birth date from source patient CSV |
| dim_hospital | hospital_id | Synthetic organization key |
| dim_hospital | region | Broad US region derived from organization state |
| fact_readmission | encounter_id | Unique inpatient encounter key |
| fact_readmission | patient_id | Patient dimension reference |
| fact_readmission | hospital_id | Hospital dimension reference |
| fact_readmission | date_key | Admission date key |
| fact_readmission | start_date | Inpatient encounter start date |
| fact_readmission | discharge_date | Inpatient encounter discharge date |
| fact_readmission | length_of_stay_days | Discharge minus start date in days |
| fact_readmission | readmission_30d | 1 when next inpatient start is 1-30 days after discharge; otherwise 0 |
| fact_readmission | days_to_readmission | Days from discharge to next inpatient start |
| fact_readmission | age_band | Age group at admission |
| fact_readmission | reason_category | Encounter reason description |
| fact_readmission | total_cost | Source claim cost, cleaned for invalid values |

The detailed source-to-target dictionary and example values are included in the full project submission package.
