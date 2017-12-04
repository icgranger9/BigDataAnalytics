#predicts gets the label for a given instance. N is a set of arrtibutes for the desired score, data is everything, i is an int for the instance
def score_individual(data, i,  N):
	runningTotal = 0.0

	for attr in N:
		runningTotal += data.iloc[i, attr]

	return int(round(runningTotal/len(N), 0))

#gets the total score accuracy for a given set of attributes N. Precision at is the number of instances that will be used to calculate accuracy.
def score_total(data, N, precisionAt):
	accuracyList =[]

	for precision in precisionAt:
		accuracy = 0.0

		for i in range(precision):
			result = score_individual(data, i, N)

			if (result == data.iloc[i, -1]):
				accuracy+=1

		accuracyList.append(round((accuracy/precision)*100, 0))

	return accuracyList