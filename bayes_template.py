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

      self.freq_dist = freq_dist

   def getFreqDist(self):
      os.chdir("movies_reviews")
      freq_dist = {}
      num_good = 0

      good_reviews = glob.glob("movies-5*.txt")

      good_reviews = good_reviews[:int(len(good_reviews)*.9)]

      for review in good_reviews:
         num_good += 1
         review = self.loadFile(review)
         review = self.tokenize(review)
         review = [s.lower() for s in review]
         review = set(review)
         for token in review:
            if token in freq_dist:
               freq_dist[token]['good'] += 1
            else:
               freq_dist[token] = {'good':1,'bad':0}

      num_bad = 0

      bad_reviews = glob.glob("movies-1*.txt")

      bad_reviews = bad_reviews[:int(len(bad_reviews)*.9)]

      for review in bad_reviews:
         num_bad +=1

         review = self.loadFile(review)
         review = self.tokenize(review)
         review = [s.lower() for s in review]
         review = set(review)
         for token in review:
            if token in freq_dist:
               freq_dist[token]['bad'] += 1
            else:
               freq_dist[token] = {'good':0,'bad':1}
      freq_dist = {"num_good":num_good,"num_bad":num_bad,"freq_dist":freq_dist}

      prob_dist = {}
      for key in freq_dist['freq_dist']:
         freq_dist['freq_dist'][key]['pwgg'] = float(freq_dist['freq_dist'][key]['good']) / float(freq_dist['num_good'])

      return freq_dist
         

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      words = self.tokenize(sText)
      words = [s.lower() for s in words]
      words = set(words)

      num_docs = self.freq_dist['num_good'] + self.freq_dist['num_bad']
      num = 0
      den = 0
      for word in words:
         if word in self.freq_dist['freq_dist']:
            pwgg = self.freq_dist['freq_dist'][word]['pwgg']
            if pwgg != 0:
               pwgg = math.log(pwgg)
            pw = float(self.freq_dist['freq_dist'][word]['good'] + self.freq_dist['freq_dist'][word]['bad']) / float(num_docs)
            if pw != 0:
               pw = math.log(pw)

            num += pwgg
            den += pw

      if num == 0 or den == 0:
         return -1

      print "num" + str(num)
      print "den" + str(den)

      tot = num*float(self.freq_dist['num_good'])/num_docs

      tot = tot / den

      print tot



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
abayes.classify("this is a fantastic review")

