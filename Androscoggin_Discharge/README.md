Streamflow Analysis – Androscoggin River Flow Station in Lewiston, Maine

This R script analyzes streamflow data from the USGS gauge station in Lewiston, Maine, to assess years to long-term averages and estimates flood recurrence intervals from 1995 to 2024.

Highlights
- Summarize 29 years of discharge data
- Plot long-term and annual flow patterns
- Compare 2020–2023 flows with 1995–2019 averages to investigate if flooding has increased
- Estimate 5-, 25-, 50-, and 100-year flood discharges
- Plot flow duration curve and identify extreme events

Data Utilized
- Data source: USGS NWIS Instantaneous Discharge public data using USGS dataRetrieval package
Time range: 1995-01-01 to 2024-03-04

How It's Made
- Data Collection: Streamflow data was retrieved from the USGS National Water Information System using the dataRetrieval R package for the Androscoggin River at Lewiston, Maine.
- Data Cleaning: Missing values were handled, column names standardized, and date-time data formatted for analysis.
- Analysis: Long-term and recent flow patterns were summarized, and 25-year average flows were calculated to compare historical trends with 2020–2023 flows.
- Statistical Modeling: Flood recurrence intervals were estimated using annual maximum flows and a log-linear model to calculate 5-, 25-, 50-, and 100-year flood discharges.
- Visualization: Time series plots, annual overlays, flow duration curves, and extreme flood event plots were created using ggplot2 to illustrate trends and anomalies.

Tools: R, dataRetrieval, dplyr, tidyr, ggplot2, lubridate.

Usage
- Install required packages: "dataRetrieval", "dplyr", "ggplot2", "lubridate"
- Run the script to generate the plots and analysis
Output

Attached to the folder is a report analyzing the results produced in this investigative study. The code and plots produced are walked through. The report concludes there are no more frequent flooding events in the last 3 years than in the previous 26 years.

