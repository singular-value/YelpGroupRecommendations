import sys
import pickle

predictions = open('predictions.txt','r')

hugeDict = {}

businesses = open('businessIDs.txt','r')
userDict = {}

for restaurantHash in businesses:
    userDict[restaurantHash[:-1]] = float(predictions.readline()[:-1])
    

pickle.dump(userDict,open("predictionary.p","wb"))
