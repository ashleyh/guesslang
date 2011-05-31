import re

def count_relative(search, txt, size):
#  return int(float(len(re.findall(search, txt)))*10000000/float(size)) > 0
#  return float(len(re.findall(search,txt)))/float(size)
  return len(re.findall(search,txt)) > 0

def code_features(txt):
  size = len(txt)
  return {
    'struct_access': count_relative('->', txt, size),
    'angle_bracket': count_relative('[<>]', txt, size),
    'var': count_relative('var', txt, size),
    'def': count_relative('def', txt, size),
    'function': count_relative('function', txt, size),
    'module': count_relative('module', txt, size),
    'require': count_relative('require', txt, size),
    'nil': count_relative('nil', txt, size),
    'class': count_relative('class', txt, size),
    'colon': count_relative(':', txt, size),
    'end': count_relative('end', txt, size),
    'curly_bracket': count_relative('[{}]', txt, size),
    'square_bracket': count_relative('[\\[\\]]', txt, size),
    'asterisk': count_relative('\\*', txt, size)
  }


def get_features(fn):
  f = open(fn, "r")
  txt = f.read()
  f.close()

  return code_features(txt)

