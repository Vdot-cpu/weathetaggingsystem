#!/usr/local/bin/python
# -*- coding: iso-8859-1 -*-

import requests
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
from meteostat import Point, Daily, Monthly, Hourly
from datetime import datetime

# Create Point for Locations
# London
london = Point(51.5074, -0.1278)
# New York
new_york = Point(40.7128, -74.0060)
# Tokyo
tokyo = Point(35.6762, 139.6503)
# Get Hourly data for 2018

# Weather parameters
temperature = 'tavg'
precipitation = 'prcp'

# stock parameters
# agriculture_ticker = yf.Ticker("AAPL")
agriculture_ticker = yf.Ticker("^SPGSAG")
technology_ticker = yf.Ticker("^SPGSTISO")
consumerGood_ticker = yf.Ticker("^SPHLCGIP")


def set_start_date_time(year, month, day):
    startYear = year
    startMonth = month
    startDay = day
    global stockStartDate
    stockStartDate = str(year) + '-' + str(month) + '-' + str(day)
    global weatherStartDate
    weatherStartDate = datetime(year, month, day)


def set_end_date_time(year, month, day):
    endYear = year
    endMonth = month
    endDay = day
    global stockEndDate
    stockEndDate = str(year) + '-' + str(month) + '-' + str(day)
    global weatherEndDate
    weatherEndDate = datetime(year, month, day)


# Set date range
set_start_date_time(2023, 2, 17)
set_end_date_time(2023, 2, 24)

# granularity "1m" "2m" "5m" "15m" "30m" "60m" "90m" "1h" “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

# get the stock data
def get_stock_data(startDate, endDate, interval, ticker):
    print(f"Fetching stock data from {startDate} to {endDate}")
    history = ticker.history(start=startDate, end=endDate, period=interval, actions=False)
    print(history)
    return history


# get weather data
def get_weather_data(location):
    print(f"Fetching weather data from {weatherStartDate} to {weatherEndDate}")
    data = Daily(location, weatherStartDate, weatherEndDate)
    data = data.fetch()
    return data


# mpf.plot(get_stock_data(stockStartDate,stockEndDate,'1m',agriculture_ticker), type='line')

# Plot both datasets on the same graph
def plot_data(ticker, interval, location):
    # Get stock data
    stock_data = get_stock_data(stockStartDate, stockEndDate, interval, ticker)

    # Get weather data
    weather_data = get_weather_data(location)

    # Filter weather data to match date range of stock data
    weather_data = weather_data.loc[stock_data.index[0]:stock_data.index[-1], :]

    # Create subplots
    fig, ax = plt.subplots()

    # Plot stock data
    ax.plot(stock_data.index, stock_data['Close'], color='blue')

    # Plot weather data
    ax2 = ax.twinx()
    ax2.plot(weather_data.index, weather_data[temperature], color='red')

    # Add labels
    ax.set_ylabel('Price')
    ax2.set_ylabel('Temperature (°C)')
    ax.set_xlabel('Date')

    # Set x-axis scale to match stock data
    ax.set_xlim([stock_data.index[0], stock_data.index[-1]])

    plt.show()


set_start_date_time(2023, 2, 20)
set_end_date_time(2023, 2, 25)
plot_data(consumerGood_ticker, '1d', london)