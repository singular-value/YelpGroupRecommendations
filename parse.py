import json, re
import pickle
import csv
import time

file = open("yelp_academic_dataset_review.json",'r')
#file = open("testReview.txt",'r')

lines = file.readlines()

locations = []

users = []
businesses = []
list = []

review_dict = {}
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
         review = {}
         review['user_id'] = str(o['user_id'])
         review['stars'] = str(o['stars'])
         review['business_id'] = str(o['business_id'])
         review['date'] = time.strptime(str(o['date']),'%Y-%m-%d')

         #Is the user's id already in the dictionary?
         if review['user_id'] in review_dict.keys():
             # iterate through each review by that user
             updated = False
             for i,rev in enumerate(review_dict[review['user_id']]):
                 # if the business is the same, but the new review's date is more recent, update
                 if rev['business_id'] == review['business_id']:
                    updated = True
                    if review['date'] > rev['date']:
                        review_dict[review['user_id']][i] = review
                        break
             if not updated:
                review_dict[review['user_id']].append(review)
         else:
             # if the user id was never there, just create a new list and add it to the dict entry
             review_list = []
             review_list.append(review)
             review_dict[review['user_id']] = review_list

         #print str(o['stars']) + ' |u ' + str(o['user_id']) + ' |i ' + str(o['business_id'])

#pickle.dump(users, open('saveUsers.p','wb'))
#pickle.dump(businesses, open('saveBiz.p','wb'))
f = open('saveReviewDict.p','wb')

pickle.dump(review_dict, f)
f.close()

#for entry in review_dict.keys():
#    for rating in review_dict[entry]:
#        print rating['stars'] + ' |u ' + rating['user_id'] + ' |i ' + rating['business_id']

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