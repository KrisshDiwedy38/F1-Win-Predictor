import fastf1

years = [2022, 2023, 2024]
events = ['Q','R']
rounds = [22,22,24]

count = -1 
for year in years:
   count += 1
   for round in range(1,rounds[count]+1):
      for event in events:
         session = fastf1.get_session(year, round, event)
         print(session)