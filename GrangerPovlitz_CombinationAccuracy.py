import pandas as pd
import itertools
import sys
from scipy import stats

#our functions from other files
import GrangerPovlitz_Score as scr
import GrangerPovlitz_Rank as rnk


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

def main():

	#setup variables
	precisionAt = [100,200,300]
	gazeData = setup_data()
	combos = combinations( range(gazeData.shape[1]-1))
	rankData = rnk.rank_setup()
	# print "col me on ur cl ph:"
	# print gazeData.iloc[:,0].shape[1]
    #
	# return 0
	'''singlecombos = [0,1,2,3,4]
				for attr1 in singlecombos:
					for attr2 in singlecombos:
						print "Diversity between " + str(attr1) + " and " + str(attr2) + " is " + str(stats.ks_2samp(gazeData.iloc[:,attr1].values, gazeData.iloc[:,attr2].values)[0])
					print ""
				print ""'''
	# runs score and rank total for each combinations, and neatly prints out the result.
	for attrs in combos:
		print map(lambda x: chr(x+65), attrs)
		print "\tScore accuracy percentages: " + str(scr.score_total(gazeData, attrs, precisionAt))
		print "\tRank  accuracy percentages: " + str(rnk.rank_total(gazeData, rankData, attrs, precisionAt))
		print 


if __name__ == '__main__':
	main()
