import praw
from collections import deque
from time import sleep
from operator import itemgetter
import json
import os


def extract():
   b = os.path.getsize("out.txt")
   useragent = "corpusbuilder/1.0 by scott"
   cache = deque(maxlen = 500)

   r = praw.Reddit(user_agent=useragent)
   running = True

   dict = {}
   if b == 0:
      #dict = {}
      print "t"
   else:
      #dict= json.load(open("out.txt"))
      #dict = [s.encode('utf-8') for s,t in dict]
      print "t"
   punc = ['?','!',',','.',':','"',';','(',')','[',']']

   while running:
      allcomments = r.get_comments('all', limit = 400)
      print "retrieved comments"
      for x in allcomments:
         if x.id in cache:
            print "IN CACHE"
            break
         cache.append(x.id)

         try:
            for i in x.body.split():
               j = i.encode('utf-8').strip()
               #print j
               if j in dict:
                  #print "already in"
                  dict[j] += 1
               else:
                  #print "adding"
                  dict[j] = 1
         except Exception, e:
            print "ERROR: ", e
            print "Sleeping"
            sleep(30)

      
      sortD = sorted(dict.iteritems(), key=itemgetter(1), reverse=True)
      #print sortD
      formatPrint(sortD)
      #open('out.txt','w').close()
      #json.dump(sortD, open("out.txt",'w'))
      formatOutput(sortD)
      print "Sleeping"
      sleep(30)

def formatPrint(dictionary):
   print "temp"
   for key,value in dictionary:
      print key, value


def formatOutput(dictionary):
   f =open('out.txt', 'w')
   for key,value in dictionary:
      f.write(str(key) + '\t' + str(value) + '\n')




extract()
