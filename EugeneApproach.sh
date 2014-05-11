#!/bin/bash
#echo "Hello World"
#counter=1
#for var in "$@"
#do
#    echo "User $counter is $var"
#    let "counter += 1"
#done

python predict.py $@ | vowpalwabbit/vw -i movielens.reg -p predictions.txt -t
paste predictions.txt businessIDs.txt | column -s $'\t' -t > delete.txt
sort -nr -k 1 delete.txt | python filterRestaurants.py
rm delete.txt