# Patient Readmission Analysis

[![Validate project pipeline](https://github.com/jaibaranwal/patient-readmission-analysis/actions/workflows/validate.yml/badge.svg)](https://github.com/jaibaranwal/patient-readmission-analysis/actions/workflows/validate.yml)

**Student:** Jai Baranwal  
**Roll No.:** 2500321540074  
**Branch & Section:** CSE DS - A  
**Project:** HCLTech Career Shaper - Project 16  
**GitHub:** https://github.com/jaibaranwal  
**Repository:** https://github.com/jaibaranwal/patient-readmission-analysis

## About the project
I built this project to study whether an inpatient encounter is followed by another inpatient stay for the same patient within 30 days after discharge. The work covers data cleaning, readmission calculation, SQLite modelling, SQL analysis, charts, a notebook and a Streamlit dashboard interface.

## Dataset used
The current analysis uses a deterministic, project-generated synthetic dataset. It contains 120 synthetic patients, 7 synthetic hospital organisations and 435 raw encounter rows before cleaning. The generated data include a few controlled quality issues so that the cleaning and validation steps can be checked. They are not real patient records and are not the official Synthea sample.

## Preview results
- Raw encounters: 435
- Clean encounters: 432
- Eligible inpatient fact rows: 362
- 30-day readmission flags: 78
- Readmission rate: 21.55%
- Automated validation: 7/7 passed
- Separate patient-level flag checks: 20/20 passed

These figures describe only the generated academic sample. They are not hospital performance or clinical findings.

## Run the project
Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/run_pipeline.py --input data/sample
python scripts/load_sqlite.py
python scripts/run_analysis.py
python scripts/manual_verify_20.py
python tests/test_pipeline.py
streamlit run app/streamlit_app.py
```

## Project structure
- `src/` - cleaning and analysis modules
- `scripts/` - pipeline, SQLite loader, analysis, verification and report generation
- `sql/` - SQLite schema and seven business queries
- `data/sample/` - deterministic synthetic input data
- `data/clean/` - cleaned dimensions, encounters, fact tables and quality log
- `data/processed/` - query exports (the SQLite database is included in the full project ZIP)
- `notebooks/` - annotated analysis notebook
- `app/` - Streamlit dashboard
- `reports/` - report PDFs, charts, KPIs and validation outputs
- `docs/` - project documentation and Power BI/Excel guides
- `powerbi/` - DAX measures
- `submission/` - three LMS-ready files and a small upload ZIP

## Readmission definition
An index inpatient encounter is flagged when the same patient has a subsequent inpatient encounter starting strictly after its discharge date and no later than 30 calendar days after discharge. Emergency and ambulatory encounters are not counted as inpatient readmissions. This is a descriptive encounter-based measure and does not determine preventability or clinical risk.

## LMS upload files
The three LMS files are kept in `submission/`:
1. `Patient_Readmission_Project_Report.pdf` - main project report.
2. `Patient_Readmission_Dataset_Details.pdf` - dataset details and quality summary.
3. `patient_readmission_cleaned.csv` - analysis-ready inpatient fact dataset.

The full project ZIP contains the source code, data, SQL, database, notebook, charts, validation files and supporting guides.

## Notes
A Power BI model guide and DAX measures are included. A native `.pbix` file must be saved from Power BI Desktop; it is not included here. The records in this repository are synthetic and must not be used for clinical decisions.
