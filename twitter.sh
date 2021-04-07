#!/bin/bash

# Run scripts n times
let iter=10
basepath="data/tweets/tweet_data_raw_"

for i in `seq 1 $iter`;
do python scripts/fetch_stream_tweets.py 5 ${basepath}${i};
done
