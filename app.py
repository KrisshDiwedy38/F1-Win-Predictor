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
session = f1.get_session(2024,2,'R')
session.load()
print((session.weather_data).to_string())
# print(session.results.columns)
# race_data = session.results.loc[:,['TeamName','Abbreviation','FullName','Time', 'Position']].copy()
# time = 0
# for row in race_data.sort_values("Position").itertuples():
#    time += (row.Time).total_seconds()
#    data = session
#    data = {
#       'Position' : row.Position,
#       'TeamName' : row.TeamName,
#       'DriverCode' : row.Abbreviation,
#       'FullName' : row.FullName,
#       'Time' : round(time,5)
#    }

#    values.append(data)

# df = pd.DataFrame(values)

# df.to_sql("racedata", engine, if_exists="append", index=False)
# print("Data inserted successfully!")
