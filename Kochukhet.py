import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------
# Kochukhet Coordinates
LATITUDE = 23.707306
LONGITUDE = 90.415483

# Calculate dates
today = datetime.now()
week_ago = today - timedelta(days=7)

# Format dates for API (YYYY-MM-DD)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

# Open-Meteo API URL
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    f"&start_date={start_date}"
    f"&end_date={end_date}"
    f"&daily=temperature_2m_max,temperature_2m_min"
    f"&timezone=auto"
)

# Fetch weather data
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("\n=== Raw API Response ===")
    print(data)
else:
    print(f"Error: {response.status_code}")
    exit()

# ---------------------------------------------------
# Extract daily weather data

daily_data = data.get("daily", {})

df = pd.DataFrame({
    "date": daily_data.get("time", []),
    "max_temp": daily_data.get("temperature_2m_max", []),
    "min_temp": daily_data.get("temperature_2m_min", [])
})

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

print("\n=== Kochukhet Weather Data ===")
print(df)

# ---------------------------------------------------
# Display summary statistics

print("\n=== Weather Summary ===")
print(f"Highest Temperature: {df['max_temp'].max()} °C")
print(f"Lowest Temperature: {df['min_temp'].min()} °C")
print(f"Average Maximum Temperature: {df['max_temp'].mean():.2f} °C")
print(f"Average Minimum Temperature: {df['min_temp'].mean():.2f} °C")

# ---------------------------------------------------
# Create Weather Plot

plt.figure(figsize=(12, 6))

plt.plot(
    df["date"],
    df["max_temp"],
    marker="o",
    linewidth=2,
    label="Max Temperature"
)

plt.plot(
    df["date"],
    df["min_temp"],
    marker="o",
    linewidth=2,
    label="Min Temperature"
)

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Kochukhet Weather - Past 7 Days")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)

plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
chart_file = "kochukhet_weather_chart.png"
plt.savefig(chart_file, dpi=300)

print(f"\nChart saved as: {chart_file}")

plt.show()

# ---------------------------------------------------
# Create data folder

os.makedirs("data", exist_ok=True)

# Save CSV
csv_file = "data/kochukhet_weather.csv"
df.to_csv(csv_file, index=False)

print(f"Data saved to: {csv_file}")

# ---------------------------------------------------
# Display complete weather table

print("\n=== Complete Weather Report ===")
for _, row in df.iterrows():
    print(
        f"{row['date'].strftime('%Y-%m-%d')} | "
        f"Max: {row['max_temp']} °C | "
        f"Min: {row['min_temp']} °C"
    )