#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="${PYTHON_BIN:-python3}"

printf '\n=== Patient Readmission Analysis: submission verification ===\n'
printf 'Project folder: %s\n' "$ROOT"

printf '\n[1/6] Cleaning the sample data and building the fact table\n'
"$PYTHON_BIN" scripts/run_pipeline.py --input data/sample

printf '\n[2/6] Loading the SQLite database and exporting SQL query results\n'
"$PYTHON_BIN" scripts/load_sqlite.py

printf '\n[3/6] Calculating KPIs and creating charts\n'
"$PYTHON_BIN" scripts/run_analysis.py

printf '\n[4/6] Checking SQL summary totals and regional rates\n'
"$PYTHON_BIN" scripts/sql_summary.py

printf '\n[5/6] Independently checking 20 patient readmission cases\n'
"$PYTHON_BIN" scripts/manual_verify_20.py

printf '\n[6/6] Running the automated acceptance tests\n'
"$PYTHON_BIN" tests/test_pipeline.py

printf '\n=== Verification finished successfully ===\n'
printf 'See reports/kpis.json, reports/test_results.csv and reports/manual_verification_20.csv\n'
