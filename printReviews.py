import cPickle as pickle
import sys, math

biz_dict = pickle.load(open('saveBizDict.p','r'))
review_dict = pickle.load(open('saveReviewDict.p','r'))

for i in xrange(len(sys.argv)-1):
    print "User anonymized ID: " + sys.argv[i+1]
    for review in review_dict[sys.argv[i+1]]:
        print review['stars'] + "/5, " + biz_dict[review['business_id']]['name']
    print
