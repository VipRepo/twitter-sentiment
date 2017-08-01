from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#consumer key, consumer secret, access token, access secret.
ckey="x95BeZk7sOKw2Vk3473V8EJbX"
csecret="QKHc6Tt1CnDUqUWhw6hw2ocZcS9XOkz40oYieLs3vyOpOOwR55"
atoken="773834086377021441-vuM1wsFoFe9M0cA5Z0J6JMoWeCy54X3"
asecret="N2VZQr5n1IV3MsTUfZsOo9fSI4MF0OcaOgMju7AgIHHmk"

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())

tag = input("Enter the tag to search: ")
twitterStream.filter(track=[tag])
