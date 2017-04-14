#!/bin/bash
# Performs pre-run setup before a test run.

GENS=$1
SCRIPT=$2

cp ./cachebackup/CacheHandlerBase.dn ./cache/CacheHandlerBase.dn
mkdir ./cache/$2
mkdir ./results/$2
for i in `seq 0 $1`; do
	mkdir ./cache/$2/$i
   touch ./results/$2/results$i.txt
done
