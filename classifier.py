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
import pyglex
from collections import defaultdict
import re
import sys
import argparse

 




def main(argv):
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
    args = argparser.parse_args(argv)

    if not any([args.make, args.test, args.show]):
        argparser.print_help()
        return 1

    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, 'data')
    

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
    main(sys.argv)
