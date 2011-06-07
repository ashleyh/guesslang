import json
import urllib2
import time
import os

for i in range (76262, 894190):
  try:
    metadata = json.loads(urllib2.urlopen("http://gist.github.com/api/v1/json/"+str(i)).read());
#    time.sleep(0.1)
    for gist in metadata['gists']:
      for file in gist['files']:
        data = urllib2.urlopen("http://gist.github.com/raw/"+str(i)+"/"+file).read()
#        time.sleep(0.1)
        try:
          os.makedirs(os.path.join("gists", str(i)))
        except:
          pass

        f = open(os.path.join("gists", str(i), file), "w")
        f.write(data)
        f.close()

  except Exception as e:
    print "Error", i, e
