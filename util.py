import os

import pyglex

from . import languages_i_claim_to_know

def get_language(fn):
    """
    guess the language based on filename `fn`. return
    the name of the appropriate pygments lexer.
    """
    lang = pyglex.get_language(fn)
    if lang == "C" :
        lang = "C++"
    return lang

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

