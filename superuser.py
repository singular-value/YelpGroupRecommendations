import json, re
import csv, sys
import pickle
import cPickle as pickle
file = open("reviews.txt",'r')

group = []
#command line arguments for members of group
for user in sys.argv[1:]:
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
#populate dict (business, val/uid/bid)
for rating in newUser:
    key = rating['bid'] # key is business id
    if key not in bratings.keys():
        bratings[key] = []
    bratings[key].append(rating)

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
#    print dict

    for key in bratings.keys():
        ratings = bratings[key]
        sum = 0.0
        inc = 0.0
        for rating in ratings:
            sum += dict[rating['uid']]*rating['val']
            inc += dict[rating['uid']]
        avg = sum/inc
        print str(avg) + ' |u SUPERUSER ' + str(key)


#svf_avg(bratings)
#svf_mh(bratings)
svf_expert(bratings, newUser)
