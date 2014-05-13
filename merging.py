# merging.py - The program to merge the predicted reviews of users
import cPickle as pickle
import library
import operator
import sys

# The number of users
group_size = len(sys.argv)-2

def least_misery(data, user_ids, business_id):
    min = data[user_ids[0]][business_id]
    for x in range(1, group_size):
        current = data[user_ids[x]][business_id]
        min = current if current < min else min
    return min

def most_happiness(data, user_ids, business_id):
    most = data[user_ids[0]][business_id]
    for x in range(1, group_size):
        current = data[user_ids[x]][business_id]
        most = current if current < most else most
    return most

def average(data, user_ids, business_id):
    average = 0.0
    for x in range(0, group_size):
        average += data[user_ids[x]][business_id]
    merged_value = float(average) / float(group_size)
    return merged_value

def expert(data, user_ids, business_id, original_data):
    expert = 0.0
    total_count = 0.0
    for x in range(0, group_size):
        count = len(original_data[user_ids[x]])
        expert += count * data[user_ids[x]][business_id]
        total_count += count
    return expert / total_count

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

    svf = sys.argv[1]
    group_ids = sys.argv[2:]
    merge = {}

    original_reviews = {}
    if svf == "expert":
        original_reviews = pickle.load(open("saveReviewDictValidation.p", "rb"))

    # for each business, get the ratings, then combine the user data based on the SVF
    for business_id in full_data[group_ids[0]]:

        # obtain an object containing all svf values
        if svf == "lm":
            merge[business_id] = least_misery(full_data, group_ids, business_id)
        elif svf == "mh":
            merge[business_id] = most_happiness(full_data, group_ids, business_id)
        elif svf == "avg":
            merge[business_id] = average(full_data, group_ids, business_id)
        elif svf == "expert":
            merge[business_id] = expert(full_data, group_ids, business_id, original_reviews)

    merge = sorted(merge.iteritems(), key=lambda x: x[1], reverse=True)
    for key, val in merge:
        print str(val) + ' ' + str(key)

main()
