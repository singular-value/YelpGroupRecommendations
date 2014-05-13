import random


class SVF():
    most_happiness = "most_happiness"
    least_misery = "least_misery"
    average = "average"
    expert = "expert"


# choose a random group of group_size
def choose_random_ids(data, group_size):
    user_ids = []
    id_set = set()

    for x in range(0, group_size):
        user_id = random.choice(data.keys())
        while user_id in id_set:
            user_id = random.choice(data.keys())
        id_set.update(user_id)
        user_ids.append(user_id)

    return user_ids


def evaluate_ratings(data, user_ids, business_id, original_data):
    svf = {}
    group_size = len(user_ids)

    min = data[user_ids[0]][business_id]
    for x in range(1, group_size):
        current = data[user_ids[x]][business_id]
        min = current if current < min else min
    svf[SVF.least_misery] = min

    most = data[user_ids[0]][business_id]
    for x in range(1, group_size):
        current = data[user_ids[x]][business_id]
        most = current if current < most else most
    svf[SVF.most_happiness] = most

    average = 0.0
    for x in range(0, group_size):
        average += data[user_ids[x]][business_id]
    merged_value = float(average) / float(group_size)
    svf[SVF.average] = merged_value

    expert = 0.0
    total_count = 0.0
    for x in range(0, group_size):
        count = len(original_data[user_ids[x]])
        expert += count * data[user_ids[x]][business_id]
        total_count += count
    svf[SVF.expert] = expert / total_count

    return svf

def evaluate_ratings2(data, user_ids, business_id):
    svf = {}
    group_size = len(user_ids)

    # give the indices to save time

    marked_indices = {}
    ratings = {}
    for user_id in user_ids:
        for index, val in enumerate(data[user_id]):
            if val["business_id"] == business_id:
                ratings[user_id] = float(val["stars"])
                marked_indices[user_id] = index
                break
    svf["ratings"] = ratings
    svf["marked_indices"] = marked_indices

    min = ratings[user_ids[0]]
    for x in range(1, group_size):
        current = ratings[user_ids[x]]
        min = current if current < min else min
    svf[SVF.least_misery] = min

    most = ratings[user_ids[0]]
    for x in range(1, group_size):
        current = ratings[user_ids[x]]
        most = current if current > min else min
    SVF[SVF.most_happiness] = most

    average = 0
    for x in range(1, group_size):
        average +=  ratings[user_ids[x]]
    svf[SVF.average] = float(average) / float(group_size)

    # # this whole mess means - search through the user's list of reviews for the first one that
    # # has a matching business_id attribute. Then get the star value and cast it to an int
    # min = float(next((x for x in data[user_ids[0]] if x["business_id"] == business_id), None)["stars"])
    # for x in range(1, group_size):
    #     current = float(next((x for x in data[user_ids[x]] if x["business_id"] == business_id), None)["stars"])
    #     min = current if current < min else min
    # svf[SVF.least_misery] = min
    #
    # average = 0.0
    # for x in range(0, group_size):
    #     average += float(next((x for x in data[user_ids[x]] if x["business_id"] == business_id), None)["stars"])
    # merged_value = float(average) / float(group_size)
    # svf[SVF.average] = merged_value

    return svf