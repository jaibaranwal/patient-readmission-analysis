"""Load cleaned CSV files into SQLite and export seven SQL query results."""
from pathlib import Path
import sqlite3, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; CLEAN=ROOT/"data/clean"; DB=ROOT/"data/processed/readmission.db"
DB.parent.mkdir(parents=True,exist_ok=True)
if DB.exists(): DB.unlink()
con=sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON")
con.executescript((ROOT/"sql/schema.sql").read_text())
p=pd.read_csv(CLEAN/"dim_patient.csv"); h=pd.read_csv(CLEAN/"dim_hospital.csv"); f=pd.read_csv(CLEAN/"fact_readmission.csv")
p.to_sql("dim_patient",con,index=False); h.to_sql("dim_hospital",con,index=False)
dates=pd.to_datetime(f.date_key)
d=pd.DataFrame({"date_key":f.date_key.drop_duplicates().sort_values().values})
d["year"]=pd.to_datetime(d.date_key).dt.year; d["month_number"]=pd.to_datetime(d.date_key).dt.month
d["month_name"]=pd.to_datetime(d.date_key).dt.month_name(); d["year_month"]=pd.to_datetime(d.date_key).dt.strftime("%Y-%m")
d.to_sql("dim_date",con,index=False)
f.to_sql("fact_readmission",con,index=False)
query=(ROOT/"sql/queries.sql").read_text()
import re
blocks=re.split(r"(?=-- Q[1-7]:)",query)
qdir=ROOT/"data/processed/query_results"; qdir.mkdir(parents=True,exist_ok=True)
for block in blocks:
    m=re.match(r"-- Q(\d+):\s*(.*)",block.strip())
    if not m: continue
    sql="\n".join(x for x in block.splitlines() if not x.strip().startswith("--")).strip().rstrip(";")
    pd.read_sql_query(sql,con).to_csv(qdir/f"Q{m.group(1)}.csv",index=False)
con.close()
print("SQLite database and seven query exports saved.")
