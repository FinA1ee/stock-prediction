# ensure that you already installed yfinance library
# pip install yfinance

import yfinance as yf
import csv

ticker_list = ["TSLA"]
for t in ticker_list:
    cpny = yf.Ticker(t)
    cpny_stock = cpny.history(
        start="2021-04-07",
        end="2021-04-08",
        interval="1m"
    ).reset_index()

    cpny_stock.to_csv("data/stock_data_realtime_{}.csv".format(t))
