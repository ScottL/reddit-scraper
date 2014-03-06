import praw
from collections import deque
from time import sleep
from operator import itemgetter
import json
import os


def extract():
   b = os.path.getsize("out.txt")
   useragent = "corpusbuilder/1.0 by scott"
   cache = deque(maxlen = 1000)

   r = praw.Reddit(user_agent=useragent)
   running = True

   dict = {}
   if b == 0:
      dict = {}
      print "Empty file"
   else:
      #dict= json.load(open("out.txt"))
      #dict = [s.encode('utf-8') for s,t in dict]
      dict = formatInput()
      print "Populated file"

   punc = ['?','!',',','.',':','"',';','(',')','[',']']

   while running:
      allcomments = r.get_comments('all', limit = 950)
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
      sortD = sorted(dict.iteritems(), key=itemgetter(1), reverse=True)
      #formatPrint(sortD)
      formatOutput(sortD)
      #open('out.txt','w').close()
      #json.dump(sortD, open("out.txt",'w'))
      print "Sleeping\n\n"
      sleep(45)


def formatPrint(dictionary):
   print "temp"
   for key,value in dictionary:
      print key, value


def formatOutput(dictionary):
   f =open('out.txt', 'w')
   for key,value in dictionary:
      f.write(str(key) + '\t' + str(value) + '\n')
 

def formatInput():
   read =open('out.txt', 'r')
   dict = {}
   for line in read:
      pair = line.split()
      dict[pair[0]] = int(pair[1])

   return dict
   
extract()
