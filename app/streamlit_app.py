from pathlib import Path
import json, pandas as pd, streamlit as st, plotly.express as px
ROOT=Path(__file__).resolve().parents[1]
FACT=ROOT/"data/clean/fact_readmission.csv"
st.set_page_config(page_title="Patient Readmission Analysis",page_icon="🏥",layout="wide")
st.title("Patient Readmission Analysis")
st.caption("Synthetic educational dataset - not real patient data or clinical guidance.")
if not FACT.exists():
    st.error("Clean data not found. Run python scripts/run_pipeline.py --input data/sample first.")
    st.stop()
df=pd.read_csv(FACT,parse_dates=["start_date"])
with st.sidebar:
    st.header("Filters")
    region=st.multiselect("Region",sorted(df.region.unique()),default=sorted(df.region.unique()))
    age=st.multiselect("Age band",sorted(df.age_band.unique()),default=sorted(df.age_band.unique()))
    reason=st.multiselect("Encounter reason",sorted(df.reason_category.unique()),default=sorted(df.reason_category.unique()))
view=df[df.region.isin(region)&df.age_band.isin(age)&df.reason_category.isin(reason)]
if view.empty: st.warning("No rows match these filters."); st.stop()
n=len(view); r=int(view.readmission_30d.sum())
a,b,c,d=st.columns(4)
a.metric("Inpatient encounters",f"{n:,}"); b.metric("30-day readmissions",f"{r:,}")
c.metric("Readmission rate",f"{100*r/n:.1f}%"); d.metric("Average stay",f"{view.length_of_stay_days.mean():.1f} days")
view["month"]=view.start_date.dt.to_period("M").astype(str)
monthly=view.groupby("month",as_index=False).agg(encounters=("encounter_id","count"),readmissions=("readmission_30d","sum"))
monthly["rate_pct"]=100*monthly.readmissions/monthly.encounters
st.plotly_chart(px.line(monthly,x="month",y="rate_pct",markers=True,title="Monthly 30-day readmission rate"),use_container_width=True)
by_region=view.groupby("region",as_index=False).agg(encounters=("encounter_id","count"),readmissions=("readmission_30d","sum"))
by_region["rate_pct"]=100*by_region.readmissions/by_region.encounters
st.plotly_chart(px.bar(by_region,x="region",y="rate_pct",title="Readmission rate by region"),use_container_width=True)
st.dataframe(view,use_container_width=True,hide_index=True)
