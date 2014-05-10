#!/bin/bash
#echo "Hello World"
#counter=1
#for var in "$@"
#do
#    echo "User $counter is $var"
#    let "counter += 1"
#done

python superuser.py $@ > inputfile.txt
rm delete.reg
rm delete.cache
vowpalwabbit/vw /dev/stdin -b 18 -q ui --rank 150 --l2 0.001 --learning_rate 0.015 --passes 10 --decay_learning_rate 0.97 --power_t 0 -f delete.reg --cache_file delete.cache < inputfile.txt
rm inputfile.txt
vowpalwabbit/vw -i delete.reg -p predictions.txt -t superuserpredict.txt
rm delete.reg
rm delete.cache
paste predictions.txt businessIDs.txt | column -s $'\t' -t > delete.txt
sort -nr -k 1 delete.txt > predictions.txt
rm delete.txt