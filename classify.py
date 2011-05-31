import pickle
import nltk
import sys
from features import *

f = open("classifier.pickle", "r")
classifier = pickle.load(f)
f.close()

while 1:
  name = sys.stdin.readline().strip()
  if name == 'quit':
    break
  
  try:
    probs = classifier.prob_classify(get_features(name))
    for label in probs.samples():
      print label.rjust(10), '%.10f' % probs.prob(label)
  except:
    print "Error!"
