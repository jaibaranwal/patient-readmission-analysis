-- Q1: Overall readmission KPI
SELECT COUNT(*) inpatient_encounters, SUM(readmission_30d) readmissions_30d,
 ROUND(100.0*SUM(readmission_30d)/NULLIF(COUNT(*),0),2) readmission_rate_pct
FROM fact_readmission;

-- Q2: Monthly trend
SELECT d.year_month, COUNT(*) encounters, SUM(f.readmission_30d) readmissions,
 ROUND(100.0*SUM(f.readmission_30d)/NULLIF(COUNT(*),0),2) rate_pct
FROM fact_readmission f JOIN dim_date d ON d.date_key=f.date_key
GROUP BY d.year_month ORDER BY d.year_month;

-- Q3: Region comparison
SELECT h.region, COUNT(*) encounters, SUM(f.readmission_30d) readmissions,
 ROUND(100.0*SUM(f.readmission_30d)/NULLIF(COUNT(*),0),2) rate_pct
FROM fact_readmission f JOIN dim_hospital h ON h.hospital_id=f.hospital_id
GROUP BY h.region ORDER BY rate_pct DESC;

-- Q4: Age band distribution
SELECT age_band, COUNT(*) encounters, SUM(readmission_30d) readmissions
FROM fact_readmission GROUP BY age_band ORDER BY age_band;

-- Q5: Encounter reason distribution
SELECT reason_category, COUNT(*) encounters, SUM(readmission_30d) readmissions,
 ROUND(100.0*SUM(readmission_30d)/NULLIF(COUNT(*),0),2) rate_pct
FROM fact_readmission GROUP BY reason_category ORDER BY rate_pct DESC;

-- Q6: Self-join for subsequent readmissions within 30 days
SELECT a.encounter_id index_encounter_id, a.patient_id, a.discharge_date,
 MIN(b.start_date) next_inpatient_start
FROM fact_readmission a JOIN fact_readmission b
 ON a.patient_id=b.patient_id AND b.start_date>a.discharge_date
 AND b.start_date<=date(a.discharge_date,'+30 day')
GROUP BY a.encounter_id, a.patient_id, a.discharge_date;

-- Q7: Prior discharge gap using LAG
WITH ordered AS (
 SELECT patient_id, encounter_id, start_date, discharge_date, readmission_30d,
 LAG(discharge_date) OVER(PARTITION BY patient_id ORDER BY start_date, encounter_id) prior_discharge
 FROM fact_readmission
)
SELECT CASE WHEN prior_discharge IS NULL THEN 'First observed stay'
 WHEN julianday(start_date)-julianday(prior_discharge)<=30 THEN 'Within 30 days'
 ELSE 'More than 30 days' END prior_gap_group,
 COUNT(*) encounters, SUM(readmission_30d) readmissions
FROM ordered GROUP BY prior_gap_group;
