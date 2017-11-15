import numpy as np
import pandas as pd 
import itertools
import sys
import time
import copy

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


############################################
def rank_setup(data):
	rankData = copy.deepcopy(data)

	for x in range(data.shape[1]-1):
		
		attr_sorted = rankData.iloc[:, x].tolist()
		for val in range(len(attr_sorted)):
			attr_sorted[val] = [attr_sorted[val], val]

		attr_sorted.sort(key=lambda x: x[0])

		for val in range(len(attr_sorted)):
			attr_sorted[val] = [val, attr_sorted[val][1]]

		attr_sorted.sort(key=lambda x: x[1])
		

		for val in range(len(attr_sorted)):
			rankData.iloc[attr_sorted[val][1], x] = int(attr_sorted[val][0])
			#print "\t["+str(attr_sorted[val][1])+ "," + str(x)+ "]: " + str(attr_sorted[val][0])+ "\t"+ str(rankData.iloc[attr_sorted[val][1], x])


	#print rankData
	return rankData



#get the score for a given instance. N is a set of arrtibutes for the desired score, data is everything, i is an int for the instance
def score_individual(data, i,  N):
	runningTotal = 0
	for attr in N:
		runningTotal += data.iloc[i, attr]

	return int(round(runningTotal/len(N),0))

###################################
# grade individual given ith index and M attributes based on rank
def rank_individual(data, i, N, cutoff):
	rankTotal = 0
	for attr in N:
		rankTotal += data.iloc[i, attr]
	#print rankTotal
	if rankTotal < cutoff:
		return 0
	else:
		return 1

# find out how many 1s there are, used for rank classification cutoff
def determinte_c(data):
    num_ones = 0
    for attr in range(data.shape[0]):
        num_ones += data.iloc[attr, -1]

    return num_ones



#gets the total score inaccuracy for a given set of attributes N
def score_total(data, N):
	wrong = 0.0
	for x in range(data.shape[0]):
		result = score_individual(data, x, N)

		if not result == data.iloc[x, -1]:
			wrong +=1 

	return (wrong/data.shape[0])
	

#########################
#gets the total rank inaccuracy for a given set of attributes N
def rank_total(data, N, c):
	wrong = 0.0
	for x in range(data.shape[0]):
		result = rank_individual(data, x, N, c)
		if not result == data.iloc[x, -1]:
			wrong +=1 

	return (wrong/36300)

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
	rankData = rank_setup(gazeData) 
	c = determinte_c(rankData)

	#print gazeData
	#print rankData
	#print combos

	for attrs in combos:
					print str(attrs) +": "
					print "\tScore accuracy: " + str(int(score_total(gazeData, attrs)*100))+"%"
					print "\tRank  accuracy: " + str((1-(rank_total(rankData, attrs, c)))*100)+ "%\n"




if __name__ == '__main__':
	main()
