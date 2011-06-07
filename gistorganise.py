import os

dirs = {
  ".rb": "ruby", 
  ".py": "python", 
  ".cc": "cpp", 
  ".rbx": "ruby", 
  ".cpp": "cpp",
  ".pl": "perl",
  ".js": "javascript", 
  ".coffee":"coffeescript",
  ".scala": "scala", 
  ".sh": "shell",
  ".java": "java",
  ".m": "objc",
  ".cs": "csharp",
  ".php": "php",
  ".c": "c",
  ".hs": "haskell",
  ".go": "go"
}

for dir in os.listdir("gists"):
  dir_f = os.path.join("gists", dir)
  if os.path.isdir(dir_f):
    fc = 0
    for gist in os.listdir(dir_f):
      fc += 1
      gist_f = os.path.join(dir_f, gist)
      if os.path.isfile(gist_f):
        base, ext = os.path.splitext(gist)
        if ext in dirs:
          newfn = dir + "-" + str(fc) + "-" + gist
          newpath = os.path.join(dirs[ext], newfn)
          
          print gist_f, " -> ", newpath
          os.rename(gist_f, newpath)
