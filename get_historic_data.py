""" THIS IS FOR STORING THE DATA REQUIRED FOR MY MODEL IN A POSTGRESQL DATABASE TO PRACTICE THE INTEGRATION OF PYTHON AND POSTGRESQL
    THIS IS NOT REQUIRED!! F1 CACHE WILL WORK JUST FINE"""

import fastf1 as f1
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# PostgreSQL Parameters
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

# Years, Events and No. of Races for the years
years = [2022, 2023, 2024]
events = ['R']
rounds = [22,22,24]

# Store Result Data
result_values = []
# Store Weather Data
weather_values = []

count = -1
# Getting Race Data for Round " " of Year " "
for year in years:
   count += 1
   for event in events:
      for race_round in range(1,rounds[count] + 1):
         session = f1.get_session(year, race_round, event)
         # Load Weather and Result data 
         session._load_weather_data()
         session._load_drivers_results()
         # Set a unique id for Primary Key and referencing other tables
         race_id = f"{str(year)}_{race_round}"
         # Extracting race name
         race_name = str(session).split(":")[1].split("-")[0].strip()
         # Checking if the race had rain
         if session.weather_data["Rainfall"].any():
            rainfall = "True"
         else:
            rainfall = "False"
         
         # Getting required data
         result_data = session.results.loc[:,['TeamName','Abbreviation','FullName','Time', 'Position', 'Status']].copy()
         time = 0

         for row in result_data.sort_values("Position").itertuples():

            # Handling null time values given to lapped cars 
            if row.Status == "+1 Lap" or row.Status == "+2 Laps":
               time += 10.00
            else: 
               # Converting timedelta value to float value(in seconds)
               time += (row.Time).total_seconds()
            
            # Race Result table
            race_data = {
               'Position' : row.Position,
               'RaceID' : race_id,
               'RaceName' : race_name,
               'TeamName' : row.TeamName,
               'DriverCode' : row.Abbreviation,
               'FullName' : row.FullName,
               'Time(s)' : round(time,4),
               'Status' : row.Status
            }
            # Race Weather table
            weather_data = {
               'RaceID' : race_id,
               'RaceName' : race_name,
               'Rainfall' : rainfall
            }
            result_values.append(race_data)
         weather_values.append(weather_data)

# Converting values into a panads dataframe
f1_result_df = pd.DataFrame(result_values)
f1_weather_df = pd.DataFrame(weather_values)

# Converting dfs to sql table and inserting in the database
f1_result_df.to_sql("F1ResultData", engine, if_exists="append", index = False)
print("Result Data Enter Successfully!")
f1_weather_df.to_sql("F1WeatherData", engine, if_exists="append", index= False)
print("Weather Data Enter Successfully!")