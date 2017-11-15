import numpy as np
import pandas as pd 
import itertools
import sys
import time
import copy

#input : none
#output: a pandas dataFrame, which is the test data
def setup_data():
	#trys to take in the arguments (names of train and test files) from the command line
	try:
		arg1 = sys.argv[1]


		if ("Gaze_DataFile.csv" in arg1):
			gazeData = pd.read_csv(arg1)

			for x in range(gazeData.shape[0]):
				if gazeData.iloc[x, -1]=="Left":
					gazeData.iloc[x, -1] = 0		#Uncertain, double check
				else:
					gazeData.iloc[x, -1] = 1

			gazeData = gazeData.iloc[:, 1:]


		else:
			1/0 ##causes an error, if the train and test data is not included


		return(gazeData)

	#ends the program if the data is not input correctly.
	except (ZeroDivisionError, IndexError):
		print "Error with the input files"
		quit()

#get the score for a given instance. N is a set of arrtibutes for the desired score, data is everything, i is an int for the instance
def score_individual(data, i,  N):
	runningTotal = 0
	for attr in N:
		runningTotal += data.iloc[i, attr]

	return int(round(runningTotal/len(N),0))



#gets the total score inaccuracy for a given set of attributes N
def score_total(data, N):
	wrong = 0.0
	for x in range(data.shape[0]):
		result = score_individual(data, x, N)

		if not result == data.iloc[x, -1]:
			wrong +=1 

	return (wrong/data.shape[0])
	

# num is an int for nuber of attributes
def combinations(data):
	combos = []
	for i in range(len(data)+1):
		els = [list(x) for x in itertools.combinations(data, i)]
		combos.extend(els)

	if [] in combos:
		combos.remove([])

	return combos


def main():
	gazeData = setup_data()
	combos = []
	combos = combinations( range(gazeData.shape[1]-1))
	
	#print gazeData
	#print combos

	for attrs in combos:
		print str(attrs) +": "
		print "\tScore accuracy: " + str(int(score_total(gazeData, attrs)*100))+"%"
		print "\tRank  accuracy: " + "" + "%\n"




if __name__ == '__main__':
	main()
