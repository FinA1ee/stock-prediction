# stock-prediction

Instructions:

1. Run $ python fetchStreamTweets.py ['runtime'] (runtime must be an integer in range [1, 100])
2. Run $ python readData.py

Functionality:

Streaming all tweets with certain keywords for a period of time,
parse and extract the content text, store them in ../data/tweetParsed.



#### Scripts

- `extract_stock.py`

  uses `yfinance` library to extract stock data for a certain company everyday from 2020-11-01 to 2020-12-01

  ```
  pip install yfinance
  ```

  - change `ticker_name` to desired company name in the script

  - change `interval` if you want to extract with different frequencies (ie, stock price change every minute/ hour/ etc.)

  - Run in main directory `/stock_prediction`, and output `stock_data.csv` file will be in `/data` folder

  

  