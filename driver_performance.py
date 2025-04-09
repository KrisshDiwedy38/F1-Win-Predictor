import fastf1 as f1
import pandas as pd
from sqlalchemy import create_engine

# SQL parameters
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

# Extract dataset from SQL to IDE in form of a pandas dataframe 
df = pd.read_sql('SELECT * FROM "F1ResultData" ORDER BY "index" ;', engine)
weather_df = pd.read_sql('SELECT * FROM "F1WeatherData" ORDER BY "index" ;', engine)

# Number for laps in F1 races
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

# Getting data to calculate the performance
driver_performance_data = df.loc[:,["DriverCode", "Time", "RaceName"]].copy().dropna()

# Driver Performance  = time / number of laps : Will be used to calculate the circuit specific performance
for row in driver_performance_data.sort_values("DriverCode").itertuples():
   if row.RaceName in race_laps:
      performance = row.Time / race_laps[row.RaceName]
      times.append(row.Time)
      driver_performance.append(performance)
   
driver_performance_data['Performance'] = driver_performance
driver_performance_data['LapTime'] = times

# Driver Mean = Mean of driver performance from all the races in dataset : Shows the form of the driver coming into the race
means = {}
for driver in driver_performance_data["DriverCode"].unique():
    driver_mean = driver_performance_data[driver_performance_data["DriverCode"] == driver]["Performance"].mean()
    means[driver] = driver_mean

driver_mean_df = pd.DataFrame(list(means.items()), columns=["DriverCode", "MeanPerformance"])