import tweepy
import csv

# Credenziali per l'API di twitter
consumer_key = "####"
consumer_secret = "####"
access_token = "####"
access_token_secret = "####"

# Login 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

csvFile = open('desktop/tweet/tweetIta.csv', 'a')
csvWriter = csv.writer(csvFile)

# Scarico i tweet in lingua italiana che contengono la parola 'musica'
for tweet in tweepy.Cursor(api.search, lang="it",  q="musica", tweet_mode="extended").items(1000):
        if not (hasattr(tweet, 'retweeted_status')):
                csvWriter.writerow([tweet.user.screen_name,
                                    tweet.full_text.replace("\n", "")])

        if (hasattr(tweet, 'retweeted_status')): # Per i retweet
                csvWriter.writerow([tweet.user.screen_name,
                                    tweet.retweeted_status.full_text.replace("\n", "")])













