#!/bin/bash

BASE='/mnt/hd-data/Datasets/quickdraw/qd_cat_'

save_sketches(){
	COD=$(printf "%02d" $1)
	CAT=$BASE$COD
	echo "python read_ndjson.py --dir --category $CAT -sample 1100"
}

for i in {1..10} 
do
	save_sketches $i
done
wait
echo "Finishing OK"	
