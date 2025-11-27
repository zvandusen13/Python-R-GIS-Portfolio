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

How it was Made
- Data Collection: Property ownership and assessment data were manually extracted from the Lewiston Assessor’s database and written in a CSV file
- Data Cleaning: Missing values were removed for analyses that required purchase prices or dates. Numeric conversion and date formatting were applied.
- Mapping: Shapefiles of the properties neighboring the Bates campus were acquired from the Lewiston city government. Using the sf package, the properties were color-coded by assessed values using ggplot2
- Statistical Testing: Wilcoxon tests compared purchase prices to current assessed values to determine significant appreciation or depreciation.
- Visualization: Property purchasing history, value changes, and spatial distribution were plotted to identify trends and patterns over time.

Usage
- Install required packages: "dataRetrieval", "dplyr", "ggplot2", "lubridate"
- Run the script to generate the plots and analysis
Output

Attached to the folder is a report that displays the plots and an analysis of the significance of the data and the plots. The report contextualizes the property portfolio to the time period of the purchases and theorizes the college's expansion plan for the decades to come.
