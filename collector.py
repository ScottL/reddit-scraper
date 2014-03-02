import praw
from collections import deque
from time import sleep
from operator import itemgetter
import json
import os

b = os.path.getsize("out.txt")
useragent = "corpusbuilder/1.0 by scott"
cache = deque(maxlen = 350)

r = praw.Reddit(user_agent=useragent)
running = True

s = set([])
if b == 0:
   dict = {}
else:
   dict= json.load(open("out.txt"))
   dict = [s.encode('utf-8') for s,t in dict]
   print dict
punc = ['?','!',',','.',':','"',';','(',')','[',']']

while running:
   allcomments = r.get_comments('all', limit = 340)
   print "retrieved comments"
   for x in allcomments:
      if x.id in cache:
         print "IN CACHE"
         print "Sleeping"
         sleep(30)
         break
      cache.append(x.id)

      try:
         for i in x.body.split():
            j = i.encode('utf-8').strip()
            #print j
            if j in dict:
               print "already in"
               dict[j] += 1
            else:
               print "adding"
               dict[j] = 1
      except Exception, e:
         print "ERROR: ", e
         print "Sleeping"
         sleep(30)

   
   sortD = sorted(dict.iteritems(), key=itemgetter(1), reverse=True)
   print sortD
   open('out.txt','w').close()
   json.dump(sortD, open("out.txt",'w'))
