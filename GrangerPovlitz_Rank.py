import copy
import GrangerPovlitz_Score as scr

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

# finds out how many 1s there are, used for score classification cutoff
# data: score classification data
# precision: integer, such as 100, 200, 300
def determinte_c(data, precision):
    num_ones = 0
    num_ones_new = 0
    # for i in range(data.shape[0]):
    for i in range(precision):
		num_ones += data.iloc[i, -1]
		num_ones_new += scr.score_individual(data, i, [0])
		# print str(score_individual(data, i, [0]))

    # print str(num_ones) +"\n" + str(num_ones_new)
    return num_ones

# predicts gets the label for a given instance. data is the ranked data, i is the particular instance, N is the set of attributes, and cutoff is the point at which we determine 1 or 0 
def rank_individual(data, i, N, cutoff):
	rankTotal = 0
	for attr in N:
		rankTotal += data.iloc[i, attr]
	
	#Note: doesn't rank total need to be divided by the number of attributes?
	if rankTotal <= cutoff:
		return 0
	else:
		return 1

#gets the total rank inaccuracy for a given set of attributes N
	#Note: calculates the inaccuracy, which is the wrong way to go about it, according to Hsu
	#Note: add precision at, where we measure the accuracy at a given number of instances, instead of the total
def rank_total(data, N, c, precisionAt):
	accuracyList = []
	for precision in precisionAt:
		accuracy = 0.0
		for x in range(precision):
			result = rank_individual(data, x, N, c)
			if result == data.iloc[x, -1]:
				accuracy +=1
		accuracyList.append(int(round((accuracy/precision)*100 , 0)))


	return accuracyList


def rank_total_revised(scoresData, ranksData, N, precisionAt):
	accuracyList = []
	for precision in precisionAt:
		accuracy = 0.0
		cutoff = determinte_c(scoresData, precision)
		#print "cutoff for precision " + str(precision) + " is " + str(cutoff)
		for x in range(precision):
			result = rank_individual(ranksData, x, N, cutoff)
			if result == ranksData.iloc[x, -1]:
				accuracy +=1
		accuracyList.append(int(round((accuracy/precision)*100 , 0)))
	return accuracyList