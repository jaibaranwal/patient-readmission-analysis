"""Create descriptive KPIs and PNG charts from the cleaned encounter fact."""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
def analyse():
    fact_path = ROOT / "data/clean/fact_readmission.csv"
    df = pd.read_csv(fact_path, parse_dates=["start_date"])
    if df.empty: raise ValueError("No eligible inpatient encounters. Check the input data.")
    total = len(df); readm = int(df.readmission_30d.sum())
    kpis = {
        "dataset_mode": "project_generated_synthetic_preview",
        "total_inpatient_encounters": total,
        "readmissions_within_30_days": readm,
        "readmission_rate_pct": round(100 * readm / total, 2),
        "average_length_of_stay_days": round(float(df.length_of_stay_days.mean()), 2),
        "unique_patients": int(df.patient_id.nunique()),
        "interpretation": "Synthetic preview only; not real clinical or hospital performance data."
    }
    report = ROOT / "reports"; charts = report / "charts"; charts.mkdir(parents=True, exist_ok=True)
    (report / "kpis.json").write_text(json.dumps(kpis, indent=2), encoding="utf-8")
    monthly = df.assign(month=df.start_date.dt.to_period("M").astype(str)).groupby("month").agg(
        encounters=("encounter_id","count"), readmissions=("readmission_30d","sum")).reset_index()
    monthly["rate_pct"] = 100 * monthly.readmissions / monthly.encounters
    region = df.groupby("region").agg(encounters=("encounter_id","count"), readmissions=("readmission_30d","sum")).reset_index()
    region["rate_pct"] = 100 * region.readmissions / region.encounters
    reason = df.groupby("reason_category").agg(encounters=("encounter_id","count"), readmissions=("readmission_30d","sum")).reset_index()
    reason["rate_pct"] = 100 * reason.readmissions / reason.encounters
    stay = df.assign(stay_band=pd.cut(df.length_of_stay_days, [-1,2,5,9,1000], labels=["0-2","3-5","6-9","10+"]))
    stay = stay.groupby("stay_band", observed=False).agg(encounters=("encounter_id","count"), readmissions=("readmission_30d","sum")).reset_index()
    stay["rate_pct"] = 100 * stay.readmissions / stay.encounters
    for frame, x, title, filename in [
        (monthly,"month","Monthly inpatient activity","01_monthly_trend.png"),
        (region,"region","30-day readmission by region","02_region_readmission.png"),
        (reason,"reason_category","30-day readmission by encounter reason","03_reason_category.png"),
        (stay,"stay_band","30-day readmission by length of stay","04_problem_area_los.png")]:
        fig, ax = plt.subplots(figsize=(9,4.8))
        ax.bar(frame[x].astype(str), frame.rate_pct)
        ax.set_title(title); ax.set_xlabel(x.replace("_"," ").title()); ax.set_ylabel("Readmission rate (%)")
        ax.tick_params(axis="x", rotation=35); fig.tight_layout(); fig.savefig(charts/filename, dpi=150); plt.close(fig)
    return kpis
