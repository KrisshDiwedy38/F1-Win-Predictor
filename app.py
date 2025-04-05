import fastf1 as f1
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from datetime import date

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

print(df.iloc[-40:])
print(weather_df.iloc[-5:])
