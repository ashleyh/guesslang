from pygments.lexers import find_lexer_class, get_all_lexers
from pygments import lex
import pygments.token
import pygments.util
import fnmatch
import re
from debork import timeout, Timeout

def tokenize(language, source):
    # have you found yourself looking here after getting a UnicodeDecoeError?
    # thought so. i think upgrading to pygments 1.5 should do the trick.
    lexer = find_lexer_class(language)(encoding='guess')
    return lex(source, lexer)

ttypes = pygments.token

def pseudo_tokenize(language, source):
    try:
        with timeout(2):
            tokens = list(tokenize(language, source))
    except Timeout:
        return

    interesting_tokens = [] 
    ttypes = pygments.token
    magic = '!"$%^&*"$%^&*' # ahem.

    for ttype, val in tokenize(language, source):
        if ttype in ttypes.Keyword or ttype in ttypes.Operator or \
            ttype in ttypes.Name or ttype in ttypes.Punctuation:
            interesting_tokens.append(val)
        elif ttype in ttypes.Error or ttype in ttypes.Other:
            interesting_tokens.append(magic+'error')
        elif ttype in ttypes.Comment:
            interesting_tokens.append(magic+'comment')
        elif ttype in ttypes.Literal:
            interesting_tokens.append(magic+'literal')
        elif ttype in ttypes.Text:
            pass
        else:
            print 'unknown token', ttype, val

    for token in interesting_tokens:
        yield token

    # woo tokenwise n-grams
    for token1, token2 in zip(interesting_tokens, interesting_tokens[1:]):
        yield token1 + ' ' + token2

# super-duper fast version of pygment's `get_lexer_for_filename` or whatever
# it's called
pattern_cache = []

for name, aliases, patterns, mimetypes in get_all_lexers():
    for pattern in patterns:
        regexp = re.compile(fnmatch.translate(pattern))
        pattern_cache.append((name, regexp))

def get_language(filename):
    found_index = None
    found_name = None

    for i, (name, regexp) in enumerate(pattern_cache):
        if regexp.match(filename) is not None:
            found_index = i
            found_name = name
            break

    if found_index is None:
        return None
    
    if found_index > 1:
        # bring this one to the front on the assumption
        # that there will be clumps of files with the same
        # extension
        obj = pattern_cache[found_index]
        del pattern_cache[found_index]
        pattern_cache.insert(0, obj)

    return name

