import pickle, sys

file = open('saveBizDict.p', 'r')
biz_dict = pickle.load( file)
for line in sys.stdin:
    business = line.split()[-1]
    if 'Food' in biz_dict[business]['categories'] and 'Restaurants' in biz_dict[business][categories] and 'Grocery' not in biz_dict[business][categories]:
        print line

