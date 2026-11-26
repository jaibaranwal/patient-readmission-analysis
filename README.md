# Patient Readmission Analysis

**Project 16 · Individual Data Analytics Project**

**Prepared by:** Jai Baranwal  
**GitHub:** [@jaibaranwal](https://github.com/jaibaranwal)  
**Repository:** https://github.com/jaibaranwal/patient-readmission-analysis

## Project overview
This project studies whether a completed inpatient encounter is followed by another inpatient encounter for the same synthetic patient within 30 days after discharge. It combines Python/pandas data cleaning, a SQLite star schema, seven analytical SQL queries, descriptive KPIs, four charts, a Streamlit dashboard and Power BI/Excel implementation guides.

## Quick run from this repository
Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/run_pipeline.py --input data/sample
python scripts/load_sqlite.py
python scripts/run_analysis.py
python tests/test_pipeline.py
streamlit run app/streamlit_app.py
```

The committed GitHub sample is a compact, project-generated synthetic smoke-test fixture (12 encounter rows, including inpatient and ambulatory records). It is not actual patient data and is not the same as the larger fixture used for the full report.

## Larger submission-package preview
The full submission ZIP supplied with this project was run against a larger deterministic project-generated fixture:
- Raw encounters: 435
- Clean encounters: 432
- Eligible inpatient encounters: 362
- 30-day readmissions: 78
- Preview readmission rate: 21.55%
- Synthetic patients: 120
- SQL query exports: 7
- Automated checks: 7/7 PASS
- Independent scripted patient-case comparisons: 20/20 PASS
- SQLite foreign-key violations: 0

Those are software-validation results from synthetic records, not hospital performance or clinical findings. The GitHub quick-run fixture will produce different totals.

## Repository structure
- `src/` reusable cleaning and analysis modules
- `scripts/` pipeline runner, SQLite loader and analysis runner
- `sql/` SQLite schema and seven business queries
- `app/` Streamlit dashboard
- `data/sample/` compact synthetic smoke-test fixture
- `docs/` problem statement, synopsis, SRS, data dictionary, source notes and BI guides

The full submission package additionally contains the annotated Jupyter notebook, detailed data dictionary, Oracle reference SQL, ER diagram, full preview fixture, cleaned CSVs, SQLite database, result exports, KPI JSON, four PNG charts, validation files, final report PDF and synopsis PDF.

## Readmission rule
An index inpatient encounter is flagged when the same patient has a subsequent inpatient encounter starting 1–30 calendar days after its discharge date. Emergency and ambulatory encounters are not counted as inpatient readmissions. This is a descriptive encounter-based rule, not a causal or clinical-risk measure.

## Dataset and limitations
The included records are synthetic. They are not the official Synthea 1K CSV sample or real patient records. The full package includes source notes and a downloader for the official Synthea synthetic sample. Synthetic results cannot support diagnosis, treatment, risk scoring, preventability or hospital-performance claims.

Power BI Desktop is a Windows application. Model relationships, DAX and a three-page report layout are documented; an actual PBIX must be saved from Power BI Desktop.

## Source citation
Walonoski et al. (2018), *Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record*, Journal of the American Medical Informatics Association, 25(3), 230–238. https://doi.org/10.1093/jamia/ocx079
