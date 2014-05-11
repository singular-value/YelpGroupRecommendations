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
# validation: P1qwZrslRv9KS9vPJNXe4g

print 'YOUR REVIEWS'
for review in userReviews:
    print 'name: ' + str(bizDict[review['business_id']]['name']) + ' review: ' + str(review['stars'])

if len(userReviews) < 5:
    print 'Sorry, your user doesn\'t have enough ratings'
else:
    potNeighbors = {}
    for user_id in reviewDict.keys():
        reviewList = reviewDict[user_id]
        count = 0.0
        bizlist = []
        for review in reviewList:
            for user_review in userReviews:
                #print 'review' + str(review)
                #print user_review
                if review['business_id'] == user_review['business_id']:
                    count += 1
                    bizlist.append(review)
        if count > 5:
            #print 'A match with : ' + str(user_id)
            potNeighbors[user_id] = bizlist

    if len(potNeighbors.keys()) < 10:
        print 'Sorry, your user doesn\'t have enough ratings'
    else:
        bizCountDict = {}
        for review in userReviews:
            for neighbor in potNeighbors.keys():
                for nreview in potNeighbors[neighbor]:
                    if review['business_id'] == nreview['business_id']:
                        if review['business_id'] not in bizCountDict.keys():
                            bizCountDict[review['business_id']] = 0
                        bizCountDict[review['business_id']] += 1

        list = sorted(bizCountDict.iteritems(), key=lambda x: x[1], reverse=True)
        business_to_remove = list[0][0]
        myReview = None
        for review in userReviews:
            if review['business_id'] == business_to_remove:
                myReview = review


        #####INSERTED FROM PREVIOUS CODE #####
        dotProducts = {}
        for user_id in potNeighbors.keys():
            reviewList = potNeighbors[user_id]
            sum = 0.0
            norm_indiv = 0.0
            norm_user = 0.0
            for review in reviewList:
                for user_review in userReviews:
                    if user_review['business_id'] == business_to_remove:
                        continue
                    #print 'review' + str(review)
                    #print user_review
                    if review['business_id'] == user_review['business_id']:
                        sum += int(review['stars']) * int(user_review['stars'])
                        norm_indiv += int(user_review['stars']) ** 2
                        norm_user += int(review['stars']) ** 2

            dotProducts[user_id] = sum/(math.sqrt(norm_indiv)*math.sqrt(norm_user))


        list = sorted(dotProducts.iteritems(), key=lambda x: x[1], reverse=True)

        userToDiff = {}
        for entry in list:
            entrysReviews = reviewDict[entry[0]]
            for review in entrysReviews:
                 if review['business_id'] == business_to_remove:
                     diff = math.fabs(int(myReview['stars']) - int(review['stars']))
                     userToDiff[entry] = diff
                     print ' entry: ' + entry[0] + ' score: ' + str(entry[1]) + ' diff: ' + str(diff)
