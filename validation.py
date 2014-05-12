# choose a random restaurant - requires a mapping from restaurants to users
# select a subset of the users who have rated this website
# remove their restaurant rating
import random
import cPickle as pickle
import library
import os, sys
import time

def main(group_size, num_iterations):
    time_start = time.clock()
    b2u_map = pickle.load(open("saveBizToUsersDict.p", "rb"))
    time_loadb2u = time.clock()
    u2r_map = pickle.load(open("saveReviewDictValidation.p", "rb"))
    print "Time to load b2u: " + str(time_loadb2u - time_start)
    print "Time to load u2r: " + str(time.clock() - time_loadb2u)

    # choose a random restaurant
    business_id = random.choice(b2u_map.keys())
    while len(b2u_map[business_id]) < group_size:
        business_id = random.choice(b2u_map.keys())

    final_merged_eval = {}
    final_superuser_eval = {}

    for x in range(0, num_iterations):

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

        time_vw_merge_conversion = time.clock()

        # convert to VW
        file = open("reviews_temp.txt", "wb")
        for user_id in u2r_map:
            for business_id in u2r_map[user_id]:
                file.write(str(u2r_map[user_id][business_id]) + " |u " +
                           user_id + " |i " + business_id + "\n")

        print "Time to write vw imput file for merge: " + str(time.clock() - time_vw_merge_conversion)

        # VowpalWabbit shell script
        os.system("vowpalwabbit/vw -i movielens.reg -p predictions.txt -t reviews_temp.txt")
        id_string = ' '.join(str(x) for x in user_ids)
        print id_string
        os.system("python makePredictionary.py " + id_string)


        data = pickle.load(open("predictionary.p","r"))
        merged_ratings = {}
        for user_id in user_ids:
            merged_ratings[user_id] = data[user_id][business_id]
        merged_ratings_svf = library.evaluate_ratings(data, user_ids, business_id)

        # validate function
        merge_evaluations = validate(original_ratings, original_ratings_svf, merged_ratings_svf)
        print merge_evaluations

        # Superuser version ------------------------------------------------
        user_string = ""
        for user_id in user_ids:
            user_string += user_id + " "

        # create super user
        # convert to VW
        # VowpalWabbit shell script for superuser
        os.system("./StephenApproach.sh " + user_string)
        data = pickle.load(open("predictionary.p","r"))
        superuser_ratings_svf = {}
        superuser_ratings_svf["average"] = float(data[business_id])
    #    os.system("./StephenApproach.sh reviews_temp.txt lm xxx " + user_string)
    #    os.system("./StephenApproach.sh reviews_temp.txt mh xxx " + user_string)
    #    os.system("./StephenApproach.sh reviews_temp.txt expert xxx " + user_string)

        # create super user
        # convert to VW
        # VowpalWabbit shell script for superuser
        os.system("./StephenApproach.sh avg nonorm " + user_string)
        data = pickle.load(open("predictionary.p","r"))
        superuser_ratings_svf = {}
        superuser_ratings_svf["average"] = float(data[business_id])

        os.system("./StephenApproach.sh lm nonorm " + user_string)
        data = pickle.load(open("predictionary.p","r"))
        superuser_ratings_svf["least_misery"] = float(data[business_id])

        os.system("./StephenApproach.sh mh nonorm " + user_string)
        data = pickle.load(open("predictionary.p","r"))
        superuser_ratings_svf["most_happiness"] = float(data[business_id])

        os.system("./StephenApproach.sh expert nonorm " + user_string)
        data = pickle.load(open("predictionary.p","r"))
        superuser_ratings_svf["expert"] = float(data[business_id])
    #    os.system("./StephenApproach.sh reviews_temp.txt lm xxx " + user_string)
    #    os.system("./StephenApproach.sh reviews_temp.txt mh xxx " + user_string)
    #    os.system("./StephenApproach.sh reviews_temp.txt expert xxx " + user_string)

        # validate function
        superuser_evaluations = validate(original_ratings, original_ratings_svf, superuser_ratings_svf)

        # sum up values
        if not final_merged_eval:
            final_merged_eval = merge_evaluations
            final_superuser_eval = superuser_evaluations
        else:
            for svf in merge_evaluations["accuracy"]:
                final_merged_eval["accuracy"][svf] += merge_evaluations["accuracy"][svf]
                final_merged_eval["fairness"][svf] += merge_evaluations["fairness"][svf]
                final_merged_eval["satisfaction"][svf] += merge_evaluations["satisfaction"][svf]
                final_superuser_eval["accuracy"][svf] += superuser_evaluations["accuracy"][svf]
                final_superuser_eval["fairness"][svf] += superuser_evaluations["fairness"][svf]
                final_superuser_eval["satisfaction"][svf] += superuser_evaluations["satisfaction"][svf]

    #divide to get averages
    for svf in merge_evaluations["accuracy"]:
        final_merged_eval["accuracy"][svf] /= num_iterations
        final_merged_eval["fairness"][svf] /= num_iterations
        final_merged_eval["satisfaction"][svf] /= num_iterations
        final_superuser_eval["accuracy"][svf] /= num_iterations
        final_superuser_eval["fairness"][svf] /= num_iterations
        final_superuser_eval["satisfaction"][svf] /= num_iterations

    # read out all the values
    print "n=" + str(num_iterations)
    print "Order: Accuracy, Fairness, Satisfaction on rows"
    print "Order: lm, mh, avg, expert on columns"
    print "Merged"
    sys.stdout.write(str(final_merged_eval["accuracy"]["least_misery"]) + "\t")
    sys.stdout.write(str(final_merged_eval["accuracy"]["most_happiness"]) + "\t")
    sys.stdout.write(str(final_merged_eval["accuracy"]["average"]) + "\t")
    sys.stdout.write(str(final_merged_eval["accuracy"]["expert"]) + "\n")

    sys.stdout.write(str(final_merged_eval["fairness"]["least_misery"]) + "\t")
    sys.stdout.write(str(final_merged_eval["fairness"]["most_happiness"]) + "\t")
    sys.stdout.write(str(final_merged_eval["fairness"]["average"]) + "\t")
    sys.stdout.write(str(final_merged_eval["fairness"]["expert"]) + "\n")

    sys.stdout.write(str(final_merged_eval["satisfaction"]["least_misery"]) + "\t")
    sys.stdout.write(str(final_merged_eval["satisfaction"]["most_happiness"]) + "\t")
    sys.stdout.write(str(final_merged_eval["satisfaction"]["average"]) + "\t")
    sys.stdout.write(str(final_merged_eval["satisfaction"]["expert"]) + "\n")

    print "Superuser"
    sys.stdout.write(str(final_superuser_eval["accuracy"]["least_misery"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["accuracy"]["most_happiness"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["accuracy"]["average"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["accuracy"]["expert"]) + "\n")

    sys.stdout.write(str(final_superuser_eval["fairness"]["least_misery"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["fairness"]["most_happiness"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["fairness"]["average"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["fairness"]["expert"]) + "\n")

    sys.stdout.write(str(final_superuser_eval["satisfaction"]["least_misery"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["satisfaction"]["most_happiness"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["satisfaction"]["average"]) + "\t")
    sys.stdout.write(str(final_superuser_eval["satisfaction"]["expert"]) + "\n")



def validate(actual, actual_svf, predicted_svf):

    evaluations = {}

    # accuracy
    accuracy = {}
    for svfp in predicted_svf:
        accuracy[svfp] = abs(actual_svf[library.SVF.average] - predicted_svf[svfp])
    evaluations["accuracy"] = accuracy

    # fairness
    fairness = {}

    for svf in predicted_svf:
        dev_from_pred = 0
        actual_dev = 0
        for user_id in actual:
            actual_dev += (actual[user_id] - actual_svf[library.SVF.average]) ** 2
            dev_from_pred += (actual[user_id] - predicted_svf[svf]) ** 2
        fairness[svf] = abs(actual_dev - dev_from_pred)
    evaluations["fairness"] = fairness

    # satisfaction
    satisfaction = {}
    for svf in predicted_svf:
        satisfaction[svf] = abs(actual_svf[svf] - predicted_svf[svf])
    evaluations["satisfaction"] = satisfaction

    print "EVALUATIONS"
    for svf in evaluations["satisfaction"]:
        print svf
        print "accuracy:\t" + str(evaluations["accuracy"][svf])
        print "fairness:\t" + str(evaluations["fairness"][svf])
        print "satisfaction:\t" + str(evaluations["satisfaction"][svf])

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

validate(actual, actual_svf, predicted_svf)
#main(sys.argv[1], sys.argv[2])
