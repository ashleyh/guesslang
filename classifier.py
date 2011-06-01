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
  [("data/php/"+fn, "php") for fn in os.listdir("data/php")] + \
  [("data/csharp/"+fn, "csharp") for fn in os.listdir("data/csharp")] + \
  [("data/java/"+fn, "java") for fn in os.listdir("data/java")] + \
  [("data/cpp/"+fn, "cpp") for fn in os.listdir("data/cpp")] + \
  [("data/python/"+fn, "python") for fn in os.listdir("data/python")]

featuresets = [(get_features(fn), g) for (fn,g) in files]

random.shuffle(featuresets)
count = len(featuresets)
print "Total featuresets: ", count

train_set, test_set = featuresets[count/2:], featuresets[:count/2]

classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set)

print classifier.show_most_informative_features(20)


print "Writing to file"

f = open("classifier.pickle", "w")
pickle.dump(classifier, f)
f.close()
