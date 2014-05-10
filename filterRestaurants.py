import cPickle as pickle
import sys

file = open('saveBizDict.p', 'r')
biz_dict = pickle.load( file)
count = 0
for line in sys.stdin:
    business = line.split()[-1]
    if ('Food' in biz_dict[business]['categories'] or 'Restaurants' in biz_dict[business]['categories']) and ('Grocery' not in biz_dict[business]['categories']):
        print line[:-1]
        count += 1
        if count == 10:
            break
