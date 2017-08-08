from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import re

#consumer key, consumer secret, access token, access secret.
ckey="x95BeZk7sOKw2Vk3473V8EJbX"
csecret="QKHc6Tt1CnDUqUWhw6hw2ocZcS9XOkz40oYieLs3vyOpOOwR55"
atoken="773834086377021441-vuM1wsFoFe9M0cA5Z0J6JMoWeCy54X3"
asecret="N2VZQr5n1IV3MsTUfZsOo9fSI4MF0OcaOgMju7AgIHHmk"

pages_to_follow = ['@EconomicTImes','@CNBC', '@moneycontrolcom', '@business']
fund_managers = ['Vinit Sambre', 'Jinesh Gopani', 'R. Janakiraman','Sohini Adani', 'Mrinal Singh']

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

API = tweepy.API(auth)

tweets = []

for page in pages_to_follow:
    tweets.extend(API.user_timeline(page, count=20))

print('Total no of collected tweets:'+ str(len(tweets)))

