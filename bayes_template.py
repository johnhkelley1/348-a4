# Name: 
# Date:
# Description:
#
#
# NetIDs:
# jhk192
# dkm840
# nlp412

import math, os, pickle, re, glob, nltk

class Bayes_Classifier:

   def __init__(self):
      os.chdir("movies_reviews")
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      freq_dist = self.getFreqDist(.9)

      self.freq_dist = freq_dist

   def getFreqDist(self,v_start):


      freq_dist = {}
      num_good = 0

      good_reviews = glob.glob("movies-5*.txt")

      good_reviews_full = good_reviews

      good_reviews = good_reviews[:int(len(good_reviews)*v_start)]

      if v_start < .9:
         t2_start = v_start + 0.1
         good_reviews_full = good_reviews_full[int(-t2_start*len(good_reviews_full)):]
         good_reviews = good_reviews + good_reviews_full



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

      bad_reviews_full = bad_reviews

      bad_reviews = bad_reviews[:int(len(bad_reviews)*v_start)]

      if v_start < .9:
         bad_reviews_full = bad_reviews_full[int(-t2_start*len(bad_reviews_full)):]
         bad_reviews = bad_reviews + bad_reviews_full

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

      prob_neg = 0
      prob_pos = 0

      for word in words:
         if word in self.freq_dist['freq_dist']:
            prob_neg += math.log( (self.freq_dist['freq_dist'][word]['bad']+1) / 0.175 )

            prob_pos += math.log( (self.freq_dist['freq_dist'][word]['good']+1) / 0.825 )

      prob_pos = abs(prob_pos)
      prob_neg = abs(prob_neg)
      if prob_pos > prob_neg:
         return 1
      return 0


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

      print "recall good ",float(num_good) / float(tot)

      tot_good = tot


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

      pres_good = float(num_good) / float(num_good +  float(tot - num_bad))

      pres_bad = float(num_bad) / float(num_bad +  float(tot_good - num_good))

      print "recall bad ",float(num_bad) / float(tot)

      print "pres good ",pres_good
      print "pres bad ",pres_bad

      f_good = 2*(pres_good*num_good)/(pres_good+num_good)
      f_bad = 2*(pres_bad*num_bad)/(pres_bad+num_bad)

      print "f good ",f_good
      print "f bad ",f_bad

      ret = {"rec_good":float(num_good),"rec_bad":float(num_bad),"pres_good":pres_good,"pres_bad":pres_bad,"f_good":f_good,"f_bad":f_bad}

      return ret


   def crossValidation(self):
      aves = []
      for i in range(10):
         print "ITERATION ",i
         freq_dist = self.getFreqDist(float(i)/10.0)
         self.freq_dist = freq_dist
         aves.append(abayes.test())

      rec_good_ave = 0
      rec_bad_ave = 0
      pres_good_ave = 0
      pres_bad_ave = 0
      f_good_ave = 0
      f_bad_ave = 0

      for item in aves:
         rec_good_ave += item['rec_good']
         rec_bad_ave += item['rec_bad']
         pres_good_ave += item['pres_good']
         pres_bad_ave += item['pres_bad']
         f_good_ave += item['f_good']
         f_bad_ave += item['f_bad']

      rec_good_ave /= 10
      rec_bad_ave /= 10
      pres_good_ave /= 10
      pres_bad_ave /= 10
      f_good_ave /= 10
      f_bad_ave /= 10

      print rec_good_ave
      print rec_bad_ave
      print pres_good_ave
      print pres_bad_ave
      print f_good_ave
      print f_bad_ave



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
# abayes.train()
# abayes.test()
# abayes.classify("this is a fantastic review")
abayes.crossValidation()

