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

- `pyspark_rf_train.py`


  - take input of `data/data_processed/*.csv` as training (and testing, for now) data
  - train 5 folds cv random forest model on numerical data
    + customize 1: change max_trees, max amount of random forests generated
    + customize 2: change maxDepth, max depth of each random forest
    + customize 3: change minInstancesPerNode, minimum distance of each subnode, currently calculated using Gini index
  - output to `data/data_prediction/`
  - run in main directory

  > note: change the `Trend` in `process_join_data.py` from -1 to 0 for the model to understand it is categorical

  > todo1: the indexes are messed up by cross-validation, need to fix it

  > todo2: need more data, current prediction is not useful since there is only one Trend

