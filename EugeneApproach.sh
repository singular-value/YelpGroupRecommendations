#!/bin/bash

python predict.py $@ | vowpalwabbit/vw -i movielens.reg -p predictions.txt -t
python makePredictionary.py $@
rm predictions.txt
#python makePredictionary.py $@
#paste predictions.txt businessIDs.txt | column -s $'\t' -t > delete.txt
#sort -nr -k 1 delete.txt | python filterRestaurants.py
#rm delete.txt