# stock-prediction

#### Scripts

- `fetch_stream_tweets.py`

  uses `tweepy` library to extract streaming tweeter data for a certain period of time

  ```
  pip install tweepy
  python scripts/fetch_stream_tweets.py `runtime`
  ```

  - Run in main directory `/stock_prediction` , and output `tweet_data_raw` file will be in `/data` folder

- `read_stream_tweets.py`

  uses `pandas` library to read and parse the tweeter data and outputs a csv file

  ```
  python scripts/read_stream_tweets.py
  ```

  - Run in main directory `/stock_prediction` , and output `tweet_data_parsed.csv` file will be in `/data` folder

- `extract_stock.py`

  uses `yfinance` library to extract stock data for a certain company everyday from 2020-11-01 to 2020-12-01

  ```
  pip install yfinance
  ```

  - change `ticker_name` to desired company name in the script

  - change `interval` if you want to extract with different frequencies (ie, stock price change every minute/ hour/ etc.)

  - Run in main directory `/stock_prediction`, and output `stock_data.csv` file will be in `/data` folder

- `pandas_predict.py`

  - debug purpose, use it to test ml framework without pyspark

  - change absolute path to relative path accordingly

- `pyspark_predict.py`

  - change `global_setup` part to debug

  - change absolute path to relative path accordingly
