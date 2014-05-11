import sys, math
import cPickle as pickle

user = sys.argv[1]

file = open('saveReviewDict.p','rb')
filebiz = open('saveBizDict.p', 'rb')
reviewDict = pickle.load(file)
bizDict = pickle.load(filebiz)

userReviews = reviewDict[user]

#run this as :
#python group_formation.py xAVu2pZ6nIvkdHh8vGs84Q

print 'YOUR REVIEWS'
for review in userReviews:
    print 'name: ' + str(bizDict[review['business_id']]['name']) + ' review: ' + str(review['stars'])

if len(userReviews) < 5:
    print 'Sorry, your user doesn\'t have enough ratings'
else:
    dotProducts = {}
    for user_id in reviewDict.keys():
        reviewList = reviewDict[user_id]
        count = 0.0
        sum = 0.0
        norm_indiv = 0.0
        norm_user = 0.0
        for review in reviewList:
            for user_review in userReviews:
                #print 'review' + str(review)
                #print user_review
                if review['business_id'] == user_review['business_id']:
                    count += 1
                    sum += int(review['stars']) * int(user_review['stars'])
                    norm_indiv += int(user_review['stars']) ** 2
                    norm_user += int(review['stars']) ** 2
        if count > 5:
            #print 'A match with : ' + str(user_id)
            dotProducts[user_id] = sum/(math.sqrt(norm_indiv)*math.sqrt(norm_user))

    if len(dotProducts.keys()) < 10:
        print 'Sorry, your user doesn\'t have enough ratings'
    else:
        list = sorted(dotProducts.iteritems(), key=lambda x: x[1], reverse=True)

        i = 0
        for entry in list:
            if i != 0:
                print 'MATCH ' + str(i) + ': ' + str(entry[0])
                review_list = reviewDict[entry[0]]
                j = 0
                for review in review_list:
                    j += 1
                    print 'name: ' + bizDict[review['business_id']]['name'].encode('utf-8') + ' review: ' + str(review['stars'])
                    if j > 10:
                        break
            i += 1
            if i > 10:
                break

