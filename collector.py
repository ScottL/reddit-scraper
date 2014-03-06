import praw
from collections import deque
from time import sleep
from operator import itemgetter
import json
import os

FILENAME = "out.txt"

def extract():
   useragent = "corpusbuilder/1.0 by scott"
   cache = deque(maxlen = 1000)
   r = praw.Reddit(user_agent=useragent)
   running = True
   dict = {}
   dict = initialDictionary(FILENAME)

   punc = ['?','!',',','.',':','"',';','(',')','[',']']

   while running:
      allcomments = r.get_comments('all', limit = 600)
      print "retrieved comments"
      wordCount = 0
      commentCount = 0
      for x in allcomments:
         if x.id in cache:
            print "IN CACHE"
            break
         cache.append(x.id)
         commentCount += 1

         try:
            for i in x.body.split():
               j = i.encode('utf-8').strip()
               if j in dict:
                  dict[j] += 1
               else:
                  dict[j] = 1
               wordCount += 1
         except Exception, e:
            print "ERROR: ", e
            print "Sleeping"
            sleep(30)

      print "Parsed ", commentCount, " new comments"
      print "Added ", wordCount, " new word counts"      
      print "Wrote to file"
      sortDict = sorted(dict.iteritems(), key=itemgetter(1), reverse=True)
      #formatPrint(sortD)
      writeDictionary(sortDict, FILENAME)
      #open('out.txt','w').close()
      #json.dump(sortD, open("out.txt",'w'))
      print "Sleeping\n\n"
      sleep(45)


# Testing purposes. pretty print dictionary
def formatPrint(dictionary):
   print "temp"
   for key,value in dictionary:
      print key, value


# Write dictionary to file
def writeDictionary(dictionary, filename):
   f =open(filename, 'w')
   for key,value in dictionary:
      f.write(str(key) + '\t' + str(value) + '\n')
   f.close()

# Read dictionary from file
def readDictionary(filename):
   read =open(filename, 'r')
   dict = {}
   for line in read:
      pair = line.split()
      dict[pair[0]] = int(pair[1])
   read.close()
   return dict


# Initilize dictionary
def initialDictionary(filename):
   b = os.path.getsize(filename)
   dict = {}
   if b == 0:
      print "Empty file"
   else:
      #dict= json.load(open("out.txt"))
      #dict = [s.encode('utf-8') for s,t in dict]
      dict = readDictionary(filename)
      print "Populated file"
   return dict

extract()
