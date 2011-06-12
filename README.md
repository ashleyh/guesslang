0. Install python 2.7, nltk, and pygments 1.5
1. Put some example files in `data/${language}/`
2. Run `python classifier.py --make` to generate guesser.pickle
3. Run `python classifier.py --test --show` to test and get a nice pretty coloured analysis of the bad files
4. Run `python findshitfiles.py` to show the worst-classified files for each language
5. Run `python classify.py` and type some file paths to see what it thinks they are
6. Run `python classify-web.py` and go to http://127.0.0.1:6789 to have your input classified
