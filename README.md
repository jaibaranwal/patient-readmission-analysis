# Patient Readmission Analysis

**Project 16 · Individual Data Analytics Project**

**Prepared by:** Jai Baranwal  
**GitHub:** [@jaibaranwal](https://github.com/jaibaranwal)  
**Repository:** https://github.com/jaibaranwal/patient-readmission-analysis

## Project overview
This project studies whether a completed inpatient encounter is followed by another inpatient encounter for the same synthetic patient within 30 days after discharge. It combines Python/pandas data cleaning, a SQLite star schema, seven analytical SQL queries, descriptive KPIs, charts, a Jupyter notebook, a Streamlit dashboard and Power BI/Excel implementation guides.

## Dataset and interpretation
The repository's bundled working data are a deterministic, project-generated synthetic fixture. They are not real patient records and are not the official Synthea 1K CSV sample. The included preview metrics validate that the pipeline works; they must not be interpreted as hospital performance or clinical findings. The official Synthea sample downloader and instructions are included for a full-source run.

## Verified preview run
- Raw encounters: 435
- Clean encounters: 432
- Eligible inpatient encounters: 362
- 30-day readmissions: 78
- Preview readmission rate: 21.55%
- Synthetic patients: 120
- SQL query exports: 7
- Automated checks: 7/7 PASS
- Independent patient-case comparisons: 20/20 PASS
- SQLite foreign-key violations: 0

## Run the project
Python 3.10+ is recommended.

\`\`\`bash
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
\`\`\`

## Repository structure
- \`src/\` reusable cleaning and analysis modules
- \`scripts/\` pipeline, database loader, downloader and validation utilities
- \`sql/\` SQLite schema and seven business queries; Oracle equivalents are also provided in the downloadable project
- \`app/\` Streamlit dashboard
- \`data/sample/\` deterministic synthetic fixture
- \`data/clean/\` cleaned tables and data-quality audit
- \`docs/\` problem statement, synopsis, SRS, data dictionary, source notes and BI guides
- \`reports/\` output charts, metrics, validation results and final report
- \`notebooks/\` annotated analysis notebook

## Readmission rule
An index inpatient encounter is flagged when the same patient has a subsequent inpatient encounter starting 1–30 calendar days after its discharge date. Emergency and ambulatory encounters are not counted as inpatient readmissions. This is a descriptive encounter-based rule, not a causal or clinical-risk measure.

## Limitations
The included preview is synthetic. Regional comparisons are derived from synthetic hospital-state values. Results do not establish preventability, care quality or clinical risk. Power BI Desktop is a Windows application; the project includes model, DAX and three-page layout instructions for the Windows workflow.

## Source citation
Walonoski et al. (2018), *Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record*, Journal of the American Medical Informatics Association, 25(3), 230–238. https://doi.org/10.1093/jamia/ocx079
