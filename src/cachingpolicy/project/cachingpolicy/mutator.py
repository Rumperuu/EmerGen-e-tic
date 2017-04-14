#!/usr/bin/python

'''
                             CachingPolicy 0.9                            
                    Copyright (c) 2017 Ben Goldsworthy (rumps)                   
                                                                               
    CachingPolicy is an EmerGen(e)tic module for testing the use of genetic
	algorithms as applied to the cache updating behaviour of a web server.
                                                                            
    This file is part of the CachingPolicy EmerGen(e)tic module.
	
	CachingPolicy is free software: you can redistribute it and/or modify        
	it under the terms of the GNU General Public License as published by       
	the Free Software Foundation, either version 3 of the License, or          
	(at your option) any later version.                                        
																			   
	CachingPolicy is distributed in the hope that it will be useful,             
	but WITHOUT ANY WARRANTY; without even the implied warranty of             
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              
	GNU General Public License for more details.                               
																			   
	You should have received a copy of the GNU General Public License          
	along with CachingPolicy.  If not, see <http://www.gnu.org/licenses/>.     
'''

import fileinput
import math
import random
import shutil
import sys
import os

# This script generates the initial population of candidate programs,
# and performs mutation/crossover for each subsequent generation.

# Mutation probability variables, to be read in from the config file upon the 
# first run of the mutation/crossover methods.
# 0: Mutation chance
# 1: Crossover chance
# 2: Binary Operator Mutation chance
# 3: Operand Mutation chance
# 4: nthMost* Mutation chance
# 5: Create Subtree Mutation chance

probabilities = [None for x in range(6)]

with open("./project/cachingpolicy/config.conf") as inFile:
	for i, line in enumerate(inFile):
		if i == 6:
			intRange = int(line.partition(":")[2])	

binaryOperators = ["*", "+", "-", "/"]
operands = [str(n) for n in range(intRange)]
for n in range(intRange):
	operands.append("nthMostRecentlyUsed(0)")
	operands.append("nthMostFrequentlyUsed(0)")
operands.append("random()")
verbose = False
script = ""

def getSubLists(lst):
	"""Recursively gets every sub-tree of a given expression."""
	subLists = []
	for token in lst:
		if isinstance(token, list):
			subLists.append(token)
			if getSubLists(token) is not None:
				subLists.append(getSubLists(token)[0])
	if len(subLists) == 0: return None
	elif len(subLists) == 1: return subLists[0]
	else: return subLists
	
def crossover(parentA, parentB):
	"""Crosses over a random subtree from chromosome A to a random point on
	chromosome B."""
	if verbose: print("\tCrossover: Parent A (", compile(parentA), ") x Parent B (", compile(parentB), ")")
	
	subTrees = []
	for i, token in enumerate(parentA):
		if isinstance(token, list):
			subTrees.append(token)
			subLists = getSubLists(token)
			if subLists is not None:
				subTrees.append(subLists)
	
	changePoint = []
	
	temp = 0
	while 1:
		# DEBUG - trying to avoid the endless loop error, if this is the cause.
		temp += 1
		if temp > 1000: break
		#/DEBUG
		changePoint = random.choice(parentB)
		if not isinstance(changePoint, list):
			if str(changePoint).isnumeric():
				break
	if len(subTrees) > 0:
		newSubTree = random.choice(subTrees)
		if verbose: print("\t\tResult: "+compile(newSubTree)+" replaced operand "+changePoint+" ("+compile([newSubTree if x==changePoint else x for x in parentB])+")")
		return [newSubTree if x==changePoint else x for x in parentB]
	else: return [parentB]
	
def mutate(chromosome, initialPop = None):
	"""Recursively applies, to each token, a random chance of mutating 
	a given operand, operator, or replacing the former with an entirely 
	new expression."""	
	if probabilities[2] is None:
		with open("./project/cachingpolicy/config.conf") as inFile:
			for i, line in enumerate(inFile):
				if i < 6 and i > 1:
					probabilities[i] = int(line.partition(":")[2])
			
	operandMutChance = 100 if initialPop else probabilities[3]
	
	for i, token in enumerate(chromosome):
		if verbose: print("\tMutating: "+compile(chromosome))
		token = str(token)
		
		if len(chromosome) < 3:
			if random.randrange(100) < probabilities[5]:# and "nthMost" not in token:
				if len(chromosome) == 1:
					chromosome.append(random.choice(binaryOperators))
					chromosome.append(random.randrange(intRange))
				elif random.randrange(100) < 50:
					chromosome.remove(chromosome[0])
				else:
					chromosome[1] = [random.choice(operands), random.choice(binaryOperators), random.choice(operands)] 
					
		else:
			if isinstance(token, list):
				chromosome[i] = mutate(token)
				
			if token in binaryOperators and random.randrange(100) < probabilities[2]:
				chromosome[i] = random.choice(binaryOperators)
			elif token.isnumeric() and random.randrange(100) < operandMutChance:
				chromosome[i] = random.choice(operands)
		'''
		elif "nthMost" in token and random.randrange(100) < probabilities[4]:
			if random.randrange(100) < 50:
				chromosome[i] = "nthMostRecentlyUsed" if token == "nthMostFrequentlyUsed" else "nthMostFrequentlyUsed"
			else:
				chromosome.remove(token)
		'''
		if verbose: print("\t\tResult: "+compile(chromosome))
	
	return chromosome
	
def parse(chromosome):
	"""Given a `str` representation of a chromosome, recursively parses
	it into a `List`."""
	i = 0
	counter = 0
	substring = ""
	result = []
	while i < len(chromosome):
		if chromosome[i] is "r":
			i += len("random()")
			result.append("random()")
		elif chromosome[i] is "n":
			function = ""
			if chromosome[i+7] is "F":
				function = "nthMostFrequentlyUsed"
			elif chromosome[i+7] is "R":
				function = "nthMostRecentlyUsed"
			i += len(function)-1
			result.append(function)
		elif chromosome[i] is "(":
			substring = ""
			for j in chromosome[i:]:
				if j is "(":
					counter += 1
				elif j is ")":
					counter -= 1
				substring += j
				if counter == 0:
					result.append(parse(substring[1:(len(substring)-1)]))
					i += len(substring) - 1
					break
		elif chromosome[i].isnumeric():
			num = ""
			while chromosome[i].isnumeric():
				num += chromosome[i]
				i += 1
				if i == len(chromosome):
					break
			if len(num) > 0:
				i -= 1
			result.append(num)
		elif chromosome[i] in binaryOperators:
			result.append(chromosome[i])
		i += 1
	return result

def compile(chromosome):
	"""Given a `List` representation of a chromosome, recursively compiles 
	it into a `str`."""
	string = ""
	for i in chromosome:
		if isinstance(i, list):
			string += "("
			string += compile(i)
			string += ")"
		else:
			string += str(i)
	return string
	
def createInitialPop(candidates):
	"""Creates the initial population for generation 0."""
	for i in range(candidates):
		cID = "0_"+str(i)
		shutil.copyfile("./cache/CacheHandlerBase.dn", "./cache/"+script+"/0/CacheHandler"+cID+".dn")
		writeChromosomeToFile(cID, parse(readChromosomeFromFile(cID)))
		os.system("dnc ./cache/"+script+"/0/CacheHandler"+cID+".dn")
		
def readChromosomeFromFile(cID):
	"""Reads the chromosome from a given `CacheHandler*.dn` file."""
	with open("./cache/"+script+"/"+str(cID.partition("_")[0])+"/CacheHandler"+cID+".dn") as inFile:
		for line in inFile:
			if "// BEGIN" in line:
				return next(inFile).partition(" = ")[2].rstrip()
			
def writeChromosomeToFile(cID, chromosome):
	"""Writes a given chromosome to a `CacheHandler*.dn` file."""
	shutil.copyfile("./cache/CacheHandlerBase.dn", "./cache/"+script+"/"+str(cID.partition("_")[0])+"/CacheHandler"+cID+".dn.temp")
	with open("./cache/"+script+"/"+str(cID.partition("_")[0])+"/CacheHandler"+cID+".dn.temp") as inFile:
		with open("./cache/"+script+"/"+str(cID.partition("_")[0])+"/CacheHandler"+cID+".dn", "w") as outFile:
			for line in inFile:
				outFile.write(line)
				if "// BEGIN" in line:
					outFile.write("\t\t\t\tindex = "+compile(chromosome[0])+"\n")
					next(inFile)
	os.remove("./cache/"+script+"/"+str(cID.partition("_")[0])+"/CacheHandler"+cID+".dn.temp")

def hasSubTrees(chromosome):
	for x in chromosome[0]:
		if isinstance(x, list): return True
	else: return False

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
	global verbose
	verbose = True if int(args[2]) == 1 else False
	
	if generation == 0:
		createInitialPop(candidates)
	else:
		# Gets all of the previous generation's chromosomes.
		for i in range(candidates):
			oldCID = str(generation - 1) + "_" + str(i)
			chromosomes.append((parse(readChromosomeFromFile(oldCID)), oldCID))
		
		# Reads in the results of the previous generation's chromosomes.
		rankSelect = []
		with open("./results/"+script+"/results"+str(generation-1)+".txt") as inFile:
			for line in inFile:
				rankSelect.append([line.partition(":")[0], line.partition(":")[2].partition("ms")[0]])
		# Sorts them by response time
		rankSelect.sort(key=lambda x: int(x[1]))
		# Truncates the bottom 90% of the candidates
		del rankSelect[int(math.ceil(candidates/10)):]
		
		remainingIDs = [str(n) for n in range(candidates)]
		
		# Retains the top 10% best-peforming chromosomes for the next 
		# generation.
		if verbose: print("\nApplying rank selection to top 10% from prev. generation...")
		for currCandidate, oldCID in enumerate(rankSelect):
			newCID = str(generation) + "_" + str(oldCID[0].partition("_")[2])
			for chromosome in chromosomes:
				if chromosome[1] == oldCID[0]:
					if verbose: print("\tResult: "+str(oldCID[0])+" copied to "+newCID)
					newChromosome = [chromosome[0], newCID]
					newChromosomes.append(newChromosome)
					#chromosomes.remove(chromosome)
					remainingIDs.remove(newCID.partition("_")[2])
					break
		if verbose: print("\n")
		
		if probabilities[0] is None:
			with open("./project/cachingpolicy/config.conf") as inFile:
				for i, line in enumerate(inFile):
					if i > 1: break
					probabilities[i] = int(line.partition(":")[2])
		
		# For the remaining chromosomes, creates the next generation's
		# population, whilst having a chance to affect mutation or
		# crossover operations on each.
		for currCandidate, chromosome in enumerate(chromosomes):
			if str(currCandidate) in remainingIDs:
				newCID = str(generation) + "_" + str(currCandidate)
				
				newChromosome = [chromosome[0], newCID]
				if random.randrange(100) < probabilities[0]:
					haveSubTrees = [x for x in chromosomes if hasSubTrees(x)]
					if len(haveSubTrees) > 1:
						parentB = random.choice(haveSubTrees)[0]
						if hasSubTrees(chromosome[0]):
							if verbose: print("Crossing over into "+newCID)
							newChromosome = [crossover(chromosome[0], parentB, verbose), newCID]
							if verbose: print("Crossover finish.")
							
				if random.randrange(100) < probabilities[1]:
					if verbose: print("Mutating "+str(generation-1) + "_" + str(currCandidate)+"->"+newCID+":")
					newChromosome = [mutate(chromosome[0], True), newCID]
					if verbose: print(str(generation-1) + "_" + str(currCandidate)+"->"+newCID+" mutation finish.\n")
					
					
				newChromosomes.append(newChromosome)
		
		# Writes this new population to `.dn` files, and then runs the
		# Dana compiler on the.
		for currCandidate, chromosome in enumerate(newChromosomes):
			newCID = str(generation) + "_" + str(currCandidate)
			writeChromosomeToFile(newCID, chromosome)
			os.system("dnc ./cache/"+script+"/"+str(newCID.partition("_")[0])+"/CacheHandler"+newCID+".dn")
	return 0
	
if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
