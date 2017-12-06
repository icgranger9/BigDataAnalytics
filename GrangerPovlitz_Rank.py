import copy
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
			cutoff += scr.score_individual(data, i, N) #why individual and not label?
	return cutoff

def rank_individual(rankData, i, N, cutoff):
	iRank = 0
	for attr in N:
		iRank += rankData.iloc[i, attr]
	#print "iRank, cutoff: " + str(iRank) + ",\t" + str(cutoff);

	numElements = rankData.shape[0] * len(N)
	return int(iRank >= (numElements - cutoff))


def rank_total(scoreData, rankData, N, precisionAt):
	accuracyList = []
	c = determine_c(scoreData, N)

	for precision in precisionAt:
		accuracy = 0.0
		# if debug:
		# 	print "cutoff for precision " + str(precision) + " is " + str(cutoff)
		for x in range(precision):
			result = rank_individual(rankData, x, N, c)
			if result != scr.score_individual(scoreData, x, N):
				pass
				# print "inconsistency at x: " + str(x) + "\tvalue: " + str(scoreData.iloc[x, N[0]]) + "\tranked: " + str(int(rankData.iloc[x, N[0]])) + "\ttruth: " + str(rankData.iloc[x, -1])
			if result == rankData.iloc[x, -1]:
				# print "cx",
				accuracy +=1
				# print "i:\t" + str(x) + "\tscore: " + str(scoreData.iloc[x, N[0]]) + "\tprecision: " + str(precision) + "\tRK"
		
		accuracyList.append((round(accuracy/precision*100, 2)))

	return accuracyList
