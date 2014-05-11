# merging.py - The program to merge the predicted reviews of users
import cPickle as pickle
import library
import operator
import sys

# The number of users
group_size = len(sys.argv)-1


def main():

    full_data = pickle.load(open("predictionary.p", "rb"))
    # full_data = \
    #     {
    #         "a": {"1": 0.5, "2": 0.1, "3": 0.1, "4": 0.1, },
    #         "b": {"1": 0.5, "2": 0.3, "3": 0.1, "4": 0.5, },
    #         "c": {"1": 0.5, "2": 0.5, "3": 0.1, "4": 0.7, },
    #         "d": {"1": 0.5, "2": 0.7, "3": 0.1, "4": 0.3, },
    #         "e": {"1": 0.5, "2": 0.9, "3": 0.1, "4": 0.6, },
    #     }
    # pickle.dump(full_data, open('data.p','wb'))

    group_ids = sys.argv[1:]
    merge = {}

    # for each business, get the ratings, then combine the user data based on the SVF
    for business_id in full_data[group_ids[0]]:

        # obtain an object containing all svf values
        merge[business_id] = library.evaluate_ratings(full_data, group_ids, business_id)

    merge = sorted(merge.iteritems(), key=lambda x: x[1][library.SVF.average], reverse=True)
    for key, val in merge:
        print str(val["average"]) + ' ' + str(key)

main()
