# Dataset source and limitations

## Bundled dataset
The repository's preview dataset is a deterministic, project-generated synthetic fixture. It is not a hospital extract, not real patient data, and not the official Synthea 1K sample. Included metrics and charts are software-validation outputs only.

## Intended source
Synthea 1K Sample Synthetic Patient Records (CSV): https://synthetichealth.github.io/downloads.html  
Synthea project: https://github.com/synthetichealth/synthea  
Paper: https://doi.org/10.1093/jamia/ocx079

Synthea generates synthetic patient records. Cite the project and paper when using its archive; never describe synthetic records as actual patient records.

## Input files
- patients.csv: Id, BIRTHDATE, GENDER, RACE, ETHNICITY
- organizations.csv: Id, NAME, CITY, STATE
- encounters.csv: Id, Patient, Organization, Start, Stop, EncounterClass, Description, ReasonDescription, Total_Claim_Cost

## Interpretation
The 30-day flag is an encounter-date rule: the same patient must have a subsequent inpatient encounter starting 1-30 days after index discharge. This is descriptive only and does not assess preventability, quality of care or clinical risk.
