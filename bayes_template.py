# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re, glob

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      freq_dist = self.getFreqDist()

      print freq_dist

   def getFreqDist(self):
      os.chdir("movies_reviews")
      freq_dist = {}
      for review in glob.glob("movies-5*.txt"):

         review = self.loadFile(review)
         review = self.tokenize(review)
         review = [s.lower() for s in review]
         review = set(review)
         for token in review:
            if token in freq_dist:
               freq_dist[token]['good'] += 1
            else:
               freq_dist[token] = {'good':1,'bad':0}

      for review in glob.glob("movies-1*.txt"):

         review = self.loadFile(review)
         review = self.tokenize(review)
         review = [s.lower() for s in review]
         review = set(review)
         for token in review:
            if token in freq_dist:
               freq_dist[token]['bad'] += 1
            else:
               freq_dist[token] = {'good':0,'bad':1}
      return freq_dist

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """

   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

abayes = Bayes_Classifier()
abayes.train()

