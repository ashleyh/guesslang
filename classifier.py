# classifier.py: build a language classifier
#
# Copyright 2011 Ashley Hewson
# 
# This file is part of Compiler Zoo.
# 
# Compiler Zoo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Compiler Zoo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Compiler Zoo.  If not, see <http://www.gnu.org/licenses/>.

import nltk
import random
import sys
import re
import os
import cPickle as pickle
from pyglex import  tokenize, ttypes
import pyglex
from collections import defaultdict
import re
import sys
from pygments.console import ansiformat
import argparse

 
def get_language(fn):
    """
    guess the language based on filename `fn`. return
    the name of the appropriate pygments lexer.
    """
    lang = pyglex.get_language(fn)
    if lang == "C" :
        lang = "C++"
    return lang

# make experiments a bit more reproducible
random.seed(1)

# words that will be escaped and wrapped in \b ... \b
words_a = '''
    def int char const while return if printf strcmp
    strchr puts else typedef struct void memcpy malloc
    sizeof NULL unsigned for nil end do true false float
    __attribute__ require class self public synchronized
    static String new equals boolean throw toString import
    package java org interface this private double
    Length echo use my qw local shift sub next function
    null try catch finally var array string set or and foreach
    switch case break using namespace Object Iterable css
    print where let in System println _SESSION _POST
    virtual template prototype implicit val _ php perl
    len None True False final override pass module then
    of document window extends sys os python alert 
    cout FILE fopen fclose Maybe typeof say elif __init__
    from except bool object type each sealed abstract 
    instance data deriving delegate chomp toArray toList
    asInstanceOf @property del implements reinterpret_cast
    delete @Override Integer
'''.split()

# words that will be escaped but won't be wrapped in \b ... \b
words_b = '''
    ; * ++ ( ) { } & === == ? : | =~ @ ::~ :: . -> $ .= -> , => `
    << \ >> <% %> <: :> < > [ ] $(
'''.split()

# plain regexes
others = [
    # c preprocessor
    r'#\s*include\s*<.*>',
    r'#\s*include\s*".*"',
    r'#\s*define\s+.*',
    r'#\s*ifdef\s+.*',
    r'#\s*endif',
    r'#\s*undef\s+.*',
    # $igils for perl
    r'\$\w+',
    # python's ubiquitous :
    r':$',
    # generics for java/c#
    r'List\s*<',
    # TitleCase for c#/go
    r'\b[A-Z][a-z]+[A-Z]',
    # camelCase for java
    r'\b[a-z]+[A-Z][a-z]+',
    # ALLCAPS for c constants
    r'[A-Z]{3,}',
    # json
    r'\{\s*\w+:',
    # java's foreach
    r'for\s*\([^;]+\)\s*\{',
    # scala's type annotations
    r'var\s+\w+:',
    # javascript closure idiom
    r'\(\s+function\s+\(',
    # python's pass on a line by itself
    r'^\s+pass\s*$',
    # ruby's end on a line by itself
    r'^\s*end\s*$',
    # shebang
    r'^#!/',

]

def find_all(txt):
    """
    iterate over non-overlapping features in txt
    yielding `{name of regex}, {extents in txt}` for each
    """
    # note: matching seems to be first-match rather than
    # longest match
    # each plain regexp gets its own group and the words
    # get lumped together in a single group at the end
    regexp = (
        "|".join('(' + r + ')' for r in others)
        + "|(" +
        "|".join(r'\b' + re.escape(word) + r'\b' for word in words_a)
        + "|" +
        "|".join(re.escape(word) for word in words_b)
        + ")"
    )
    for match in re.finditer(regexp, txt):
        i = match.lastindex - 1
        if i < len(others):        
            r = others[i]
        else:
            r = match.group()
        yield r, match.span()

def get_features(txt):
    """
    return a nltk featureset for `txt`
    """
    featureset = {}
    for feature in words_a + words_b + others:
        featureset['has('+feature+')'] = False
    for r, _ in find_all(txt):
        featureset['has('+r+')'] = True
    return featureset
        
       
def highlight(source):
    """
    write `source` to stdout, highlighting all the found
    features (in purple, of course)
    """
    last_end = 0
    attr = '*purple*'
    for _, (start, end) in find_all(source):
        sys.stdout.write(source[last_end:start])
        sys.stdout.write(ansiformat(attr, source[start:end]))
        last_end = end
    sys.stdout.write(source[last_end:])

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

# these are pygments lexer names
languages_i_claim_to_know = set([
    'Ruby',  'JavaScript', 'PHP', 'Perl', 'C#', 'Go',
    'Haskell', 'Java', 'C++', 'Scala', 'Objective-C', 'Python'
])

def file_walker(top):
    """
    for each interesting file under `top`, yield `{language}, {path}`
    """
    for dirpath, dirnames, filenames in os.walk(top):
        # hopefully avoid consuming multiple versions of the same file
        for exclude in ('.git', '.svn', '.hg'):
            if exclude in dirnames:
                dirnames.remove(exclude)

        for filename in filenames:
            path = os.path.join(dirpath, filename)
            real_language = get_language(filename)
            if real_language not in languages_i_claim_to_know:
                continue
            if any(filename.endswith(exclude) for exclude in ('.h',)):
                continue
            yield real_language, path

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

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--make', action='store_true',
        help='generate the pickle'
    )
    argparser.add_argument(
        '--test', action='store_true',
        help='test the guesser'
    )
    argparser.add_argument(
        '--show', action='store_true',
        help='show details about bad files (requires --test)'
    )
    args = argparser.parse_args()

    # collect all the interesting paths
    lang_paths = defaultdict(list)
    for lang, path in file_walker('data'):
        lang_paths[lang].append(path)

    # feed some of them to the trainer, and leave the rest
    # in `lang_paths` for testing
    trainer = Trainer()
    for lang, paths in lang_paths.items():
        total = len(paths)
        train_count = min(total//2, 300)
        random.shuffle(paths)
        if args.make:
            print 'Training', lang, 'with', train_count, 'of', total
            for i in range(train_count):
                with open(paths[i], 'r') as f:
                    trainer.consume(lang, f.read())
        paths[train_count:] = []

    if args.make:
        print 'building guesser'
        guesser = trainer.make_guesser()
        guesser.classifier.show_most_informative_features(20)

        print 'pickling'
        with open('guesser.pickle', 'w') as f:
            pickle.dump(guesser, f)
    else:
        with open('guesser.pickle', 'r') as f:
            guesser = pickle.load(f)

    if args.test:
        total_tests = 0
        total_correct = 0
        bad = []
        for lang, paths in lang_paths.items():
            correct = 0
            for path in paths:
                with open(path, 'r') as f:
                    source = f.read()
                guess = guesser.guess(source)
                if lang == guess:
                    correct += 1
                    total_correct += 1
                else:
                    bad.append((path, lang, guess, source))
            print lang, float(correct)/float(len(paths))
            total_tests += len(paths)

    if args.show and args.test:
        # show mislabelled files
        print 'overall', float(total_correct)/float(total_tests)
        random.shuffle(bad)
        for path, lang, guess, source in bad:
            print path
            print lang, guess
            source = dumb_strip(source)
            highlight(source)
            print
            try:
                raw_input('type <enter> to continue or ^D to quit')
            except EOFError:
                print
                break

                

if __name__ == '__main__':
    main()
