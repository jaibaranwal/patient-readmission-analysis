# Submission Guide

**Project:** Patient Readmission Analysis  
**Project number:** 16  
**Prepared by:** Jai Baranwal  
**GitHub:** https://github.com/jaibaranwal  
**Repository:** https://github.com/jaibaranwal/patient-readmission-analysis

## Main files
- Full project package: the ZIP provided with this project
- Final written report: `reports/FINAL_REPORT.pdf`
- Synopsis: `reports/SYNOPSIS.pdf`
- Source code: `src/`, `scripts/`, `app/`
- SQL: `sql/`
- Notebook: `notebooks/patient_readmission_analysis.ipynb`
- Charts: `reports/charts/`
- Validation: `reports/test_results.csv`, `reports/manual_verification_20.csv`

## Validation snapshot
The included extended fixture contains 435 raw encounter rows, 432 cleaned encounter rows, 362 completed inpatient fact rows and 78 30-day flags (21.55%). Seven automated checks passed. Twenty distinct patient cases were independently recomputed by a separate script and matched the pipeline output.

## Important scope note
These are results from project-generated synthetic records. They are not official Synthea sample results and are not real clinical or hospital-performance findings. The official Synthea sample has not yet been downloaded and processed in this build.

Power BI model instructions and DAX are included. A native `.pbix` must be created and saved in Power BI Desktop on Windows. HCL portal upload must be performed in the student's authenticated portal session.
