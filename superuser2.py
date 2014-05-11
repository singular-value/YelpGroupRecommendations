import json, re
import csv, sys
import pickle
import cPickle as pickle
#file = open("reviewstest.txt",'r')

group = []
###read in command line arguments
file = open(str(sys.argv[1]), 'r')
svf = sys.argv[2]
nrm = sys.argv[3]
###keep track of number of group members for normalization
nUsers = len(sys.argv[4:])
for user in sys.argv[4:]:
    group.append(str(user))
#outFile1 = open("pseudoAvg.txt", 'w')
#print 'Your Group is ' + str(group)

newUser = []

# remove all group members from group, print the rest of the lines
for review in file:
    review_chars = review.split()
    if review_chars[2] in group:
        newUser.append({
                        "val": float(review_chars[0]),
                        "uid": str(review_chars[2]),
                        "bid": str(review_chars[4])})
    else:
        #i = 1
        print review[:-1]

bratings = {}
userAverages = {}
###populate dict (business, val/uid/bid) and calculate averages
for rating in newUser:
    keyB = rating['bid'] # keyB is business id
    keyU = rating['uid'] # keyU is user id
    if keyB not in bratings.keys():
        bratings[keyB] = []
    bratings[keyB].append(rating)
    if keyU not in userAverages.keys():
        userAverages[keyU]=[]
        userAverages[keyU].append({'count': int(0), 'average': float(0)})
    count = userAverages[keyU][0]['count']
    averg = userAverages[keyU][0]['average']
    userAverages[keyU][0]['count'] += 1
    userAverages[keyU][0]['average'] = (count * averg + rating['val'])/(count + 1)

###if normalized option selected, scale the ratings
if nrm=='norm':
    groupAverage = 0.0
    for key in userAverages.keys():
        groupAverage += userAverages[key][0]['average']
    groupAverage /= len(userAverages.keys())

    for key in bratings.keys():
        for i in range(0, len(bratings[key]) ):
            bratings[key][i]['val'] *= groupAverage / userAverages[bratings[key][i]['uid']][0]['average']

#average the ratings for each business and print
def svf_avg(bratings):
    for key in bratings.keys():
        ratings = bratings[key]
        sum = 0.0
        count = 0.0
        for rating in ratings:
            sum += rating['val']
            count += 1
        avg = str(sum/count)
        print str(avg) + ' |u SUPERUSER |i ' + str(key)

#least misery
def svf_lm(bratings):
    for key in bratings.keys():
        ratings = bratings[key]
        min = ratings[0]['val']
        for rating in ratings:
            if (rating['val'] < min):
                min = rating['val']
        print str(min) + ' |u SUPERUSER |i ' + str(key)

#most happiness
def svf_mh(bratings):
    for key in bratings.keys():
        ratings = bratings[key]
        max = ratings[0]['val']
        for rating in ratings:
            if (rating['val'] > max):
                max = rating['val']
        print str(max) + ' |u SUPERUSER |i ' + str(key)

def svf_expert(bratings,newUser):
    dict = {}
    count = 0.0
    for review in newUser:
        if review['uid'] not in dict:
            dict[review['uid']] = 1
        else:
            dict[review['uid']] += 1
        count += 1

    for user in dict.keys():
        dict[user] /= count
    print dict

    for key in bratings.keys():
        ratings = bratings[key]
        sum = 0.0
        inc = 0.0
        for rating in ratings:
            sum += dict[rating['uid']]*rating['val']
            inc += dict[rating['uid']]
        avg = sum/inc
        #print str(avg) + ' |u SUPERUSER ' + str(key)

#choose specified social value function to apply
if svf=='avg':
    svf_avg(bratings)
elif svf=='lm':
    svf_lm(bratings)
elif svf=='mh':
    svf_mh(bratings)
elif svf=='expert':
    svf_expert(bratings, newUser)

