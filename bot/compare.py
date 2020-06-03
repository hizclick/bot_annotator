import pandas as pd
data2 = pd.read_csv('raw_tweets.csv', encoding='utf8')
annotated_tweet_ids = data2['tweet_id'].apply(lambda x: str(x)).tolist()
tweet = data2['tweet'].tolist()

id_tweet_raw = {}
for i in range(len(annotated_tweet_ids)-1):
    id_tweet_raw[annotated_tweet_ids[i]]= tweet[i]


data2 = pd.read_csv('annotated_tweets.csv', encoding='utf8')
annotated_tweet_ids = data2['tweet_id'].apply(lambda x: str(x)).tolist()
tweet = data2['tweet'].tolist()

id_tweet_annotated = {}
for an_t_id, t  in zip(annotated_tweet_ids, tweet):
    if id_tweet_raw[an_t_id] != t:
        print("error")
