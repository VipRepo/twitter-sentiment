import nltk
import random
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

pos_tweet_file_id = 'negative_tweets.json'
neg_tweet_file_id = 'positive_tweets.json'

pos_tweets = twitter_samples.strings(pos_tweet_file_id)
stop_words = set(stopwords.words('english'))

filtered_pos_tweets = []

for pos_tweet in pos_tweets:
    word_tokens = word_tokenize(pos_tweet)
   
    # Removing Stop words
    word_tokens = [w for w in word_tokens if not w in stop_words]

    #Stemming
    
    filtered_pos_tweets.append((word_tokens, 'pos'))

print(filtered_pos_tweets[0])
