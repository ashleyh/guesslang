import sys
import cPickle as pickle
import os
import operator
from collections import defaultdict
from classifier import file_walker, Guesser

with open('guesser.pickle', 'r') as f:
    guesser = pickle.load(f)

lang_paths = defaultdict(list)
for i, (lang, path) in enumerate(file_walker('data')):
    if i % 100 == 0:
        print i, 'files done'
    with open(path, 'r') as f:
        source = f.read()
    prob = guesser.prob_classify(source).prob(lang)
    lang_paths[lang].append((path, prob))

for lang, paths in lang_paths.items():
    print " == Worst", lang, "files == "
    for path, prob in sorted(paths, key=operator.itemgetter(1))[:10]:
        print path, ':', prob

    

