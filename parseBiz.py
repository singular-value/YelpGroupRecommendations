import json, re
import pickle
import csv
import time

file = open("yelp_academic_dataset_business.json",'r')
#file = open("testBiz.txt",'r')

lines = file.readlines()

locations = []

users = []
businesses = []
list = []

biz_dict = {}
count = 0
for line in lines:
    # ignore these lines
    if line[0] != '{':
         continue
    o = json.loads(str(line))

    if o['type'] == "business":
        #data with long ids
         biz = {}
         biz['business_id'] = str(o['business_id'])
         biz['stars'] = str(o['stars'])
         biz['latitude'] = str(o['latitude'])
         biz['longitude'] = str(o['longitude'])
         biz['review_count'] = str(o['review_count'])
         biz['categories'] = str(o['categories'])
         biz_dict[biz['business_id']] = biz

#pickle.dump(users, open('saveUsers.p','wb'))
f = open('saveBizDict.p', 'wb')
pickle.dump(biz_dict, f)

f.close()
#for entry in biz_dict.keys():
#    print biz_dict[entry]['business_id'] + ' ' + biz_dict[entry]['stars']
#first: O_X3PGhk3Y5JWVi866qlJg, 4.0
#last: qW-jqCAqFF-GdbjV-jh4Hw, 3.5