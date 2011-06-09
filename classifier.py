from nltk.corpus import names
import nltk
import random
import sys
import re
import os
import pickle
from features import *

langs = ['ruby', 'c', 'javascript', 'perl', 'csharp', 'go', 'haskell', 'java', 'cpp', 'scala', 'objc', 'python']

featuresets = dict()
testsets = dict()
trainset = []

for lang in langs:
  filelist = os.listdir(os.path.join("data", lang))
  featuresets[lang] = [(get_features(os.path.join("data", lang, fn)), lang) for fn in filelist]
  random.shuffle(featuresets[lang])

  print "Total " + lang + " featuresets: " + str(len(featuresets[lang]))

for (lang, featureset) in featuresets.items():
  total = len(featureset)
  train_count = 300 if total/2 > 300 else int(total/2)
  
  train_set, test_set = featureset[:train_count], featureset[train_count:]
  trainset = trainset + train_set
  testsets[lang] = test_set

print "Total training featuresets: " + str(len(trainset))

classifier = nltk.NaiveBayesClassifier.train(trainset)

for (lang, test_set) in testsets.items():
  print "Accuracy for " + lang + " is.. " + str(nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(20)


print "Writing to file"

f = open("classifier.pickle", "w")
pickle.dump(classifier, f)
f.close()
