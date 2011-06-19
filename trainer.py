import os

import nltk

from pyglex import  tokenize, ttypes
from util import *
from features import get_features
from guesser import Guesser

def strip_gubbins(txt, lang):
    """
    during training, strip out comments and string literals
    from `txt` using the pygments lexer named `lang`
    """
    result = ""
    for ttype, val in tokenize(lang, txt):
        if ttype in ttypes.Comment:
            result += 'COMMENT'
        elif ttype in ttypes.Literal:
            result += 'LITERAL'
        else:
            result += val
    return result

class Trainer(object):
    """
    produces a `Guesser`. feed it some examples with `consume`
    and then extract the `Guesser` with `make_guesser`.
    """
    def __init__(self):
        self.featuresets = []

    def consume(self, lang, source):
        source = strip_gubbins(source, lang)
        featureset = get_features(source)
        self.featuresets.append((featureset, lang))

    def make_guesser(self):
        print 'total featuresets', len(self.featuresets)
        classifier = nltk.NaiveBayesClassifier.train(self.featuresets)
        return Guesser(classifier)

    def train_on_dir(self, dir):
        print 'training from', dir
        for lang, path in file_walker(dir):
            with open(path, 'r') as f:
                self.consume(lang, f.read())

