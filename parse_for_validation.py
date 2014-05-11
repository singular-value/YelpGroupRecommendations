import json
import pickle
import time

dataset = open("yelp_academic_dataset_review.json",'r')

lines = dataset.readlines()

# stores the valuable data
review_dict = {}
# stores the dates
review_data_dict = {}
for line in lines:
    # ignore these lines
    if line[0] != '{':
        continue
    o = json.loads(str(line))

    if o['type'] == "review":

        #data with long ids
        user_id = str(o['user_id'])
        business_id = str(o['business_id'])
        date = time.strptime(str(o['date']), '%Y-%m-%d')
        review = int(o['stars'])

        #Is the user's id already in the dictionary?
        if user_id in review_data_dict:
            # iterate through each review by that user
            if business_id in review_data_dict[user_id]:
                # if the business is the same, but the new review's date is more recent, update
                if date > review_data_dict[user_id][business_id]:
                    review_dict[user_id][business_id] = review
            else:
                review_dict[user_id][business_id] = review
        else:
            # if the user id was never there, just create a new dict and add it to the dict entry
            review_dict[user_id] = {business_id: review}
            review_data_dict[user_id] = {business_id: date}

f = open('saveReviewDictValidation.p', 'wb')

pickle.dump(review_dict, f)
f.close()