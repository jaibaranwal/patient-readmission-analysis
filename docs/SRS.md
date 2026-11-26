# Software Requirements Specification

## Purpose
Provide a repeatable workflow to clean encounter data, derive a 30-day inpatient readmission flag and explore descriptive patterns.

## Users
Students and analysts reviewing synthetic encounter data for an educational project.

## Functional requirements
- Read patient, organization and encounter CSV files.
- Standardise identifiers, dates and key categorical fields.
- Log row counts affected by data-quality rules.
- Retain a clean encounter output and derive completed inpatient facts.
- Mark a readmission when the next same-patient inpatient encounter starts 1-30 days after discharge.
- Load dimension and fact tables into SQLite.
- Run seven documented SQL queries and export result CSVs.
- Calculate KPIs and charts and provide a filterable Streamlit dashboard.
- Validate key uniqueness, required fields, ranges, foreign keys and Python/SQL totals.

## Non-functional requirements
- Use Python 3.10 or later.
- Keep data processing reproducible and scripts executable from the repository root.
- Store identifiers as text.
- Document source provenance and synthetic-data limitations.
- Do not use the measures for diagnosis, treatment or clinical risk assessment.

## Acceptance criteria
The pipeline completes on the supplied synthetic CSV sample, SQLite tables load without foreign-key violations, query exports are created, and automated validation reports PASS/FAIL for the core checks.
