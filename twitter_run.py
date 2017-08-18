from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import re
import classifier_run as classifier

#consumer key, consumer secret, access token, access secret.
ckey="x95BeZk7sOKw2Vk3473V8EJbX"
csecret="QKHc6Tt1CnDUqUWhw6hw2ocZcS9XOkz40oYieLs3vyOpOOwR55"
atoken="773834086377021441-vuM1wsFoFe9M0cA5Z0J6JMoWeCy54X3"
asecret="N2VZQr5n1IV3MsTUfZsOo9fSI4MF0OcaOgMju7AgIHHmk"


def get_pages_to_follow():
#    pages_to_follow = ['@EconomicTImes','@CNBC', '@moneycontrolcom', '@business']
    pages_to_follow = ['@Sentime36444626'] 
    return pages_to_follow

def get_mf_id_mgr_mapping():
    map = {}
    map['12341'] = 'Vinit Sambre'
    map['12342'] = 'Jinesh Gopani'
    map['12343'] = 'Sohini Adani'
    map['12344'] = 'Mrinal Singh'
    return map


#pages_to_follow = ['@EconomicTImes','@CNBC', '@moneycontrolcom', '@business']
#pages_to_follow = ['@Sentime36444626']
pages_to_follow = get_pages_to_follow()

#fund_managers = ['Vinit Sambre', 'Jinesh Gopani', 'R. Janakiraman','Sohini Adani', 'Mrinal Singh']
mf_id_mgr_map = get_mf_id_mgr_mapping()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

API = tweepy.API(auth)

tweets = []
collected_mf_tweet_map = dict.fromkeys(get_mf_id_mgr_mapping())

for k, v in collected_mf_tweet_map.items():
    collected_mf_tweet_map[k] = []

for page in get_pages_to_follow():
    tweet_page = API.user_timeline(page, count=10)
    for tweet in tweet_page:
        for k, v in get_mf_id_mgr_mapping().items():
            if v in tweet.text:
#                print('Key: '+k+' Value:'+v+' Tweet: '+tweet.text)
                collected_mf_tweet_map[k].append(tweet.text)

#print(str(collected_mf_tweet_map))

mf_popularity_map = {}

for k, v in collected_mf_tweet_map.items():
    total_tweets = len(v)
    pos_tweets = 0
    for tweet in v:
        if classifier.sentiment(tweet)[0] == 'pos':
            pos_tweets = pos_tweets + 1
    if total_tweets != 0:
        pos_perc = pos_tweets/total_tweets
        neg_perc = (total_tweets - pos_perc)/total_tweets
    else:
        pos_perc = 0
        neg_perc = 0
    mf_popularity_map[k] = pos_perc - neg_perc

print(str(mf_popularity_map))

        

