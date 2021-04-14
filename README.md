# stock-prediction

#### Scripts

All scripts should be running under Python 3.6.

- `twitter.sh`

  ```
  python3 -m pip install tweepy
  python3 -m pip install progressbar
  python3 -m pip install pandas
  python3 -m pip install textblob
  python3 -m pip install emojis

  chmod +x twitter.sh
  ./twitter.sh [iteration] [runtime] [date]
  ```

  1. Use `progressbar` library to display script running progess.
  2. Set command line arg `iteration` to adjust how many iterations to run.
  3. Set command line arg `runtime` to adjust how long to run in seconds for each iteration.
  4. Set command line arg `date` to adjust the date of running.
  5. Raw tweet jsons are stored in `data/tweet_raw_[date]/*`.
  6. Processed csv files are stored in `data/tweet_parsed_[date]/*`.

  ```
  # If we fetch 6 hours of real-time data, 30 min each set on 13rd April, then run twitter.sh:
  $ ./twitter.sh 12 1800 0413
  ```

- `fetch_stream_tweets.py`

  ```
  pip3 install tweepy
  python3 scripts/fetch_stream_tweets [runtime in seconds] [output_path]
  ```

  uses `tweepy` library to extract streaming tweeter data for a certain period of time

- `read_stream_tweets.py`

  ```
  pip3 install textblob
  python3 scripts/read_stream_tweets [input_path] [output_path]
  ```

  uses `pandas` library to read and parse the tweeter data and outputs a csv file
  uses `textblob` library to access the sentiment score of tweet content

- `extract_stock.py`

  uses `yfinance` library to extract stock data for a certain company everyday from 2020-11-01 to 2020-12-01

  ```
  pip3 install yfinance
  ```

  - change `ticker_name` to desired company name in the script

  - change `interval` if you want to extract with different frequencies (ie, stock price change every minute/ hour/ etc.)

  - Run in main directory `/stock_prediction`, and output `stock_data.csv` file will be in `/data` folder

- `pandas_predict.py`

  - debug purpose, use it to test ml framework without pyspark

- `pyspark_predict.py`

  - change `global_setup` part to debug

- `process_join_data.py`

  ```
  python3 process_join_data.py [target_date]
  python3 process_join_data.py 0409
  ```

  - process tweets for hashtags. outputted to `data/tweet_processed_{target_date}/` folder as a csv file
  - process tweets and stock data, and join them to be outputted to `data/data_processed/` folder as a csv file
  - should be run in main directory
  - make sure you have `data/stock_data.csv` before running

  note:

  - `window_size=10` : look at stock price changes 10 minutes after the tweet's create time
  - `trend`: 1 represents increasing, -1 represents decreasing, 0 otherwise

- `pyspark_rf_train.py`

  - take input of `data/data_processed/*.csv` as training (and testing, for now) data
  - train 5 folds cv random forest model on numerical data
    - customize 1: change `max_trees`, max amount of random forests generated
    - customize 2: change `maxDepth`, max depth of each random forest
    - customize 3: change `minInstancesPerNode`, minimum distance of each subnode, currently calculated using Gini index
  - output to `data/data_prediction/`
  - run in main directory

- `cnn_train.py`

  - install anaconda
  - install tensorflow in anaconda
  - take input of `data/data_processed/*.csv` as training data
    - customize 1: change `BATCH_SIZE`, number of data processed in one iteration
    - customize 2: change `epochs`
  - run in main directory

- `lstm_train.py`

  - currently using manual one-hot encoding, next: embedding text
  - run in main directory

#### Features

- `Sentiment_Score`

- `Emoji_Score`
