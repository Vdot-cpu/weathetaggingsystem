import unittest
from datetime import datetime

from main import *


class TestWeatherStockAnalysis(unittest.TestCase):

    def test_set_start_date_time(self):
        # Test case 1
        stockStartDate, weatherStartDate = set_start_date_time(2023, 2, 17)
        self.assertEqual(stockStartDate, '2023-2-17')
        self.assertEqual(weatherStartDate, datetime(2023, 2, 17))

        # Test case 2
        stockStartDate, weatherStartDate = set_start_date_time(2021, 12, 1)
        self.assertEqual(stockStartDate, '2021-12-1')
        self.assertEqual(weatherStartDate, datetime(2021, 12, 1))

    def test_set_end_date_time(self):
        # Test case 1
        stockEndDate, weatherEndDate = set_end_date_time(2023, 2, 24)
        self.assertEqual(stockEndDate, '2023-2-24')
        self.assertEqual(weatherEndDate, datetime(2023, 2, 24))

        # Test case 2
        stockEndDate, weatherEndDate = set_end_date_time(2021, 12, 31)
        self.assertEqual(stockEndDate, '2021-12-31')
        self.assertEqual(weatherEndDate, datetime(2021, 12, 31))

    def test_stock_data_validity(self):
        # Test case 1: Valid stock
        valid_ticker = yf.Ticker("AAPL")
        valid_stock_data = get_stock_data('2021-01-01', '2021-01-31', '1d', valid_ticker)
        self.assertTrue(is_stock_data_valid(valid_stock_data))

        # Test case 2: Invalid stock
        invalid_ticker = yf.Ticker("INVALID")
        invalid_stock_data = get_stock_data('2021-01-01', '2021-01-31', '1d', invalid_ticker)
        self.assertFalse(is_stock_data_valid(invalid_stock_data))

    def test_weather_data_validity(self):
        london = Point(51.5074, -0.1278)
        stockStartDate, weatherStartDate = set_start_date_time(2021, 1, 1)
        stockEndDate, weatherEndDate = set_end_date_time(2021, 12, 31)

        stock_data = get_stock_data(stockStartDate, stockEndDate, '1d', apple_ticker)

        weather_data = get_weather_data(london, 'tavg', stock_data)

        self.assertFalse(weather_data.empty, msg="Weather data should not be empty")
        self.assertTrue('tavg' in weather_data.columns, msg="Weather data should have a 'tavg' column")


if __name__ == '__main__':
    unittest.main()