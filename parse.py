import json, re
import csv

file = open("yelp_phoenix_academic_dataset",'r')
#w = open('blah', 'r+')
lines = file.readlines()
#lines = lines[1:]
#lines = lines[:-2]

locations = []

test = open(r'C:\Users\Stephen\Documents\13-14 Junior\COS 424\yelp_phoenix_academic_dataset\test.csv', 'w+')
users = []
businesses = []
list = []
for line in lines[1:]:
    # ignore these lines
    if line[0] != '{':
        continue 
    o = json.loads(str(line))
    


    if o['type'] == "review":
        # if o['user_id'] not in users:
        #     users.append(o['user_id'])
        #     print o['user_id']
        # if o['business_id'] not in businesses:
        #     businesses.append(o['business_id'])
        #print str(o['stars']) + ' |u ' + str(users.index(o['user_id'])) + ' |i ' + str(businesses.index(o['business_id']))
    
for i in businesses:
    print i
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