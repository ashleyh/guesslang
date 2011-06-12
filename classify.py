import pickle
import nltk
import sys
from classifier import Guesser

with open('guesser.pickle', 'r') as f:
    guesser = pickle.load(f)

print 'type a path or ^D to quit'
while True:
    try:
        name = raw_input('>')
    except EOFError:
        break

    try:
        with open(name, 'r') as f:
           source = f.read()
    except:
        print 'error!'
    else:
        for prob, lang in guesser.guesses(source):
            print lang.rjust(10), '%.10f' % prob
