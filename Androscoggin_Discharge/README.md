Streamflow Analysis – Androscoggin River Flow Station in Lewiston, Maine

Overview
This R script analyzes streamflow data from the USGS National Water Information System for the Androscoggin River in Maine. It visualizes discharge trends, compares recent years to long-term averages, and estimates flood recurrence intervals from 1995 to 2024.

Tools and Data
Packages used: dataRetrieval, dplyr, tidyr, ggplot2, lubridate
Data source: USGS NWIS Instantaneous Discharge using USGS dataRetrieval package
Time range: 1995-01-01 to 2024-03-04

Key Analyses
- Summarize 29 years of discharge data
- Plot long-term and annual flow patterns
- Compare 2020–2023 flows with 1995–2019 averages to investigate if flooding has increased
- Estimate 5-, 25-, 50-, and 100-year flood discharges
- Plot flow duration curve and identify extreme events

Output
Produces time series, annual overlay, flood frequency, and duration curve plots using ggplot2.
