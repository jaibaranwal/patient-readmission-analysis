PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS fact_readmission;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_hospital;
DROP TABLE IF EXISTS dim_patient;
CREATE TABLE dim_patient (
  patient_id TEXT PRIMARY KEY, birth_date TEXT,
  gender TEXT NOT NULL, race TEXT NOT NULL, ethnicity TEXT NOT NULL
);
CREATE TABLE dim_hospital (
  hospital_id TEXT PRIMARY KEY, hospital_name TEXT NOT NULL,
  city TEXT, state TEXT, region TEXT NOT NULL
);
CREATE TABLE dim_date (
  date_key TEXT PRIMARY KEY, year INTEGER NOT NULL CHECK(year BETWEEN 1900 AND 2200),
  month_number INTEGER NOT NULL CHECK(month_number BETWEEN 1 AND 12),
  month_name TEXT NOT NULL, year_month TEXT NOT NULL
);
CREATE TABLE fact_readmission (
  encounter_id TEXT PRIMARY KEY, patient_id TEXT NOT NULL, hospital_id TEXT NOT NULL,
  date_key TEXT NOT NULL, start_date TEXT NOT NULL, discharge_date TEXT NOT NULL,
  length_of_stay_days INTEGER NOT NULL CHECK(length_of_stay_days >= 0),
  readmission_30d INTEGER NOT NULL CHECK(readmission_30d IN (0,1)),
  next_inpatient_encounter_id TEXT, next_inpatient_start TEXT, days_to_readmission INTEGER,
  age_at_admission REAL, age_band TEXT NOT NULL, reason_category TEXT NOT NULL,
  region TEXT NOT NULL, total_cost REAL NOT NULL CHECK(total_cost >= 0),
  FOREIGN KEY(patient_id) REFERENCES dim_patient(patient_id),
  FOREIGN KEY(hospital_id) REFERENCES dim_hospital(hospital_id),
  FOREIGN KEY(date_key) REFERENCES dim_date(date_key),
  CHECK((readmission_30d=1 AND days_to_readmission BETWEEN 1 AND 30) OR readmission_30d=0)
);
