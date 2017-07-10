import tweepy
import indicoio
#import pandas as pd
#import numpy as np
#from textblob import TextBlob
import ConfigKeys

#Twitter API credentials
consumer_key = ConfigKeys.twitter_consumer_key
consumer_secret = ConfigKeys.twitter_consumer_secret

access_token = ConfigKeys.twitter_access_token
access_token_secret = ConfigKeys.twitter_access_token_secret

#Indicoio api credentials
indicoio.config.api_key = ConfigKeys.indicoio_api_key

#Auth object and twitter API connection
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Search parameters
keywords = ['venezuela', 'maduro']
max_tweets = 500
result_type = ['popular', 'recent', 'mixed']

#Search

query = ''
for keyword in keywords:
    if query == '':
        query = keyword + ' OR ' + keyword.capitalize()
    else:
        query = query + ' OR ' + keyword + ' OR ' + keyword.capitalize()

last_id = -1

searched_tweets = []

while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1), result_type = result_type[2])
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

# Filter duplicates/retweets
printed = []
filtered_tweets = []

for tweet in searched_tweets:
    try:
        if tweet.retweeted_status.id not in printed:
            filtered_tweets.append(tweet.retweeted_status)
            #print(tweet.retweeted_status.id)
            #print(tweet.retweeted_status.text + "\n")
            printed.append(tweet.retweeted_status.id)
    except AttributeError:
        if tweet.id not in printed:
            filtered_tweets.append(tweet)
            #print(tweet.id)
            #print(tweet.text + "\n")
            printed.append(tweet.id)
    # if tweet.id not in printed:
    #     print(tweet.id)
    #     print(tweet.text + "\n")
    #     printed.append(tweet.id)
        #tweet.
    #analysis = TextBlob(tweet.text)
    #print(indicoio.sentiment(tweet.text))
    #print(indicoio.political(tweet.text))

# Sort tweets by retweets
filtered_tweets.sort(key=lambda tweet: tweet.retweet_count, reverse=True)

# Print out the tweets
for tweet in filtered_tweets:
    print('id: ' + str(tweet.id))
    print('Retweets: ' + str(tweet.retweet_count))
    print('Favorites: ' + str(tweet.favorite_count))
    print(tweet.text + "\n")

    # Print the Quoted tweet, if any 
    try:
        nuTweet = tweet.quoted_status
        print('Quoted status:')
        print('id: ' + str(tweet.quoted_status['id']))
        print('Retweets: ' + str(tweet.quoted_status['retweet_count']))
        print('Favorites: ' + str(tweet.quoted_status['favorite_count']))
        print(tweet.quoted_status['text'] + "\n")

    except AttributeError:
        pass