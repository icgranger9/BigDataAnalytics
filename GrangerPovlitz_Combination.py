import pandas as pd

def combine(data, attrs):
	#create new dataframe, and give it the truth vals
	#print data.iloc[:, -1].tolist()
	result = pd.DataFrame(data={"Comb":range(0-(data.shape[0]), 0), "Rating":data.iloc[:, -1].tolist()})


	#create a list, to store and sort the combination
	tmpList = []

	#finds the combination for each D sub i
	for i in range(data.shape[0]):
		average = 0.0

		for N in attrs:
			average += data.iloc[i, N]
		average = average/len(attrs) # do not explicitly need to divide
		, beacuse it is a comparison

		
		tmpList.append([i, average])


	#uses that combination to retermine a rank
	tmpList.sort(key=lambda x: x[1])
	for i in range(len(tmpList)):
		tmpList[i][1] = i
	tmpList.sort(key=lambda x: x[0])

	#adds that rank to the result dataframe
	for i in range(result.shape[0]):
		result.iloc[i, 0] = tmpList[i][1]

	#just return dataframe with cols: rank, truth
	print result
	return result


def accList(data, precisionAt):
	data = data.sort_values("Comb", ascending=False, kind='mergesort')
	#print data

	truthList =data.iloc[:, -1].tolist()

	result = []

	for precision in precisionAt:
		accuracy = 0.0
		for i in range(precision):
			accuracy+=truthList[i]

		result.append([accuracy, precision])

	return result

def accuracy(data, attrs, precisionAt):
	dataSet = combine(data, attrs)
	result = accList(dataSet, precisionAt)

	return result
