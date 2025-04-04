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

years = [2022, 2023, 2024]
events = ['R']
rounds = [22,22,24]

count = -1
for year in years:
   count += 1
   for event in events:
      for round in range(1,rounds[count] + 1):
         session = f1.get_session(year, round, event)
         session._load_weather_data()
         session._load_drivers_results()
         race_id = f"{str(year)}_{round}"
         race_name = str(session).split(":")[1].split("-")[0].strip()
         if session.weather_data["Rainfall"].any():
            rainfall = "True"
         result_data = session.results.loc[:,['TeamName','Abbreviation','FullName','Time', 'Position']].copy()
         time = 0
         for row in result_data.sort_values("Position").itertuples():
            time += (row.Time).total_seconds()
            race_data = {
            'Position' : row.Position,
            'RaceName' : race_name,
            'RaceID' : race_id,
            'TeamName' : row.TeamName,
            'DriverCode' : row.Abbreviation,
            'FullName' : row.FullName,
            'Time(s)' : round(time,5),
            'Rainfall' : rainfall
         }
            
         values.append(race_data)

f1_df = pd.DataFrame(values)
f1_df.to_sql("f1data", engine, if_exists="append", index = False)
print("Data Enter Successfully!")