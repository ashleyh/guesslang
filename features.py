import re
import math

def count_relative(search, txt, size):
#  return int(float(len(re.findall(search, txt)))*10000000/float(size)) > 0
#  return float(len(re.findall(search,txt)))/float(size)
  if size == 0:
    return 0
  return math.ceil(math.log10(((len(re.findall(search,txt))*1000)/size)+1))
#  return len(re.findall(search,txt)) > 0

def has(search, txt, size):
  if txt == 0:
    return False

  if re.search(search, txt):
    return True
  else:
    return False

def code_features(txt):
  size = len(txt)
  return {
    'rel(->)': count_relative('->', txt, size),
    'rel(< or >)': count_relative('[<>]', txt, size),
    'rel(var)': count_relative('\bvar\b', txt, size),
    'rel(def)': count_relative('\bdef\b', txt, size),
    'rel(function)': count_relative('\bfunction\b', txt, size),
    'rel(const)': count_relative('\bconst\b', txt, size),
    'rel(&)': count_relative('&', txt, size),
    'rel(())': count_relative('\\(\\)', txt, size),
    'rel(;)': count_relative(';', txt, size),
    'rel($)': count_relative('\\$', txt, size),
    'rel(:)': count_relative(':', txt, size),
    'rel(end)': count_relative('\bend\b', txt, size),
    'rel({ or })': count_relative('[{}]', txt, size),
    'rel([ or ])': count_relative('[\\[\\]]', txt, size),
    'rel(*)': count_relative('\\*', txt, size),
    'rel(class)': count_relative('\bclass\b', txt, size),
    'rel(self)': count_relative('\bself\b', txt, size),
    'rel(this)': count_relative('\bthis\b', txt, size),
    'rel(,)': count_relative(',', txt, size),
    'rel(|)': count_relative('|', txt, size),
    'rel(<-)': count_relative('<-', txt, size),

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


def get_features(fn):
  f = open(fn, "r")
  txt = f.read()
  f.close()

  return code_features(txt)

