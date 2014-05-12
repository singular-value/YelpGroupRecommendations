import cPickle as pickle
import sys, math

file = open('saveBizDict.p', 'r')
biz_dict = pickle.load( file)
count = 0
for line in sys.stdin:
    rating = float(line.split()[0])
    business = line.split()[-1]
    if ('Food' in biz_dict[business]['categories'] or 'Restaurants' in biz_dict[business]['categories']) and ('Grocery' not in biz_dict[business]['categories'] and 'Convenience Stores' not in biz_dict[business]['categories'] and 'Drugstores' not in biz_dict[business]['categories']) and (rating - float(biz_dict[business]['stars']) > .25):
        print line[:-1], biz_dict[business]['name']
        count += 1
        if count == 20:
            break
