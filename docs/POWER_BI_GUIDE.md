# Power BI model and report guide

Power BI Desktop is Windows-only. This guide supports the Windows VM workflow; it is not a claim that a PBIX file has already been created.

## Load and model
1. Run the Python pipeline, then import fact_readmission.csv, dim_patient.csv, dim_hospital.csv and dim_date.csv using Home > Get Data > Text/CSV.
2. In Power Query keep identifiers as Text, date fields as Date, readmission_30d as Whole Number and total_cost as Decimal Number.
3. Create one-to-many, single-direction relationships from each dimension key to the corresponding fact foreign key.
4. Select the date table and use Table tools > Mark as date table.
5. Hide technical keys from report view.

## DAX
```DAX
Total Inpatient Encounters = COUNTROWS(FactReadmission)
30-Day Readmissions = SUM(FactReadmission[readmission_30d])
30-Day Readmission Rate = DIVIDE([30-Day Readmissions], [Total Inpatient Encounters], 0)
Average Length of Stay = AVERAGE(FactReadmission[length_of_stay_days])
Unique Patients = DISTINCTCOUNT(FactReadmission[patient_id])
```

## Three report pages
- Overview: four KPI cards, monthly trend, monthly volume and date/region/age slicers.
- Region and Patient Groups: regional rate, age-band rate, region-age matrix.
- Readmission Patterns: reason category, length-of-stay band, index-to-next-admission detail.

Display denominators alongside rates. These are descriptive synthetic-data measures, not clinical decisions.
