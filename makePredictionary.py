import sys
import pickle

predictions = open('predictions.txt','r')

hugeDict = {}

for i in xrange(len(sys.argv)-1):
    businesses = open('businessIDs.txt','r')
    userDict = {}

    for restaurantHash in businesses:
        userDict[restaurantHash[:-1]] = float(predictions.readline()[:-1])
    
    hugeDict[sys.argv[i+1]] = userDict

pickle.dump(predicionary,open("predictionary.p","wb"))
