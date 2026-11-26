# Excel Power Query and dashboard guide

1. Open a new workbook and use Data > Get Data > From Text/CSV to load the cleaned fact and dimension CSVs.
2. In Power Query, set IDs to Text, dates to Date, readmission_30d to Whole Number and total_cost to Decimal Number.
3. Use Transform > Format > Trim and Clean on descriptive text columns.
4. Review errors before choosing Remove Errors; preserve an audit of any rows excluded.
5. Load the cleaned tables to the Data Model.
6. Create PivotTables for monthly rate, rate by region, reason category and length-of-stay band.
7. Add slicers for date, region, age band and encounter reason; connect each slicer to relevant PivotTables.
8. Add a Dashboard sheet with KPI cells for encounter count, readmissions, readmission rate and average length of stay.

Cross-check formulas:
- Readmissions: SUM of readmission_30d.
- Encounter count: COUNT of encounter_id.
- Rate: readmissions / encounter count.
- Average stay: AVERAGE of length_of_stay_days.

All supplied records are synthetic. Do not present the resulting rates as hospital performance.
