#!/bin/bash

# Run scripts iter times for runtime secs
let iter=1
let runtime=10

baseFetchOutpath="data/tweetRaw/tweet_data_raw_"
baseReadInpath="data/tweetRaw/tweet_data_raw_"
baseReadOutpath="data/tweetParsed/tweet_data_parsed_"

for i in `seq 1 $iter`;
do python3 scripts/fetch_stream_tweets.py $runtime ${baseFetchOutpath}${i};
done

echo "Fetch Done."

for i in `seq 1 $iter`;
do python3 scripts/read_stream_tweets.py ${baseReadInpath}${i} ${baseReadOutpath}${i};
done

echo "Read Done."

do python3 scripts/process_join_data.py
echo "Process Done"