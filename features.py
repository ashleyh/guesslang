import re
import math

def count_relative(search, txt, size):
#  return int(float(len(re.findall(search, txt)))*10000000/float(size)) > 0
#  return float(len(re.findall(search,txt)))/float(size)
  if size == 0:
    return 0
  count = len(re.findall(search, txt))
  return float(count)/float(size)
  #  return len(re.findall(search,txt)) > 0

def has(search, txt, size):
  if txt == 0:
    return False

  if re.search(search, txt):
    return True
  else:
    return False

def crude_token_count(txt):
  search = r'[\w\s]+|[^\w\s]+'
  return len(re.findall(search, txt))  

def code_features(txt):
  size = crude_token_count(txt)
  
  features = {
    'has(<-)': has('<-', txt, size),
    'has(|)': has('|', txt, size),
    'has(nil)': has('\bnil\b', txt, size),
    'has(my)': has('\bmy\b', txt, size),
    'has(sub)': has('\bsub\b', txt, size),
    'has(package)': has('\bpackage\b', txt, size),
    'has(,)': has(',', txt, size),
    'has(function()': has('\\bfunction\\(', txt, size),
    'has(const)': has('\\bconst\\b', txt, size),
    'has(namespace)': has('\bnamespace\\b', txt, size),
    'has(using)': has('\\busing\\b', txt, size),
    'has(module)': has('\\bmodule\\b', txt, size),
    'has(this)': has('\\bthis\\b', txt, size),
    'has(#include)': has('#include\\b', txt, size),
    'has(::)': has('::', txt, size),
    'has(->)': has('->', txt, size),
    'has(self)': has('\\bself\\b', txt, size),
    'has(int)': has('\\bint\\b', txt, size),
    'has(#define)': has('#define\\b', txt, size),
    'has(class)': has('\\bclass\\b', txt, size),
    'has(NULL)': has('\\bNULL\\b', txt, size),
    'has(<?)': has('<\\?', txt, size),
    'has(int main)': has('\\bint main\\b', txt, size),
    'has(struct)': has('\\bstruct\\b', txt, size),
    'has(end)': has('\\bend\\b', txt, size),
    'has(def main)': has('\\bdef main\\b', txt, size),
    'has(def)': has('\\bdef\\b', txt, size),
    'has(interface)': has('\\binterface\\b', txt, size),
    'has(Console.Write)': has('\\bConsole\\.Write\\b', txt, size),
    'has(function)': has('\\bfunction\\b', txt, size),
    'has(val)': has('\\bval\\b', txt, size),
    'has(NS*)': has('\\bNS[A-Za-z]\\b', txt, size),
    'has(<<)': has('<<', txt, size),
    'has(echo)': has('\\becho\\b', txt, size),
    'has(use)': has('\\buse [A-Za-z0-9]\\b', txt, size),
    'has(<?php)': has('<?php\\b', txt, size),
    'has(/* or */)': has('(/\\*|\\*/)', txt, size),
  }


  for rel in (r'''-> [<>] \bvar\b \bdef\b \bfunction\b 
    \bconst\b & \( \) ; \$ : \bend\b [{}] [\[\]] \*
    \bclass\b \bself\b \bthis\b , | <- \bpublic\b
    \bprivate\b \bstatic\b \bvoid\b \bfor\b \beach\b
    \byield\b \bjava\b \bscala\b \bSystem\b \bnew\b
    \binterface\b @Override \bnamespace\b \bget\b \bset\b
    \bextends\b \bimplements\b'''.split()):
    features['rel(' + rel + ')'] = count_relative(rel, txt, size)
  
  return features


def get_features(fn):
  f = open(fn, "r")
  txt = f.read()
  f.close()

  return code_features(txt)


def rejig(lang_featuresets):
  feature_names = set()
  for featuresets in lang_featuresets.values():
    for featureset, lang in featuresets:
      for fname in featureset:
        if fname.startswith('rel('):
          feature_names.add(fname)
      break # only need one as they're all the same
  

  
  for fname in feature_names:
    print 'rejigging', fname
    all_values = [featureset[fname] for featureset, lang in featuresets \
                    for featuresets in lang_featuresets.values()]
    all_values.sort()
    n = len(all_values)
    lo = all_values[n/3]
    hi = all_values[2*n/3]
    for featuresets in lang_featuresets.values():
      for featureset, lang in featuresets:
        val = featureset[fname]
        if val < lo:
          val = -1
        elif val > hi:
          val = 0
        else:
          val = 1
        featureset[fname] = val


