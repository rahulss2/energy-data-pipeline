# energy-data-pipeline
automated pipeline parsing European energy &amp; weather time-series data to compute heating/cooling degree load proxies.
# European Energy Market Time-Series Pipeline

An automated quantitative data pipeline written in Python that ingests forecasted meteorological time-series data from European grid hubs, processes heating/cooling degree load proxies, and exports aggregated daily indicators for power market analysis.

## Key Features
- **Automated Ingestion**: Queries the Open-Meteo REST API for 7-day hourly temperature and direct normal irradiance ($W/m^2$) for Germany (central European power hub).
- **Demand Proxy Calculations**: Models heating degree requirements ($\le 18^\circ\text{C}$) and cooling degree loads ($\ge 22^\circ\text{C}$).
- **Time-Series Resampling**: Utilizes `pandas` to aggregate 168 hourly datapoints into daily means, extremes, and cumulative solar irradiance.
- **Structured Export**: Outputs clean tabular CSV summaries ready for quantitative analysis and energy balance models.

## Tech Stack
- Python 3
- Pandas (Time-series manipulation & aggregation)
- Requests (REST API integration)

## Quickstart
```bash
pip install pandas requests
python pipeline.py
