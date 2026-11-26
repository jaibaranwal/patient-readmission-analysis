"""Cleaning and 30-day inpatient readmission feature engineering."""
from pathlib import Path
import pandas as pd
from .regions import region_for_state

def _col(frame, *names):
    lookup = {str(c).strip().lower(): c for c in frame.columns}
    for name in names:
        if name.lower() in lookup:
            return lookup[name.lower()]
    return None

def load_sources(folder):
    folder = Path(folder)
    found = {p.name.lower(): p for p in folder.rglob("*.csv")}
    required = ["patients.csv", "organizations.csv", "encounters.csv"]
    missing = [n for n in required if n not in found]
    if missing:
        raise FileNotFoundError("Missing input CSV(s): " + ", ".join(missing))
    return {n[:-4]: pd.read_csv(found[n], dtype=str) for n in required}

def prepare(folder, out_dir):
    raw = load_sources(folder)
    p, o, e = (raw["patients"].copy(), raw["organizations"].copy(), raw["encounters"].copy())
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    log = []
    def record(issue, rule, n): log.append({"issue": issue, "rule_applied": rule, "rows_affected": int(n)})

    # Standardise source fields while retaining source identifiers as text.
    p = p.rename(columns={_col(p,"Id"): "patient_id", _col(p,"BIRTHDATE"): "birth_date"})
    o = o.rename(columns={_col(o,"Id"): "hospital_id", _col(o,"NAME"): "hospital_name",
                          _col(o,"CITY"): "city", _col(o,"STATE"): "state"})
    e = e.rename(columns={_col(e,"Id"): "encounter_id", _col(e,"Patient"): "patient_id",
                          _col(e,"Organization"): "hospital_id", _col(e,"Start"): "start_date",
                          _col(e,"Stop"): "discharge_date", _col(e,"EncounterClass"): "encounter_class",
                          _col(e,"ReasonDescription"): "reason_category",
                          _col(e,"Total_Claim_Cost"): "total_cost"})
    for frame, col in [(p,"patient_id"),(o,"hospital_id"),(e,"encounter_id"),(e,"patient_id"),(e,"hospital_id")]:
        if col not in frame: raise ValueError(f"Required key column missing: {col}")
        frame[col] = frame[col].astype("string").str.strip().replace({"":"<MISSING>"})

    # Keep the first dimension row per key; record excluded duplicates/missing IDs.
    miss_p = int(p.patient_id.eq("<MISSING>").sum())
    p = p[p.patient_id.ne("<MISSING>")].drop_duplicates("patient_id", keep="first").copy()
    record("patient_missing_or_duplicate_key", "Removed rows with missing patient key and kept first duplicate key.", miss_p + int(raw["patients"].shape[0]-miss_p-p.shape[0]))
    miss_o = int(o.hospital_id.eq("<MISSING>").sum())
    o = o[o.hospital_id.ne("<MISSING>")].drop_duplicates("hospital_id", keep="first").copy()
    record("organization_missing_or_duplicate_key", "Removed missing keys and kept first organization per ID.", miss_o + int(raw["organizations"].shape[0]-miss_o-o.shape[0]))
    before = len(e)
    e = e[e.encounter_id.ne("<MISSING>") & e.patient_id.ne("<MISSING>")].drop_duplicates("encounter_id", keep="first").copy()
    record("encounter_missing_or_duplicate_key", "Removed missing keys and retained the first encounter ID.", before-len(e))

    e["start_date"] = pd.to_datetime(e.start_date, errors="coerce", utc=True).dt.tz_localize(None).dt.normalize()
    e["discharge_date"] = pd.to_datetime(e.discharge_date, errors="coerce", utc=True).dt.tz_localize(None).dt.normalize()
    bad_start = int(e.start_date.isna().sum())
    e = e[e.start_date.notna()].copy()
    bad_order = int((e.discharge_date.notna() & (e.discharge_date < e.start_date)).sum())
    e = e[~(e.discharge_date.notna() & (e.discharge_date < e.start_date))].copy()
    record("invalid_start_date", "Excluded unparseable or missing encounter start dates.", bad_start)
    record("discharge_before_start", "Excluded rows where discharge preceded encounter start.", bad_order)
    record("missing_discharge_date", "Retained open encounters in clean file; they cannot be a readmission index stay.", int(e.discharge_date.isna().sum()))

    p["birth_date"] = pd.to_datetime(p.get("birth_date"), errors="coerce")
    e["birth_date"] = e.patient_id.map(p.set_index("patient_id").birth_date.to_dict())
    e["age_at_admission"] = e.start_date.dt.year - e.birth_date.dt.year
    e.loc[e.age_at_admission.lt(0) | e.age_at_admission.gt(120), "age_at_admission"] = pd.NA
    e["age_band"] = pd.cut(e.age_at_admission, [-1,17,29,39,49,59,69,79,89,120],
                           labels=["0-17","18-29","30-39","40-49","50-59","60-69","70-79","80-89","90+"]).astype("string").fillna("Unknown")
    for c in ["gender","race","ethnicity"]:
        source = _col(p, c)
        if source is None: p[c] = "Unknown"
        else: p[c] = p[source].fillna("Unknown").astype(str)
    p["birth_date"] = p.birth_date.dt.strftime("%Y-%m-%d")
    o["region"] = o.state.map(region_for_state)
    o["city"] = o.get("city", pd.Series("Unknown", index=o.index)).fillna("Unknown")
    o["hospital_name"] = o.get("hospital_name", pd.Series("Unknown", index=o.index)).fillna("Unknown")
    e["hospital_id"] = e.hospital_id.fillna("UNKNOWN")
    e = e.merge(o[["hospital_id","region"]], on="hospital_id", how="left")
    e["region"] = e.region.fillna("Unknown")
    e["encounter_class"] = e.encounter_class.fillna("unknown").str.lower().str.strip()
    e["reason_category"] = e.get("reason_category", pd.Series("Unspecified", index=e.index)).fillna("Unspecified")
    e["total_cost"] = pd.to_numeric(e.get("total_cost", 0), errors="coerce").fillna(0).clip(lower=0)
    e["length_of_stay_days"] = (e.discharge_date - e.start_date).dt.days
    e["length_of_stay_days"] = e.length_of_stay_days.clip(lower=0)

    clean_cols = ["encounter_id","patient_id","hospital_id","start_date","discharge_date","encounter_class",
                  "reason_category","region","age_at_admission","age_band","length_of_stay_days","total_cost"]
    clean = e[clean_cols].copy()
    inpatient = clean[(clean.encounter_class == "inpatient") & clean.discharge_date.notna()].copy()
    inpatient = inpatient.sort_values(["patient_id","start_date","encounter_id"])
    inpatient["next_inpatient_encounter_id"] = inpatient.groupby("patient_id").encounter_id.shift(-1)
    inpatient["next_inpatient_start"] = inpatient.groupby("patient_id").start_date.shift(-1)
    inpatient["days_to_readmission"] = (inpatient.next_inpatient_start - inpatient.discharge_date).dt.days
    inpatient["readmission_30d"] = inpatient.days_to_readmission.between(1,30).fillna(False).astype(int)
    inpatient["date_key"] = inpatient.start_date.dt.strftime("%Y-%m-%d")
    inpatient["start_date"] = inpatient.start_date.dt.strftime("%Y-%m-%d")
    inpatient["discharge_date"] = inpatient.discharge_date.dt.strftime("%Y-%m-%d")
    inpatient["next_inpatient_start"] = inpatient.next_inpatient_start.dt.strftime("%Y-%m-%d")
    for c in ["start_date","discharge_date"]: clean[c] = clean[c].dt.strftime("%Y-%m-%d")
    for name, frame in {
        "dim_patient": p[["patient_id","birth_date","gender","race","ethnicity"]],
        "dim_hospital": o[["hospital_id","hospital_name","city","state","region"]],
        "encounters_clean": clean,
        "fact_readmission": inpatient[["encounter_id","patient_id","hospital_id","date_key","start_date","discharge_date",
            "length_of_stay_days","readmission_30d","next_inpatient_encounter_id","next_inpatient_start",
            "days_to_readmission","age_at_admission","age_band","reason_category","region","total_cost"]]
    }.items():
        frame.to_csv(out / f"{name}.csv", index=False)
    pd.DataFrame(log).to_csv(out / "data_quality_log.csv", index=False)
    return {"patients":len(p),"hospitals":len(o),"clean_encounters":len(clean),
            "inpatient_encounters":len(inpatient),"readmissions":int(inpatient.readmission_30d.sum())}
