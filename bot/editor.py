import pandas as pd
import csv


unfiltered_text = list()
filtered_text = list()
row_tweet = list()

def filter(file_path):


    editable_file = pd.read_csv(file_path)

    for tweet in editable_file['﻿﻿tweet']:
        if ',' in tweet:
            index_number = editable_file[editable_file['﻿tweet'] == tweet].index.values
            if file_path == 'control_questions':
                sentiment = editable_file['class'][index_number[0]]
                unfiltered_text.append((tweet,sentiment))
            else:
                tweet_id = editable_file['tweet_id'][index_number[0]]
                unfiltered_text.append((tweet_id, tweet))

    for tweet_class in unfiltered_text:
        with open(file_path, 'a', encoding='utf8') as f:
            writer = csv.writer(f)
            if file_path == 'control_questions':
                writer.writerow([tweet_class[0].replace(',',''), tweet_class[1]])
            else:
                writer.writerow([tweet_class[0], tweet_class[1]].replace(',',''))


    data = pd.read_csv(file_path, encoding= "utf8", index_col  = '﻿tweet')
    for tweet in unfiltered_text:
        data.drop([tweet[0]], inplace=True)

filter('raw_tweets.csv')




