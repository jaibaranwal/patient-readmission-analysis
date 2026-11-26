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

# Run the complete validation sequence in one command (Mac/Linux)
./scripts/run_submission_evidence.sh
```

## What is in this repository
- `src/` - cleaning, region mapping and analysis modules
- `scripts/` - pipeline, SQLite loader, analysis, SQL summary and verification
- `sql/` - SQLite schema and seven business queries
- `data/sample/` - compact deterministic synthetic input for a repeatable smoke test
- `app/` - Streamlit dashboard source
- `docs/` - problem statement, data dictionary, dataset notes, SRS and Power BI/Excel guides
- `powerbi/` - DAX measures
- `tests/` - pipeline acceptance checks
- `.github/workflows/` - GitHub Actions pipeline validation

## Readmission definition
An index inpatient encounter is flagged when the same patient has a subsequent inpatient encounter starting strictly after its discharge date and no later than 30 calendar days after discharge. Emergency and ambulatory encounters are not counted as inpatient readmissions. This is a descriptive encounter-based measure and does not determine preventability or clinical risk.

## Full project and LMS files
The accompanying **Patient_Readmission_Analysis_Final_Submission.zip** is the complete assessment package. Its `submission/` folder contains:
1. `Patient_Readmission_Project_Report.pdf` - main project report.
2. `Patient_Readmission_Dataset_Details.pdf` - dataset details and quality summary.
3. `patient_readmission_cleaned.csv` - analysis-ready inpatient fact dataset.

The complete ZIP also contains the annotated notebook, extended synthetic fixture, cleaned data, SQLite database, seven query result CSVs, four charts, KPI outputs, validation files, final PDFs and supporting guides. These generated deliverables are kept in the full package; the GitHub repository is the code and documentation home.

## Notes
A Power BI model guide and DAX measures are included. A native `.pbix` file must be saved from Power BI Desktop; it is not included here. The records in this repository are synthetic and must not be used for clinical decisions.
