import numpy as np
import pandas as pd 
import itertools
import sys
import copy

# Not currently used, but can be added to measure runtime
#import time

# sets up a pandas dataframe with the gaze data, based on command line inputs.
def setup_data():
	# trys to take in the argument (names of gaze data file) from the command line
	try:
		arg1 = sys.argv[1]


		if ("Gaze_DataFile.csv" in arg1):
			gazeData = pd.read_csv(arg1)

			# Translates the label from 'Left' and 'Right' to 1 and 0
				#Note: double check that 1 is left and 0 is right.
			for x in range(gazeData.shape[0]):
				if gazeData.iloc[x, -1]=="Left":
					gazeData.iloc[x, -1] = 1
				else:
					gazeData.iloc[x, -1] = 0

			gazeData = gazeData.iloc[:, 1:]


		else:
			1/0 ##causes an error, if the gaze data is not included


		return(gazeData)

	#ends the program if the data is not input correctly.
	except (ZeroDivisionError, IndexError):
		print "Error with the input file"
		quit()


# returns a dataframe with the rank values for each attribute, instead of the raw attribute value. data is a dataframe with the original data
	# Note: kind of sloppy, try to clean up / make more efficent.
def rank_setup(data):
	rankData = copy.deepcopy(data)

	# for each attribute, subtracts one so we don't include the labels
	for x in range(data.shape[1]-1):
		
		#creates a list with every value in the attribute
		attr_sorted = rankData.iloc[:, x].tolist()
		for val in range(len(attr_sorted)):
			#changest that list to [value, index], for every value
			attr_sorted[val] = [attr_sorted[val], val]

		#sorts the list by the value
		attr_sorted.sort(key=lambda x: x[0])

		#converts from the value to a rank
		for val in range(len(attr_sorted)):
			attr_sorted[val] = [val, attr_sorted[val][1]]

		#resorts by the index
			#note: might not be needed?
		attr_sorted.sort(key=lambda x: x[1])
		
		#maps that rank back onto the dataframe, besed on it's original index.
		for val in range(len(attr_sorted)):
			rankData.iloc[attr_sorted[val][1], x] = int(attr_sorted[val][0])

	return rankData


# returns a list of lists, which includes all possible subsets of the original list. Takes in a list of items, which can be either numbers or strings
def combinations(data):
	combos = []
	for i in range(len(data)+1):
		els = [list(x) for x in itertools.combinations(data, i)]
		combos.extend(els)

	#removes the empty list from our list of lists
	if [] in combos:
		combos.remove([])

	return combos


# finds out how many 1s there are, used for rank classification cutoff
	# Note: may not be needed any more
def determinte_c(data):
    num_ones = 0
    for attr in range(data.shape[0]):
        num_ones += data.iloc[attr, -1]

    return num_ones


#predicts gets the label for a given instance. N is a set of arrtibutes for the desired score, data is everything, i is an int for the instance
def score_individual(data, i,  N):
	runningTotal = 0
	for attr in N:
		runningTotal += data.iloc[i, attr]
		#print str(i) + ": " +str(int(round(runningTotal/len(N),0)))

	return int(round(runningTotal/len(N),0))


#gets the total score accuracy for a given set of attributes N. Precision at is the number of instances that will be used to calculate accuracy.
	#Note: add precision at, where we measure the accuracy at a given number of instances, instead of the total
def score_total(data, N, precisionAt):
	accuracyList = []

	for precision in precisionAt:
		accuracy = 0.0
		for x in range(precision):
			result = score_individual(data, x, N)

			if result == data.iloc[x, -1]:
				accuracy +=1 
			'''else:
				print str(x)+": "+str(accuracy)'''

		accuracyList.append(int(round((accuracy/precision)*100 , 0)))
		#accuracyList.append([accuracy ,int(round((accuracy/precision)*100 , 0))])

	return accuracyList
	

# predicts gets the label for a given instance. data is the ranked data, i is the particular instance, N is the set of attributes, and cutoff is the point at which we determine 1 or 0 
def rank_individual(data, i, N, cutoff):
	rankTotal = 0
	for attr in N:
		rankTotal += data.iloc[i, attr]
	
	#Note: doesn't rank total need to be divided by the number of attributes?
	if rankTotal < cutoff:
		return 0
	else:
		return 1


#gets the total rank inaccuracy for a given set of attributes N
	#Note: calculates the inaccuracy, which is the wrong way to go about it, according to Hsu
	#Note: add precision at, where we measure the accuracy at a given number of instances, instead of the total
def rank_total(data, N, c):
	wrong = 0.0
	for x in range(data.shape[0]):
		result = rank_individual(data, x, N, c)
		if not result == data.iloc[x, -1]:
			wrong +=1 

	#shouldn't hardcode this number. (c*100), But that may be wrong after we redo rank_total.
	return (wrong/36300)


def main():

	#setup variables
	precisionAt = [100,200,300]
	gazeData = setup_data()
	combos = combinations( range(gazeData.shape[1]-1))
	rankData = rank_setup(gazeData) 
	c = determinte_c(rankData)

	#print gazeData
	#print rankData
	#print combos
	#result = score_total(gazeData, [0], precisionAt)

	# runs score and rank total for each combinations, and neatly prints out the result.
	for attrs in combos:
		#pass
		print str(attrs) +": "
		print "\tScore accuracy percentages: " + str(score_total(gazeData, attrs, precisionAt))
		#print "\tRank  accuracy: " + str((1-(rank_total(rankData, attrs, c)))*100)+ "%\n"




if __name__ == '__main__':
	main()
