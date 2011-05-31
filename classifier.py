from nltk.corpus import names
import nltk
import random
import sys
import re
import os
import pickle
from features import *

files = [("data/ruby/"+fn, "ruby") for fn in os.listdir("data/ruby")] + \
  [("data/c/"+fn, "c") for fn in os.listdir("data/c")] +  \
  [("data/js/"+fn, "js") for fn in os.listdir("data/js")] + \
  [("data/python/"+fn, "python") for fn in os.listdir("data/python")]

featuresets = [(get_features(fn), g) for (fn,g) in files]

random.shuffle(featuresets)
train_set, test_set = featuresets[2000:], featuresets[:2000]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set)

print classifier.show_most_informative_features(10)


print "Writing to file"

f = open("classifier.pickle", "w")
pickle.dump(classifier, f)
f.close()
