import re
import sys

from pygments.console import ansiformat

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

