import fastf1 as f1
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

db_params = {
    "dbname": "first",
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

f1.Cache.enable_cache("F1_Cache")
values = []
session = f1.get_session(2025,2,'R')
session._load_weather_data()
session._load_drivers_results()
print(session.results.columns)
print(session.weather_data["Rainfall"])