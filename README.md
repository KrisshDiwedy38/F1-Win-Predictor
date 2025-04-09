# F1 Race Winner Predictor

This project uses machine learning to predict the winner of an F1 race based on a variety of data sources, including historical race results, lap times, qualifying performance, and weather conditions.

## Features

- FastF1 API integration for official F1 data
- PostgreSQL backend for storing race data
- Data preprocessing using Pandas and NumPy
- Feature engineering to calculate driver form and circuit-specific performance
- Gradient Boosting Regressor to predict race outcomes
- Web scraping for dynamic race calendar and updates
- Visualizations for performance comparison

## Data Sources

- [FastF1 Python Package](https://theoehrly.github.io/Fast-F1/)
- Formula1.com for scraping completed races
- PostgreSQL database for structured data storage and retrieval

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- scikit-learn
- fastf1
- sqlalchemy
- psycopg2
- beautifulsoup4
- requests

## Project Structure

```
F1_Win_Predictor/
│
├── app.py                   # Main model pipeline # PostgreSQL operations
├── get_historical_data.py   # API and scraping logic            
├── driver_performance.py    # Data preprocessing
├── get_recent_data.py       # Making sure that database is upto date
├── req.ipynb                # Installing the required packages
├── README.md
```

## How It Works

1. **Data Collection**  
   Historical race data is pulled using FastF1 and stored in a PostgreSQL database. Recent race statuses are scraped.

2. **Data Processing**  
   Each driver's performance is calculated using lap times, qualifying results, and rain conditions. Circuit-specific performance and driver form are engineered.

3. **Model Training**  
   A Gradient Boosting Regressor is trained using a combination of:
   - Mean performance
   - Recent qualifying times
   - Circuit performance history

4. **Prediction**  
   The model predicts each driver's expected race time. The driver with the lowest predicted time is selected as the winner.

## Example Output

```
F1 2025 Japanese Grand Prix Prediction:
Predicted Winner: Max Verstappen
Top 3 Prediction:
1. VER - 5823.1s
2. LEC - 5842.7s
3. HAM - 5845.9s
```

## Limitations

- Limited data size may affect generalization
- Qualifying and weather data must be up-to-date for accurate predictions
- Some circuits and seasons may not have complete lap-by-lap data

## Future Work

- Add classification model to directly predict race position
- Adding more feature to bring down the RMSE to less than 0.5s
- Integrate real-time telemetry data
- Build a front-end UI for easier interaction
- Automate weekly updates using a scheduler

