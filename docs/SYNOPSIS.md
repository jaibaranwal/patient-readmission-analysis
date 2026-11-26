# Project Synopsis - Patient Readmission Analysis

## Introduction
This project examines whether a patient has another inpatient encounter within 30 days after discharge from an earlier inpatient encounter. It uses a consistent encounter-date rule and a reproducible analytical workflow.

## Problem
A healthcare analytics team needs a repeatable way to summarise short-interval inpatient returns while preserving patient and encounter relationships and documenting data-quality decisions.

## Objectives
1. Clean patient, organization and encounter CSV files.
2. Create a 30-day inpatient readmission flag using discharge and next-admission dates.
3. Store the analytical tables in a relational star schema.
4. Answer seven business questions using SQL.
5. Produce KPIs, charts, a notebook and a filterable dashboard.
6. Validate data keys, ranges, dimension references and Python/SQL totals.

## Method
The pipeline standardises source columns and dates, records excluded or corrected rows, derives age and region groupings, sorts inpatient encounters by patient and start date, then compares each discharge with the next inpatient start. SQLite stores dimensions and fact rows; SQL queries and Python produce the analytical outputs.

## Limitations
The bundled input is synthetic. Results are for software demonstration and cannot support clinical or hospital-performance conclusions.
