import json, re
import csv, sys
import pickle
import cPickle as pickle
file = open("saveReviewDict.p",'rb')

#outFile1 = open("pseudoAvg.txt", 'w')
#print 'Your Group is ' + str(group)
reviewDict = pickle.load(file)



uratings = {}
#populate dict (user, val/uid/bid)
for user in reviewDict.keys():
    for entry in reviewDict[user]:
        key = entry['business_id'] # key is biz id
        if key not in uratings.keys():
            uratings[key] = []
        if entry['user_id'] not in uratings[key]:
            uratings[key].append(entry['user_id'])

f = open('saveBizToUsersDict.p','wb')

pickle.dump(uratings, f)
f.close()