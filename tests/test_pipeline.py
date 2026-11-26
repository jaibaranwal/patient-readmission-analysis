"""Acceptance checks for the cleaned fact table and SQLite database."""
from pathlib import Path
import sqlite3, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
fact=pd.read_csv(ROOT/"data/clean/fact_readmission.csv")
con=sqlite3.connect(ROOT/"data/processed/readmission.db")
checks=[]
def check(name, ok, detail): checks.append((name, bool(ok), detail))
check("Unique encounter keys", fact.encounter_id.is_unique, f"rows={len(fact)}")
check("Required fields present", fact[["encounter_id","patient_id","start_date","discharge_date"]].notna().all().all(), "required fact values")
check("Readmission flag in range", fact.readmission_30d.isin([0,1]).all(), "allowed values are 0 and 1")
py=int(fact.readmission_30d.sum()); sql=int(con.execute("SELECT SUM(readmission_30d) FROM fact_readmission").fetchone()[0])
check("Python and SQLite totals match", py==sql, f"Python={py}; SQLite={sql}")
check("Foreign keys valid", len(con.execute("PRAGMA foreign_key_check").fetchall())==0, "SQLite foreign_key_check")
con.close()
for name,ok,detail in checks: print(("PASS" if ok else "FAIL")+": "+name+" - "+detail)
out=ROOT/"reports"; out.mkdir(exist_ok=True)
pd.DataFrame([{"test_case":n,"status":"PASS" if ok else "FAIL","detail":d} for n,ok,d in checks]).to_csv(out/"test_results.csv",index=False)
raise SystemExit(0 if all(x[1] for x in checks) else 1)
