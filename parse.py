import json, re
import pickle
import csv

file = open("yelp_academic_dataset_review.json",'r')
#file = open("test.txt",'r')

lines = file.readlines()

locations = []

users = []
businesses = []
list = []
review_data = [{}]

for line in lines:
    # ignore these lines
    if line[0] != '{':
        continue 
    o = json.loads(str(line))

    if o['type'] == "review":
         # data without long ids
         '''if o['user_id'] not in users:
             users.append(o['user_id'])
         if o['business_id'] not in businesses:
             businesses.append(o['business_id'])

         #if o['user_id'] in users and o['business_id'] in businesses:

         print str(o['stars']) + ' |u ' + str(users.index(o['user_id'])) + ' |i ' + str(businesses.index(o['business_id']))'''

        #data with long ids
         print str(o['stars']) + ' |u ' + str(o['user_id']) + ' |i ' + str(o['business_id'])

pickle.dump(users, open('saveUsers.p','wb'))
pickle.dump(businesses, open('saveBiz.p','wb'))

# for i in businesses:
#     print i
    #if o['type'] == "review":
    #    print str(o['stars']) + ' |u ' + str(o['user_id']) + ' |i ' + str(o['business_id'])
    
    #
    # '''if 'Price Range' in o['attributes']:
    #     if o['type'] == "business" and o['attributes']['Price Range'] == 4: #('Automotive' in o['categories']):# and o['city'] == 'Phoenix':
    #         loc = []
    #         #loc.append(o['categories'])
    #         loc.append(o['longitude'])
    #         loc.append(o['latitude'])
    #         #locations.append(o['latitude']) + "," + str(o['longitude']) + ")"
    #         locations.append(loc)'''

# test = open(r'C:\Users\Stephen\Documents\13-14 Junior\COS 424\yelp_phoenix_academic_dataset\test.csv', 'w+')
#
# for i in locations:
#     for j in i:
#         test.write(str(j)+',')
#     test.write('\n')