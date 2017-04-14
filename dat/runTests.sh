#!/bin/bash
# Runs Emergen(e)tic with a series of scripts

GEN="30"
CAN="20"

dnc "emergenetic.dn"

for FILE in ./scripts/*; do
	FILE=${FILE##*/}
	FILE=${FILE%.script}

	dana "emergenetic" $FILE $GEN $CAN
	
	for DIR in ./cache/*; do
		(cd "$DIR" && rm *.o)
	done
	cd results/ && rm *.txt && cd ..
	tar -jcvf ./archives/$FILE.bz2 cache
	rm -R cache
	cp -a ./cachebackup ./cache
done

echo 'Complete.' >complete.txt
