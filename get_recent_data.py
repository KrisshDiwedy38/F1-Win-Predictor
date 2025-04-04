import fastf1 as f1
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

f1.Cache.enable_cache("F1_Cache")

year = 2024
event = 'R'
race_round = 2

session = f1.get_session(year,race_round,event)
session._load_drivers_results()
result_data = session.results.loc[:,['TeamName','Abbreviation','FullName','Time', 'Position', 'Status']].copy()
print(result_data)