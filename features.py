import re
import math

def count_relative(search, txt, size):
#  return int(float(len(re.findall(search, txt)))*10000000/float(size)) > 0
#  return float(len(re.findall(search,txt)))/float(size)
  if size == 0:
    return 0
  return math.ceil(math.log10(((len(re.findall(search,txt))*10000000)/size)+1))
#  return len(re.findall(search,txt)) > 0

def code_features(txt):
  size = len(txt)
  return {
    'struct_access': count_relative('->', txt, size),
    'angle_bracket': count_relative('[<>]', txt, size),
    'var': count_relative('var', txt, size),
    'def': count_relative('def', txt, size),
    'function': count_relative('function', txt, size),
    'js_closure_function': count_relative('function\\(', txt, size),
    'const': count_relative('const', txt, size),
    'ampersand': count_relative('&', txt, size),
    'double_paren': count_relative('\\(\\)', txt, size),
    'semicolon': count_relative(';', txt, size),
    'dollar': count_relative('\\$', txt, size),
    'module': count_relative('module', txt, size),
    'require': count_relative('require', txt, size),
    'nil': count_relative('nil', txt, size),
    'NULL': count_relative('NULL', txt, size),
    'class': count_relative('class', txt, size),
    'namespace': count_relative('namespace', txt, size),
    'self': count_relative('self', txt, size),
    'this': count_relative('this', txt, size),
    '#include': count_relative('#include', txt, size),
    'colon': count_relative(':', txt, size),
    'end': count_relative('end', txt, size),
    'curly_bracket': count_relative('[{}]', txt, size),
    'square_bracket': count_relative('[\\[\\]]', txt, size),
    'asterisk': count_relative('\\*', txt, size),
    'slash_asterisk_comment': count_relative('(/\\*|\\*/)', txt, size)
  }


def get_features(fn):
  f = open(fn, "r")
  txt = f.read()
  f.close()

  return code_features(txt)

