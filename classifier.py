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
stop_words = set(stopwords.words('english'))
all_words = []
filtered_pos_tweets = []
filtered_neg_tweets = []

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


for pos_tweet in pos_tweets:
    pos_tweet = clean_tweet(pos_tweet)
    word_tokens = word_tokenize(pos_tweet)
    #Removing Stop words
    word_tokens = [w for w in word_tokens if not w in stop_words]
    all_words.extend(word_tokens)
    #Stemming
    #stemmed_word_tokens = [ps.stem(w) for w in word_tokens]
    filtered_pos_tweets.append((word_tokens, 'pos'))

for neg_tweet in neg_tweets:
    neg_tweet = clean_tweet(neg_tweet)
    word_tokens = word_tokenize(neg_tweet)
    #Removing Stop words
    word_tokens = [w for w in word_tokens if not w in stop_words]
    all_words.extend(word_tokens)
    #Stemming
    #stemmed_word_tokens = [ps.stem(w) for w in word_tokens]
    filtered_neg_tweets.append((word_tokens, 'neg'))

documents = filtered_pos_tweets + filtered_neg_tweets

random.shuffle(documents)


all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]
print(all_words.most_common(15))
print(all_words["stupid"])

def find_features(document):
     words = set(document)
     features = {}
     for w in word_features:
         features[w] = (w in words)
     return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

print(len(featuresets))

# set that we'll train our classifier with
training_set = featuresets[:9000]

# set that we'll test against.
testing_set = featuresets[9000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

#SVC_classifier = SklearnClassifier(SVC())
#SVC_classifier.train(training_set)
#print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


#save_classifier = open("hackovation.naivebayes.pickle","wb")
#pickle.dump(classifier, save_classifier)
#save_classifier.close()

voted_classifier = VoteClassifier(classifier,
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  SGDClassifier_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)

print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
print("Classification:", voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)

