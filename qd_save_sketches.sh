#!/bin/bash

BASE='/mnt/hd-data/Datasets/quickdraw/qd_cat_'
DIR='/mnt/hd-data/Datasets/quickdraw/'
save_sketches(){
	COD=$(printf "%02d" $1)
	CAT=$BASE$COD
	python read_ndjson.py -dir $DIR -category $CAT -sample 1100
}

for i in {1..4} 
do
	save_sketches $i &
done
wait
echo "Finishing OK"	
