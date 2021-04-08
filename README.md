# stock-prediction

#### Scripts

- `twitter.sh`

   ```
   chmod +x twitter.sh
   ./twitter.sh
   ```

   Set variable iter\runtime to adjust the running time/iteration of fetch/read scripts.
   i.e if we fetch 60 min of data, sliced each 5 min, then runtime = 300, iteration = 12

   The data produced are stored in data/tweetParsed, data/tweetRaw folders.

- `fetch_stream_tweets.py`

  uses `tweepy` library to extract streaming tweeter data for a certain period of time


- `read_stream_tweets.py`

  uses `pandas` library to read and parse the tweeter data and outputs a csv file


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
  
- `process_join_data.py`


  - process tweets and stock data, and join them to be outputted to `data/data_processed/` folder as a csv file
  - should be run in main directory

  note:

  - `window_size=10` : look at stock price changes 10 minutes after the tweet's create time
  - `trend`: 1 represents increasing, -1 represents decreasing, 0 otherwise

  > example of processed stock data:

  ![](pics/stock-data-example.png)

  
