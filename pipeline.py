import pandas as pd
import requests

# 1. Query European meteorological data (Open-Meteo REST API)
# Coordinates for Berlin/Germany hub: Lat 52.52, Lon 13.41
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,direct_normal_irradiance&forecast_days=7"
response = requests.get(url)
data = response.json()

# 2. Ingest raw time-series into structured Pandas DataFrame
df = pd.DataFrame({
    'timestamp': pd.to_datetime(data['hourly']['time']),
    'temperature_c': data['hourly']['temperature_2m'],
    'solar_irradiance_wm2': data['hourly']['direct_normal_irradiance']
})

# 3. Quantitative Demand Proxy Modeling (Degree Days)
# Heating proxy assumes baseline 18°C; Cooling proxy assumes baseline 22°C
df['heating_degree_proxy'] = df['temperature_c'].apply(lambda x: max(0, 18 - x))
df['cooling_degree_proxy'] = df['temperature_c'].apply(lambda x: max(0, x - 22))

# 4. Daily aggregation and power load metrics
daily_summary = df.set_index('timestamp').resample('D').agg({
    'temperature_c': ['mean', 'min', 'max'],
    'solar_irradiance_wm2': 'sum',
    'heating_degree_proxy': 'sum',
    'cooling_degree_proxy': 'sum'
})

# Flatten MultiIndex columns for clean tabular export
daily_summary.columns = [
    'temp_mean_c', 'temp_min_c', 'temp_max_c',
    'solar_irradiance_total_wm2',
    'heating_degree_total', 'cooling_degree_total'
]

# 5. Export structured output
daily_summary.to_csv("energy_market_demand_summary.csv")
print("Energy data pipeline executed successfully. Summary saved.")
