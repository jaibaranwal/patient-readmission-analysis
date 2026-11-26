"""Print a compact readmission summary directly from the SQLite database."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "readmission.db"
if not DB.exists():
    raise SystemExit("Database not found. Run python scripts/load_sqlite.py first.")

with sqlite3.connect(DB) as con:
    overall = con.execute(
        """SELECT COUNT(*), SUM(readmission_30d),
                  ROUND(100.0 * SUM(readmission_30d) / COUNT(*), 2),
                  ROUND(AVG(length_of_stay_days), 2)
           FROM fact_readmission"""
    ).fetchone()
    by_region = con.execute(
        """SELECT region, COUNT(*), SUM(readmission_30d),
                  ROUND(100.0 * SUM(readmission_30d) / COUNT(*), 2)
           FROM fact_readmission
           GROUP BY region
           ORDER BY 4 DESC"""
    ).fetchall()
    query_files = sorted((ROOT / "data" / "processed" / "query_results").glob("Q[1-7]_*.csv"))

print("Q1 - OVERALL READMISSION SUMMARY")
print("Inpatient encounters :", overall[0])
print("30-day readmissions  :", overall[1])
print("Readmission rate     :", f"{overall[2]:.2f}%")
print("Average stay         :", f"{overall[3]:.2f} days")
print()
print("Q3 - READMISSION RATE BY REGION")
print(f"{'Region':<14}{'Encounters':>12}{'Readmissions':>15}{'Rate':>10}")
for region, encounters, readmissions, rate in by_region:
    print(f"{region:<14}{encounters:>12}{readmissions:>15}{rate:>9.2f}%")
print()
print(f"SQL query result files found: {len(query_files)}/7")
if len(query_files) != 7:
    raise SystemExit("Expected seven query result CSV files.")
