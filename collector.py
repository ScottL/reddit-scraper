import praw
from collections import deque
from time import sleep
from operator import itemgetter
import json
import os

FILENAME_R = "raw.txt"
FILENAME_C = "clean.txt"


def extract():
   useragent = "corpusbuilder/1.0 by scott"
   cache = deque(maxlen = 1000)
   r = praw.Reddit(user_agent=useragent)
   running = True

   dict = {}
   dict = initialDictionary(FILENAME_R)
   cleanDict = {}
   cleanDict = initialDictionary(FILENAME_C)

   punctuation = ['.',',','?','!','/',':','-','[',']','{','}','(',')',';']
  
   while running:
      allcomments = r.get_comments('all', limit = 800)
      print "retrieved comments"
      wordCount = 0
      commentCount = 0
      for content in allcomments:
         if content.id in cache:
            print "IN CACHE"
            break
         cache.append(content.id)
         commentCount += 1

         try:
            for i in content.body.split():
               rawWord = i.encode('utf-8').strip()
               clean = rawWord

               for sym in punctuation:
                  if sym in rawWord:
                     clean  = rawWord.replace(sym, "")
                                   
               if clean in cleanDict:
                  cleanDict[clean] += 1
               else:
                  cleanDict[clean] = 1

               if rawWord in dict:
                  dict[rawWord] += 1
               else:
                  dict[rawWord] = 1
               wordCount += 1
         except Exception, e:
            print "ERROR: ", e
            print "Sleeping"
            sleep(30)

      print "Parsed ", commentCount, " new comments"
      print "Added ", wordCount, " new word counts"      
      sortDict = sorted(dict.iteritems(), key=itemgetter(1), reverse=True)
      sortcleanDict = sorted(cleanDict.iteritems(), key=itemgetter(1), reverse=True)
      writeDictionary(sortDict, FILENAME_R)
      writeDictionary(sortcleanDict, FILENAME_C)
      
      print "Wrote to file"
      print "Sleeping\n\n"
      sleep(50)


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
