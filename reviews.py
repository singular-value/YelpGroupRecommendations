# checks the distribution of reviews
import cPickle as pickle

ratings = [0, 0, 0, 0, 0, 0]

u2r_map = pickle.load(open("saveReviewDictValidation.p", "rb"))
# for user_id in u2r_map:
#     if len(u2r_map[user_id]) > 1:
#         for business_id in u2r_map[user_id]:
#             ratings[int(u2r_map[user_id][business_id])] += 1
# print ratings

for user_id in u2r_map:
    average = 0.0
    count = 0.0
    for business_id in u2r_map[user_id]:
        average += float(u2r_map[user_id][business_id])
        count += 1
    print str(count) + "," + str(average / count)