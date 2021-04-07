#!/bin/bash

# Run scripts iter times for runtime secs
let iter=3
let runtime=10

baseFetchOutpath="data/tweetRaw/tweet_data_raw_"
baseReadInpath="data/tweetRaw/tweet_data_raw_"
baseReadOutpath="data/tweetParsed/tweet_data_parsed_"

for i in `seq 1 $iter`;
do python scripts/fetch_stream_tweets.py $runtime ${baseFetchOutpath}${i};
done

echo "Fetch Done."

for i in `seq 1 $iter`;
do python scripts/read_stream_tweets2.py ${baseReadInpath}${i} ${baseReadOutpath}${i};
done

echo "Read Done."