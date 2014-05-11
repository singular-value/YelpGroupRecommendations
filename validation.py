# choose a random restaurant - requires a mapping from restaurants to users
# select a subset of the users who have rated this website
# remove their restaurant rating
import random
import cPickle as pickle
import library

# The number of users
group_size = 5


b2u_map = pickle.load(open("saveBizToUsersDict.p", "rb"))
u2r_map = {}

def main():
    # choose a random restaurant
    business_id = random.choice(b2u_map.keys())
    while len(b2u_map[business_id]) < group_size:
        business_id = random.choice(b2u_map.keys())

    # choose a subset of group_size users
    user_ids = random.sample(b2u_map[business_id], group_size)

    # apply social value function on data
    print library.evaluate_ratings(u2r_map, user_ids, business_id)

    # get their original ratings of the restaurant
    # remove ratings from dataset
    original_ratings = {}
    for user_id in user_ids:
        original_ratings[user_id] = u2r_map[user_id].pop(business_id)

    # Merge version ----------------------------------------------------

    # convert to VR

    # VowpalRabbit shell script

    # retrieve user rows

    # merge values

    # validate function

    # Superuser version ------------------------------------------------

    # create super user

    # convert to VR

    # VowpalRabbit shell script for superuser

    # convert to

    # retrieve superuser values

    # validate function

def validate(actual, actual_svf, predicted, predicted_svf):

    evaluations = {}

    # accuracy
    accuracy = {}
    for svfa in actual_svf:
        accuracy[svfa] = {}
        for svfp in predicted_svf:
            accuracy[svfa][svfp] = abs(actual_svf[svfa] - predicted_svf[svfp])
    evaluations["accuracy"] = accuracy

    # fairness
    evaluations["fairness"] = 0


    # satisfaction
    evaluations["satisfaction"] = 0

    return evaluations

main()