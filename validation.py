# choose a random restaurant - requires a mapping from restaurants to users
# select a subset of the users who have rated this website
# remove their restaurant rating
import random
import cPickle as pickle
import library
import os
import merging

# The number of users
group_size = 5


def main():
    b2u_map = pickle.load(open("saveBizToUsersDict.p", "rb"))
    u2r_map = {}

    # choose a random restaurant
    business_id = random.choice(b2u_map.keys())
    while len(b2u_map[business_id]) < group_size:
        business_id = random.choice(b2u_map.keys())

    # choose a subset of group_size users
    user_ids = random.sample(b2u_map[business_id], group_size)

    # apply social value function on data
    original_ratings_svf = library.evaluate_ratings(u2r_map, user_ids, business_id)

    # get their original ratings of the restaurant
    # remove ratings from dataset
    original_ratings = {}
    for user_id in user_ids:
        original_ratings[user_id] = u2r_map[user_id].pop(business_id)

    # Merge version ----------------------------------------------------

    # convert to VW
    file = open("reviews_temp.txt", "wb")
    for user_id in u2r_map:
        for business_id in u2r_map[user_id]:
            file.write(u2r_map[user_id][business_id] + " |u " +
                       user_id + " |i " + business_id)

    # VowpalWabbit shell script
    os.system("")

    # retrieve user rows + merge values
    data = pickle.load(open("vowpalwabbit output file"))
    merged_ratings = {}
    for user_id in user_ids:
        merged_ratings[user_id] = data[user_id][business_id]
    merged_ratings_svf = library.evaluate_ratings(data, user_ids, business_id)

    # validate function
    merge_evaluations = validate(original_ratings, original_ratings_svf, merged_ratings, merged_ratings_svf)

    # Superuser version ------------------------------------------------
    user_string = ""
    for user_id in user_ids:
        user_string += user_id + " "

    # create super user
    # convert to VW
    # VowpalWabbit shell script for superuser
    os.system("./StephenApproach.sh reviews_temp.txt avg xxx " + user_string)
    os.system("./StephenApproach.sh reviews_temp.txt lm xxx " + user_string)
    os.system("./StephenApproach.sh reviews_temp.txt mh xxx " + user_string)
    os.system("./StephenApproach.sh reviews_temp.txt expert xxx " + user_string)

    # retrieve superuser values

    # validate function

def validate(actual, actual_svf, predicted, predicted_svf):

    evaluations = {}

    # accuracy
    accuracy = {}
    for svfp in predicted_svf:
        accuracy[svfp] = abs(actual_svf[library.SVF.average] - predicted_svf[svfp])
    evaluations["accuracy"] = accuracy

    # fairness
    dev_from_pred = 0
    actual_dev = 0
    for user_id in actual:
        actual_dev += (actual[user_id] - actual_svf[library.SVF.average]) ** 2
        dev_from_pred += (predicted[user_id] - predicted_svf[library.SVF.average]) ** 2
    evaluations["fairness"] = abs(actual_dev - dev_from_pred)

    # satisfaction
    satisfaction = {}
    for svfa in actual_svf:
        satisfaction[svfa] = {}
        for svfp in predicted_svf:
            satisfaction[svfa][svfp] = abs(actual_svf[svfa] - predicted_svf[svfp])
    evaluations["satisfaction"] = satisfaction

    print evaluations["accuracy"]
    print evaluations["fairness"]
    for svfa in evaluations["satisfaction"]:
        print
        print svfa
        for svfp in evaluations["satisfaction"][svfa]:
            print svfp + ": " + str(evaluations["satisfaction"][svfa][svfp])

actual = {
    1: 5.0,
    2: 5.0,
    3: 5.0,
    4: 5.0,
    5: 5.0
}
actual_svf = {
    library.SVF.average: 5.0,
    library.SVF.least_misery: 5.0,
    library.SVF.most_happiness: 5.0,
    library.SVF.expert: 5.0,
}
predicted = {
    1: 5.0,
    2: 4.0,
    3: 4.0,
    4: 4.0,
    5: 4.0
}
predicted_svf = {
    library.SVF.average: 4.2,
    library.SVF.least_misery: 4.0,
    library.SVF.most_happiness: 5.0,
    library.SVF.expert: 5.0,
}

validate(actual, actual_svf, predicted, predicted_svf)
#main()