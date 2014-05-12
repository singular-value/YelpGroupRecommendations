#!/bin/bash

python predict.py ${@:2} | vowpalwabbit/vw -i movielens.reg -p predictions.txt -t
python makePredictionary.py ${@:2}
rm predictions.txt
python merging.py $@ > predictions.txt
python filterRestaurants.py < predictions.txt
rm predictions.txt
python printReviews.py ${@:2}

#python makePredictionary.py $@
#paste predictions.txt businessIDs.txt | column -s $'\t' -t > delete.txt
#sort -nr -k 1 delete.txt | python filterRestaurants.py
#rm delete.txt