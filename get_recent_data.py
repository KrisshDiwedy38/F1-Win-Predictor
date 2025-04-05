""" THIS IS FOR STORING THE DATA REQUIRED FOR MY MODEL IN A POSTGRESQL DATABASE TO PRACTICE THE INTEGRATION OF PYTHON AND POSTGRESQL
    THIS IS NOT REQUIRED!! F1 CACHE WILL WORK JUST FINE"""

import fastf1 as f1
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import date

f1.Cache.enable_cache("F1_Cache")

# Function to get the number of rounds completed
def get_completed_f1_rounds(year=2025):
   schedule = f1.get_event_schedule(year)
   completed = -1
   for race_date in schedule["EventDate"]:
      timestamp = pd.Timestamp(race_date)
      date_only = timestamp.date()
      if date_only < date.today():
         completed += 1

   return completed

# SQL Parameters
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

# Fetching data from SQL Database
df = pd.read_sql('SELECT * FROM "F1ResultData" ORDER BY "index" ;', engine)
weather_df = pd.read_sql('SELECT * FROM "F1WeatherData" ORDER BY "index";' , engine)

year = 2025
race = get_completed_f1_rounds(year)

# Get last RaceID to avoid entering dublicate data
last_race_id = df["RaceID"].iloc[-1]

if int(last_race_id.split("_")[0]) == year and int(last_race_id.split("_")[1]) == race:
   print("Data Already There")
else:
   try:
      # If Round Data not in DB, Get data and enter
      session = f1.get_session(year, race, 'R')
      session._load_drivers_results()
      session._load_weather_data()

      # Store Result Data
      result_values = []
      # Store Weather Data
      weather_values = []

      # Setting RaceID and Extracting RaceName
      race_id = f"{year}_{race}"
      race_name = str(session).split(":")[1].split("-")[0].strip()

      # Checking for rain
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
            'Time' : round(time,4),
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
      f1_weather_df.to_sql("F1WeatherData", engine, if_exists="append", index = False)
      print("Weather Data Enter Successfully!")
   except Exception as e:
      print(f"Error occured while fetching data {e}")

