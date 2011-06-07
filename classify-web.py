from flask import Flask, request, escape
import nltk
import sys
from features import *
import pickle
import operator

app = Flask(__name__)

f = open("classifier.pickle", "r")
classifier = pickle.load(f)
f.close()



@app.route("/", methods=['GET','POST'])
def hello():
  data = ""
  extra = ""
  if(request.form.has_key("code")):
    data = str(escape(request.form['code']))
    features = code_features(request.form['code'])
    probs = classifier.prob_classify(features)


    probsd = dict()
    for label in probs.samples():
      probsd[label] = probs.prob(label)

    probsd = sorted(probsd.iteritems(), key=operator.itemgetter(1))
    probsd.reverse()

    extra += "<h2>*Cameron peers into his crystal ball(s)*: I think this is... " + probsd[0][0] + "</h2>"

    extra += "<table>"
    for (k,v) in probsd:
      extra += "<tr><td>" + k + "</td><td>" + '%.10f' % v + "</td></tr>"
    extra += "</table>"
    
    extra += "<table>"
    for (k,v) in features.items():
      extra += "<tr><td>" + str(escape(k)) + "</td><td>" + str(v) + "</td></tr>"

    extra += "</table>"


  return "<form method=post><textarea name=code style='width:1000px;height:500px'>"+data+"</textarea><br><input type=submit></form>"+ extra

if __name__ == "__main__":
  app.run(debug=True)
