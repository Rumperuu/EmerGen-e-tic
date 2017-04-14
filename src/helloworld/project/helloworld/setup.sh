#!/bin/bash
# Performs pre-run setup before a test run.

GENS=$1
SCRIPT=$2

mkdir helloworld
touch ./results/$2/results.csv
echo "Hello world" > ./helloworld/helloworld.txt
mkdir ./helloworld/$2
for i in `seq 0 $1`; do
	mkdir ./helloworld/$2/$i
done
