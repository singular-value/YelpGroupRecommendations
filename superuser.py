import json, re
import csv

file = open("reviews.txt",'r')
group = ['6','3']

outFile1 = open("pseudoAvg.txt", 'w')

newUser = []
# remove all group members from group, print the rest of the lines
for review in file:
    review_chars = review.split()
    if review_chars[2] in group:
        newUser.append({
                        "val": float(review_chars[0]),
                        "uid": int(review_chars[2]),
                        "bid": int(review_chars[4])})
    else:
        outFile1.write(review)

bratings = {}
#populate dict (business, entire string)
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
        outFile1.write( str(avg) + ' |u SUPERUSER |i ' + str(key) + '\n')

#least misery
def svf_lm(bratings):
    for key in bratings.keys():
        ratings = bratings[key]
        min = ratings[0]['val']
        for rating in ratings:
            if (rating['val'] < min):
                min = rating['val']
        outFile1.write(str(min) + ' |u SUPERUSER |i ' + str(key) + '\n')

svf_avg(bratings)
#svf_lm(bratings)
