import random


class SVF():
    most_happiness = "most_happiness"
    least_misery = "least_misery"
    average = "average"


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


def evaluate_ratings(data, user_ids, business_id):
    svf = {}
    group_size = len(user_ids)

    min = data[user_ids[0]][business_id]
    for x in range(1, group_size):
        current = data[user_ids[x]][business_id]
        min = current if current < min else min
    svf[SVF.least_misery] = min

    average = 0.0
    for x in range(0, group_size):
        average += data[user_ids[x]][business_id]
    merged_value = float(average) / float(group_size)
    svf[SVF.average] = merged_value

    return svf