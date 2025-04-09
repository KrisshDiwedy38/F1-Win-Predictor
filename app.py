import fastf1 as f1
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from datetime import date
from driver_performance import driver_performance_data 
from driver_performance import driver_mean_df

# SQL Accessing parameters
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

# Getting the Performance and LapTime of drivers on the specified circuit for the last 3 years
def get_circuit_performance(df, circuit):

    # Circuit data columns - RaceName, Performance, DriverCode for the specified circuit
    circuit_data = df[df["RaceName"] ==  circuit].loc[: , ["RaceName","Performance","DriverCode"]].copy()

    # Lap Time data columns - DriverCode, LapTime for the specified circuit
    lap_time_data = df[df["RaceName"] == circuit].loc[:,["DriverCode","LapTime"]].copy()
    circuit = circuit.replace(" ","") # Remove spaces from circuit name
    performance_list = []
    time_list = []

    # Calculating mean performance and mean lap time for drivers on the circuit
    for driver in circuit_data['DriverCode'].unique():
        mean_perf = circuit_data[circuit_data['DriverCode'] == driver]['Performance'].mean()
        performance_list.append({
            'DriverCode': driver,
            'RacePerformance': mean_perf
        })
        mean_time = lap_time_data[lap_time_data['DriverCode'] == driver]['LapTime'].mean()
        time_list.append({
            'DriverCode': driver,
            'LapTime': mean_time
        })

    circuit_df = pd.DataFrame(performance_list)
    lap_time_df = pd.DataFrame(time_list)
    return circuit_df , lap_time_df

# Extract dataset from SQL to IDE in form of a pandas dataframe 
df = pd.read_sql('SELECT * FROM "F1ResultData" ORDER BY "index" ;', engine)
weather_df = pd.read_sql('SELECT * FROM "F1WeatherData" ORDER BY "index" ;', engine)

driver_data = df.loc[:,["DriverCode", "Time"]].copy()

# Get Qualifying data for the race predictions
quali_data = {
    'DriverCode': [
        'NOR', 'VER', 'RUS', 'HAM', 'PIA', 'LEC', 'SAI', 'PER', 'ALO', 'HUL',
        'STR', 'ALB', 'MAG', 'GAS', 'RIC', 'TSU', 'OCO', 'ZHO', 'BOT', 'SAR'
    ],
    'QualiTime': [
        101.243, 101.355, 101.427, 101.558, 101.697, 101.800, 101.887, 101.922, 102.019, 102.055,
        102.213, 102.368, 102.507, 102.513, 102.777, 102.797, 102.857, 103.193, 103.220, 103.379
    ]
}

quali_df = pd.DataFrame(quali_data)

circuit = "Singapore Grand Prix"

# Getting circuit performance and lap times
circuit_performance , Lap_time_df = get_circuit_performance(driver_performance_data, circuit) 

results_df = quali_df.copy()

# Merge the needed databases for training model
merged_df = pd.merge(quali_df,driver_mean_df, on='DriverCode', how='inner')
merged_df = pd.merge(merged_df,circuit_performance, on='DriverCode', how='inner')
merged_df = pd.merge(merged_df,Lap_time_df, on='DriverCode', how='inner')

# Define X and y
X = merged_df[['QualiTime', 'MeanPerformance', 'RacePerformance']]
y = merged_df['LapTime']

# Split the data into Train and Test sets 
X_train, X_test, y_train, y_test = train_test_split(X , y , test_size = 0.2, random_state = 39)

# Training Gradient Boosting model for predicting the winner
model = GradientBoostingRegressor(n_estimators = 100, learning_rate = 0.1, random_state = 39)
model.fit(X_train, y_train)

# Predicting
predicted_lap_times = model.predict(merged_df[['QualiTime', 'MeanPerformance', 'RacePerformance']])
results_df["PredictedRaceTime"] = predicted_lap_times

results_df = results_df.sort_values("PredictedRaceTime")

# Output
print(f"F1 {circuit} Prediction:")
print(f"Predicted Winner: {results_df.iloc[0]['DriverCode']}")
print("Top 3 Predictions")
top3= results_df[['DriverCode', 'PredictedRaceTime']].head(3)
print(top3[["DriverCode","PredictedRaceTime"]].to_string(index=False))

# Calculating the Mean Squared Error
y_pred = model.predict(X_test)
print("Root Mean Squared Error:", np.sqrt(mean_squared_error(y_test, y_pred)))