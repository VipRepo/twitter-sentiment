import nltk
import random
import re
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

ps = PorterStemmer()
pos_tweet_file_id = 'negative_tweets.json'
neg_tweet_file_id = 'positive_tweets.json'

pos_tweets = twitter_samples.strings(pos_tweet_file_id)
neg_tweets = twitter_samples.strings(neg_tweet_file_id)
stop_words = stopwords.words('english')
my_stop_words = ['I', 'u']

stop_words.extend(my_stop_words)

stop_words = set(stop_words)

all_words = []
filtered_pos_tweets = []
filtered_neg_tweets = []
allowed_word_types = ["J"]

def clean_tweet(tweet):
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    word_tokens = word_tokenize(tweet)
    words_tokens = [w.lower() for w in word_tokens]
    #Removing Stop words
    word_tokens = [w for w in word_tokens if not w in stop_words]
    #Stemming
    stemmed_word_tokens = [ps.stem(w) for w in word_tokens]
    return stemmed_word_tokens


for pos_tweet in pos_tweets:
    word_tokens = clean_tweet(pos_tweet)
    pos = nltk.pos_tag(word_tokens)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
    #all_words.extend(word_tokens)
    filtered_pos_tweets.append((word_tokens, 'pos'))

for neg_tweet in neg_tweets:
    word_tokens = clean_tweet(neg_tweet)
    pos = nltk.pos_tag(word_tokens)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
    #all_words.extend(word_tokens)
    filtered_neg_tweets.append((word_tokens, 'neg'))

documents = filtered_pos_tweets + filtered_neg_tweets

save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]

save_word_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

#print(len(word_features))
#print(all_words.most_common(15))

def find_features(document):
     words = set(document)
     features = {}
     for w in word_features:
         features[w] = (w in words)
     return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

featuresets_f = open("pickled_algos/featuresets.pickle","wb")
pickle.dump(featuresets, featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
print(len(featuresets))

# set that we'll train our classifier with
training_set = featuresets[:9000]

# set that we'll test against.
testing_set = featuresets[9000:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)

save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()


##NuSVC_classifier = SklearnClassifier(NuSVC())
##NuSVC_classifier.train(training_set)
##print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()

