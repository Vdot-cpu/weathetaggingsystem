import requests
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf



# API keys for OpenWeather API and S&P API
openweather_api_key = "your_openweather_api_key"

# API URLs for OpenWeather API and S&P API
openweather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude=51.51&longitude=-0.13&start_date=2023-01-06&end_date=2023-02-05&hourly=temperature_2m"


# Make API request to OpenWeather API and retrieve data
response = requests.get(openweather_url)
openweather_data = response.json()


# Print the OpenWeather data
print("OpenWeather Data:")
print(openweather_data)

#granularity "1m" "2m" "5m" "15m" "30m" "60m" "90m" "1h" “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

# Print the S&P data
def get_agricultural_data(startDate,endDate,interval):
    print("\nS&P GCSI  Data:")
    agriculture = yf.Ticker("^SPGSCI")
    print('\n  ')
    history = agriculture.history(start=startDate, end=endDate, interval = interval,actions= False)
    mpf.plot(history, type='line')

def get_agricultural_data(startDate,endDate,interval):
    print("\nNorth America Agriculture  Data:")
    agriculture = yf.Ticker("^SPGSAG")
    print('\n ')
    history = agriculture.history(start=startDate, end=endDate, interval = interval,actions= False)
    mpf.plot(history, type='line')

def get_technology_data(startDate,endDate,interval):
    print("\nNorth America Technology  Data:")
    agriculture = yf.Ticker("^SPGSTISO")
    print('\n  ')
    history = agriculture.history(start=startDate, end=endDate, interval = interval,actions= False)
    mpf.plot(history, type='line')

def get_consumerGood_data(startDate,endDate,interval):
    print("\n North America Consumer Goods Data:")
    agriculture = yf.Ticker("^SPHLCGIP")
    print('\n  ')
    history = agriculture.history(start=startDate, end=endDate, interval = interval,actions= False)
    mpf.plot(history, type='line')


get_agricultural_data('2023-02-23','2023-02-24','1m')



