from flask import Flask, request, escape
import nltk
import sys
from features import *
import pickle
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
    probs = classifier.prob_classify(code_features(request.form['code']))
    extra += "<table>"
    for label in probs.samples():
      extra += "<tr><td>" + label + "</td><td>" + '%.10f' % probs.prob(label) + "</td></tr>"
    extra += "</table>"
    


  return "<form method=post><textarea name=code style='width:1000px;height:500px'>"+data+"</textarea><br><input type=submit></form>"+ extra

if __name__ == "__main__":
  app.run(debug=True)
