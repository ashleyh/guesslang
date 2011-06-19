import re

from features import get_features

def dumb_strip(txt):
    """
    during testing, try to strip out comments and string literals
    (without knowledge of the language, obviously)
    """
    return re.sub(r'''
        " [^"]* "
     |  ' [^']* '
     |  /\* (?: [^*] | \* [^/] )*  \*/
     |  // .*
     |  \# (?! \s* (?: include | define | if | ifdef | endif | undef | !)) .*
    ''', 'SPAM', txt, flags=re.X)

class Guesser(object):
    """
    wrapper around the nltk classifier
    """
    def __init__(self, classifier):
        self.classifier = classifier

    def prob_classify(self, source):
        """
        wrapper for `prob_classify` of the nltk classifier
        """
        source = dumb_strip(source)
        featureset = get_features(source)
        return self.classifier.prob_classify(featureset)

    def guesses(self, source):
        """
        return a list of `{probability}, {guess}` from highest to lowest
        """
        dist = self.prob_classify(source)
        result = [(dist.prob(lang), lang) for lang in dist.samples()]
        result.sort(reverse = True)
        return result

    def guess(self, source):
        """
        return best guess for `source`
        """
        return self.guesses(source)[0][1]


