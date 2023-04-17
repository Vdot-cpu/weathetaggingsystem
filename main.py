from tkinter import messagebox

import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from meteostat import Point, Daily, Monthly, Hourly
from datetime import datetime
from scipy.interpolate import interp1d, InterpolatedUnivariateSpline

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
apple_ticker = yf.Ticker("AAPL")
#agriculture_ticker = yf.Ticker("^SPGSAG")
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
    return stockStartDate, weatherStartDate


def set_end_date_time(year, month, day):
    endYear = year
    endMonth = month
    endDay = day
    global stockEndDate
    stockEndDate = str(year) + '-' + str(month) + '-' + str(day)
    global weatherEndDate
    weatherEndDate = datetime(year, month, day)
    return stockEndDate, weatherEndDate

# Set date range
set_start_date_time(2023, 2, 17)
set_end_date_time(2023, 2, 24)


# granularity "1m" "2m" "5m" "15m" "30m" "60m" "90m" "1h" “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

# get the stock data
def get_stock_data(startDate, endDate, interval, ticker):
    print(f"Fetching stock data from {startDate} to {endDate}")
    history = ticker.history(start=startDate, end=endDate, period=interval, actions=False)

    if not history.empty:
        history.index = history.index.tz_localize(None)
    else:
        messagebox.showerror("Error", "Please enter a valid stock symbol.")
        return None


    print(history)
    return history


# get weather data
def get_weather_data(location, weather_parameter, stockData):

    print(f"Fetching weather data from {weatherStartDate} to {weatherEndDate}")
    data = Daily(location, weatherStartDate, weatherEndDate)
    data = data.fetch()
    data.index = data.index.tz_localize(None)
    data = data[:-1]  # Remove the last row


    # Filter out dates that are not in the stock data
    data = data.loc[data.index.isin(stockData.index)]

    print(data)
    return data

def is_stock_data_valid(stock_data):
    return not stock_data.empty

def plot_data(ticker, weather_variable, location, window):
    try:
        # Get stock data
        stock_data = get_stock_data(stockStartDate, stockEndDate, '1m', ticker)

        # Get weather data
        weather_data = get_weather_data(location, weather_variable,stock_data)
        # Filter weather data to match date range of stock data
        weather_data = weather_data.loc[stock_data.index[0]:stock_data.index[-1], :]

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 4))


        # Plot stock data
        ax.plot(stock_data.index, stock_data['Close'], color='blue')

        # Plot weather data
        ax2 = ax.twinx()
        ax2.plot(stock_data.index, weather_data[weather_variable], color='red')

        # Add labels
        if (weather_variable == "tavg"):
            weather_variable_label = "Temperature (°C)"
        elif (weather_variable == "prcp"):
            weather_variable_label = "Precipitation (mm)"
        elif (weather_variable == "pres"):
            weather_variable_label = "Pressure (atm)"

        ax.set_ylabel('Price')
        ax2.set_ylabel(weather_variable_label)
        ax.set_xlabel('Date')

        # Set x-axis scale to match stock data
        ax.set_xlim([stock_data.index[0], stock_data.index[-1]])

        # Create canvas from figure and add to window
        #canvas = FigureCanvasTkAgg(fig, master=window)
        #canvas.draw()
        #canvas.get_tk_widget().grid()

        #plt.show()
    # Return the figure object
        return fig
    except ValueError as e:
        messagebox.showerror("Error", str(e))

#set_start_date_time(2022, 2, 20)
#set_end_date_time(2023, 2, 25)
#plot_data(agriculture_ticker, '1d', london)




