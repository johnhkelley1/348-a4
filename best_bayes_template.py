# Name: Dylan McCann, Niall Pereira, John Kelley
# Date: Monday, May 23, 2016
# Description: Assignment 4: using naive bayes to classify good/bad movie reviews
# something about all being here
# yep yep

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

         for token in review:
            if token in freq_dist:
               freq_dist[token]['bad'] += 1
            else:
               freq_dist[token] = {'good':0,'bad':1}


      freq_dist = {"num_good":num_good,"num_bad":num_bad,"freq_dist":freq_dist}

      # need to iterate through freq_dist['freq_dist'][x]['good'] and sum those 
      totalWordCountPositive = 0
      totalWordCount = 0


      for key in freq_dist['freq_dist']:
         totalWordCountPositive += freq_dist['freq_dist'][key]['good']
         totalWordCount += (freq_dist['freq_dist'][key]['good'] + freq_dist['freq_dist'][key]['bad'])



      
      for key in freq_dist['freq_dist']:
         freq_dist['freq_dist'][key]['pwgg'] = float(freq_dist['freq_dist'][key]['good']) / float(totalWordCountPositive)
         freq_dist['freq_dist'][key]['pw'] = (float(freq_dist['freq_dist'][key]['good']) + float(freq_dist['freq_dist'][key]['bad'])) / float(totalWordCount)


      return freq_dist
         

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      words = self.tokenize(sText)
      #print "words here, ", words
      words = [s.lower() for s in words]
      words = set(words)
      #words = set(words) potentially bring this back in here again.

      num_docs = self.freq_dist['num_good'] + self.freq_dist['num_bad']
      prob_neg = 0
      prob_pos = 0

      for word in words:
        if word in self.freq_dist['freq_dist']:
            prob_neg += math.log((self.freq_dist['freq_dist'][word]['bad']+1) / 0.175)
            prob_pos += math.log((self.freq_dist['freq_dist'][word]['good']+1) / 0.825)

      prob_pos = abs(prob_pos)
      prob_neg = abs(prob_neg)
      if prob_pos > prob_neg:
        return 1
      return 0

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


   def test(self):

      good_reviews = glob.glob("movies-5*.txt")

      good_reviews = good_reviews[-int(len(good_reviews)*.9):]

      tot = 0
      num_good = 0
      for review in good_reviews:
         tot += 1
         review = self.loadFile(review)
         res = self.classify(review)
         num_good += res

      print "good ",float(num_good) / float(tot)


      bad_reviews = glob.glob("movies-1*.txt")

      bad_reviews = bad_reviews[-int(len(bad_reviews)*.9):]

      tot = 0
      num_bad = 0
      for review in bad_reviews:
         tot += 1
         review = self.loadFile(review)
         res = self.classify(review)
         if res == 0:
            num_bad += 1

      print "bad ",float(num_bad) / float(tot)



abayes = Bayes_Classifier()
abayes.train()
abayes.test()
abayes.classify("this is a fantastic review")







