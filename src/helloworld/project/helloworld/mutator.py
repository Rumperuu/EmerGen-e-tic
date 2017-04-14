#!/usr/bin/python

'''
                             HelloWorld 1.0                            
                    Copyright (c) 2017 Ben Goldsworthy (rumps)                   
                                                                               
    HelloWorld is an EmerGen(e)tic module for testing the function of the
	EmerGen(e)tic framework.
                                                                            
    This file is part of the HelloWorld EmerGen(e)tic module.
	
	HelloWorld is free software: you can redistribute it and/or modify        
	it under the terms of the GNU General Public License as published by       
	the Free Software Foundation, either version 3 of the License, or          
	(at your option) any later version.                                        
																			   
	HelloWorld is distributed in the hope that it will be useful,             
	but WITHOUT ANY WARRANTY; without even the implied warranty of             
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              
	GNU General Public License for more details.                               
																			   
	You should have received a copy of the GNU General Public License          
	along with HelloWorld.  If not, see <http://www.gnu.org/licenses/>.     
'''

import fileinput
import random
import shutil
import string
import sys

script = ""

def mutate(chromosome):
	"""Randomly replaces letters in the string."""
	mutation = [random.choice(string.ascii_lowercase) if random.randrange(100) < 20 else x for x in "Hello world"]
	return ''.join(mutation)

def createInitialPop(candidates):
	"""Creates the initial population for generation 0."""
	for i in range(candidates):
		cID = "0_"+str(i)
		shutil.copyfile("./helloworld/helloworld.txt", "./helloworld/"+script+"/0/helloworld"+cID+".txt")
		
def readChromosomeFromFile(cID):
	"""Reads the chromosome from a given `CacheHandler*.dn` file."""
	with open("./helloworld/"+script+"/"+str(cID.partition("_")[0])+"/helloworld"+cID+".txt") as inFile:
		return inFile.readline()
			
def writeChromosomeToFile(cID, chromosome):
	"""Writes a given chromosome to a `CacheHandler*.dn` file."""
	with open("./helloworld/"+script+"/"+str(cID.partition("_")[0])+"/helloworld"+cID+".txt", "w") as outFile:
		outFile.write(chromosome)


def main(args):
	random.seed()
	
	tabLevel = ""
	chromosome = []
	generation = int(args[0])
	candidates = int(args[1])
	chromosomes = []
	newChromosomes = []
	global script
	script = args[3]
	
	if generation == 0:
		createInitialPop(candidates)
	else:
		# Gets all of the previous generation's chromosomes.
		for i in range(candidates):
			oldCID = str(generation - 1) + "_" + str(i)
			chromosomes.append((readChromosomeFromFile(oldCID), oldCID))
		
		# Applies a 30% chance of changing the string.
		for currCandidate, chromosome in enumerate(chromosomes):
			newCID = str(generation) + "_" + str(currCandidate)
			
			if random.randrange(100) < 30:
				newChromosome = [mutate(chromosome[0]), newCID]
			else:
				newChromosome = [chromosome[0], newCID]
			print(newChromosome)
			newChromosomes.append(newChromosome)
	
		# Writes this new population to `.txt` files.
		for currCandidate, chromosome in enumerate(newChromosomes):
			newCID = str(generation) + "_" + str(currCandidate)
			writeChromosomeToFile(newCID, chromosome[0])
	return 0
	
if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
