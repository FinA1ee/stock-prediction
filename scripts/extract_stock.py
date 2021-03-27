# ensure that you already installed yfinance library
# pip install yfinance

import yfinance as yf
import csv

ticker_list = ["TSLA"]
for t in ticker_list:
    cpny = yf.Ticker(t)
    cpny_stock = cpny.history(
        start="2020-11-01", # (data['created_at'].min()).strftime('%Y-%m-%d'),
        end="2020-12-01", # data['created_at'].max().strftime('%Y-%m-%d'),

        # - valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # - default is '1d'
        # interval='1d' 
    ).reset_index()

    cpny_stock.to_csv("data/stock_data_{}.csv".format(t))
