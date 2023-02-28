import requests
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf



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

# Print the S&P data
print("\nS&P Data:")
msft = yf.Ticker("MSFT")
print('\n  ')
history = msft.history(start='2022-02-17', end='2022-03-17')
print(history)



