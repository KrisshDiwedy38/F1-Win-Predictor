import fastf1 as f1
import pandas as pd 

f1.Cache.enable_cache("F1_Cache")

years = [2022, 2023, 2024]
events = ['R']
rounds = [22,22,24]

count = -1
for year in years:
   count += 1
   for event in events:
      for round in range(1,rounds[count] + 1):
         session = f1.get_session(year, round, event)
         name = str(session).split(":")[1].split("-")[0].strip()
         print(f"{year} - {name}")
