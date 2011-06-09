import nltk
import sys
import pickle
import os
import operator
from features import *

langs = ['c', 'ruby','javascript', 'perl', 'csharp', 'haskell', 'java', 'cpp', 'scala', 'objc', 'python']

f = open("classifier.pickle", "r")
classifier = pickle.load(f)
f.close()

for lang in langs:
  filelist = os.listdir(os.path.join("data", lang))
  featuresets = [(get_features(os.path.join("data", lang, fn)), fn) for fn in filelist]
  fileprob = dict()

  for fs, fn in featuresets:
    fileprob[fn] = classifier.prob_classify(fs).prob(lang)

  sortedworstfiles = sorted(fileprob.iteritems(), key=operator.itemgetter(1))[:10]

  print " == Worst", lang, "files == "
  for (k,v) in sortedworstfiles:
    print k, ":", v
