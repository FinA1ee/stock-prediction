- Idea

Use real-time tweets sent by user to get s sense of the public impression on stock market, and try to quantify it by assigning scores to each tweets, then run LSTM model to train the scores generated on the timeline, to predict a future trend of stock market.

1. Retrieve Data

Use Twitter stream api to retrieve real-time tweets, store as json format
Filter by keywords, we focus on ‘Tesla’, ‘ElonMusk’, ‘SpaceX’…
Slice the data by minute, get 60 data setsParse Data

2. Parse Data

For each data set, we run it through 3 passes:

a. If this tweet contains emoji,
identify the basic unhappy-ish emojis, assign a negative score.  
 identify the basic happy-ish emojis, assign a positive score.

b. If the tweet is retweeted from @ElonMusk, @Tesla…
identify the common negative keywords, assign a negative score.
Else assign a positive score.

c. For all the remaining tweet, they don’t have a obvious impression as above, so we try to identify them as a whole.
Try to find the ( Tesla, [ all forms of buy ] )’s pair PMI p1,
Try to find the ( Tesla, [ all forms of sell ] )’s pair PMI p2
If p1 > p2, then our hypothesis is the remaining tweets have an overall impression of buying, vice-versa.

3. Collect Result

In pass 1 and 2, we apply each score with retweet count and likes count,
For each retweet, we give 1 extra point.
For each like, we give 0.5 extra point.

i.e
Say we have 200 tweets generated from 10:00 - 10:01 am.
For simplicity, assume they each have the 2 retweets and 2 likes.

a. In first pass, we discover 50 tweets with emoji. 20 are negative, 30 are positive.
The score after this would be like:
Pos: 30 _ ( 1 _ #retweet + 0.5 _ #like ) _ 1 = 90
Neg: 20 _ ( 1 _ #retweet + 0.5 _ #like ) _ 1 = 60

b. In second pass, we discover 30 retweets. 20 are negative, 10 are positive.
The score after this would be like:
Pos: 10 _ ( 1 _ #retweet + 0.5 _ #like ) _ 1 = 30
Neg: 20 _ ( 1 _ #retweet + 0.5 _ #like ) _ 1 = 60

c. In third pass, there are 200 - 50 - 30 = 120 tweets yet to be assigned.
Since we care about overall impression, we don’t include specific likes/retweets.
After running PMI MapReduce jobs, we discover
PMI ( Tesla, buy ) = 0.18
PMI ( Tesla, sell ) = 0.16
We apply the rule of majority wins, so score is 120.

After 3 pass,
the total pos score is 90 + 30 + 120 = 240
the total neg score is 60 + 60 = 120

For each data set, we collect a score result like this.

- Prediction
  Run the CSV in LSTM training model, 50 training sets and 10 testing sets, we predict
  What the scores would look like in the next 5 minutes, if positive score is higher, our
  hypothesis is that the stock market

- Methodology

1. Big Data source: Real-time social media data filtered by keywords
2. Python scripts to retrieve data using twitter apis, loads data into json format
3. Use Spark Framework to perform MapReduce job on the time-sliced data sets
4. Use LSTM model to train and make prediction
5. Compared with ground truth data to see if our trend is correct

- Implementation
  // To Do

- Result
  // To Do
