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

def get_circuit_performance(df, circuit):
    circuit_data = df[df["RaceName"] ==  circuit].loc[: , ["RaceName","Performance","DriverCode"]].copy()
    lap_time_data = df[df["RaceName"] == circuit].loc[:,["DriverCode","LapTime"]].copy()
    circuit = circuit.replace(" ","")
    performance_list = []
    time_list = []

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


df = pd.read_sql('SELECT * FROM "F1ResultData" ORDER BY "index" ;', engine)
weather_df = pd.read_sql('SELECT * FROM "F1WeatherData" ORDER BY "index" ;', engine)


driver_data = df.loc[:,["DriverCode", "Time"]].copy()

quali_data = {
    'DriverCode': [
        'VER', 'PER', 'HAM', 'RUS', 'LEC', 'SAI', 'NOR', 'PIA', 'ALO', 'STR',
        'OCO', 'GAS', 'ALB', 'SAR', 'BOT', 'ZHO', 'MAG', 'HUL', 'RIC', 'TSU'
    ],
    'QualiTime': [
        87.312, 87.579, 87.842, 87.925, 88.003, 88.127, 88.210, 88.305, 88.412, 88.630,
        88.794, 88.851, 89.003, 89.215, 89.384, 89.442, 89.603, 89.705, 89.822, 90.001
    ]
}

quali_df = pd.DataFrame(quali_data)

circuit = "Japanese Grand Prix"

circuit_performance , Lap_time_df = get_circuit_performance(driver_performance_data, circuit) 

results_df = quali_df.copy()

merged_df = pd.merge(quali_df,driver_mean_df, on='DriverCode', how='inner')
merged_df = pd.merge(merged_df,circuit_performance, on='DriverCode', how='inner')
merged_df = pd.merge(merged_df,Lap_time_df, on='DriverCode', how='inner')

X = merged_df[['QualiTime', 'MeanPerformance', 'RacePerformance']]
y = merged_df['LapTime']

X_train, X_test, y_train, y_test = train_test_split(X , y , test_size = 0.2, random_state = 39)
model = GradientBoostingRegressor(n_estimators = 100, learning_rate = 0.1, random_state = 39)
model.fit(X_train, y_train)

predicted_lap_times = model.predict(merged_df[['QualiTime', 'MeanPerformance', 'RacePerformance']])
results_df["PredictedRaceTime"] = predicted_lap_times

results_df = results_df.sort_values(by="PredictedRaceTime")

print(results_df)

y_pred = model.predict(X_test)
print("R² Score:", r2_score(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))