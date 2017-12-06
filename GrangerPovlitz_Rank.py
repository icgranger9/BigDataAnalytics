import copy
import numpy as np
import pandas as pd
import itertools
import sys
import GrangerPovlitz_Score as scr


def rank_setup():
	rankedData = pd.read_csv("Ranked_Data.csv") # TODO: remove hardcoding filename
	rankedData = rankedData.iloc[:, 1:]
	return rankedData

def determine_c(data, N):
	cutoff = 0
	for attr in N:
		for i in range(data.shape[0]):
			cutoff += scr.score_individual(data, i, N)
	return cutoff

def rank_individual(data, i, N, rankData, cutoff):
	iRank = 0
	for attr in N:
		iRank += rankData.iloc[i, attr]
	#print "iRank, cutoff: " + str(iRank) + ",\t" + str(cutoff);
	numElements = 720 * len(N)
	if iRank < (numElements - cutoff): # TODO: remove hardcoding 720
		return 0
	else:
		return 1

def rank_total(scoresData, ranksData, N, precisionAt):
	accuracyList = []
	c = determine_c(scoresData, N)

	for precision in precisionAt:
		accuracy = 0.0
		# if debug:
		# 	print "cutoff for precision " + str(precision) + " is " + str(cutoff)
		for x in range(precision):
			result = rank_individual(scoresData, x, N, ranksData, c)
			if result != scr.score_individual(scoresData, x, N):
				pass
				# print "inconsistency at x: " + str(x) + "\tvalue: " + str(scoresData.iloc[x, N[0]]) + "\tranked: " + str(int(ranksData.iloc[x, N[0]])) + "\ttruth: " + str(ranksData.iloc[x, -1])
			if result == ranksData.iloc[x, -1]:
				# print "cx",
				accuracy +=1
				# print "i:\t" + str(x) + "\tscore: " + str(scoresData.iloc[x, N[0]]) + "\tprecision: " + str(precision) + "\tRK"
		accuracyList.append((round(accuracy/precision*100, 2)))
	return accuracyList
