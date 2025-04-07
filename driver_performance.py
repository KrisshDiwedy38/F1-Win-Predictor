import fastf1 as f1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression


f1.Cache.enable_cache("F1_Cache")

db_params = {
    "dbname": "f1data",
    "user": "postgres",
    "password": "Krissh",
    "host": "localhost",
    "port": "5432"
}

conn_str = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"

# Create SQLAlchemy engine
engine = create_engine(conn_str)

# Test connection
with engine.connect() as conn:
    print("Connected to PostgreSQL!")

df = pd.read_sql('SELECT * FROM "F1ResultData" ORDER BY "index" ;', engine)
weather_df = pd.read_sql('SELECT * FROM "F1WeatherData" ORDER BY "index" ;', engine)

race_laps = {
    "Australian Grand Prix": 58,
    "Italian Grand Prix": 53,
    "British Grand Prix": 52,
    "São Paulo Grand Prix": 71,
    "Mexico City Grand Prix": 71,
    "Japanese Grand Prix": 53,
    "Bahrain Grand Prix": 57,
    "Abu Dhabi Grand Prix": 58,
    "Azerbaijan Grand Prix": 51,
    "Saudi Arabian Grand Prix": 50,
    "Qatar Grand Prix": 57,
    "Belgian Grand Prix": 44,
    "Austrian Grand Prix": 71,
    "Spanish Grand Prix": 66,
    "Las Vegas Grand Prix": 50,
    "Singapore Grand Prix": 61,
    "Chinese Grand Prix": 56,
    "Hungarian Grand Prix": 70,
    "United States Grand Prix": 56,
    "Miami Grand Prix": 57,
    "French Grand Prix": 53,
    "Emilia Romagna Grand Prix": 63,
    "Canadian Grand Prix": 70,
    "Dutch Grand Prix": 72,
    "Monaco Grand Prix": 78,
}

driver_performance = []
times = []

driver_data = df.loc[:,["DriverCode", "Time", "RaceName"]].copy().dropna()

for row in driver_data.sort_values("DriverCode").itertuples():
   if row.RaceName in race_laps:
      performance = row.Time / race_laps[row.RaceName]
      times.append(row.Time)
      driver_performance.append(performance)
   
performance_df = pd.DataFrame(
   {
      'Time' : times,
      'Performance' : driver_performance
   }
)

driver_race_performance = pd.merge(driver_data, performance_df, on='Time')

means = {}
for driver in driver_race_performance["DriverCode"].unique():
    driver_mean = driver_race_performance[driver_race_performance["DriverCode"] == driver]["Performance"].mean()
    means[driver] = driver_mean

mean_df = pd.DataFrame(list(means.items()), columns=["DriverCode", "MeanPerformance"])

print(mean_df.sort_values("MeanPerformance"))