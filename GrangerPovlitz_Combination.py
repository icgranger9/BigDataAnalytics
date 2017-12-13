import pandas as pd
import copy

def combine(data, attrs):
	#create a list, to store and sort the combination
	tmpList = []

	data = data.sort_index(axis=0)

	#finds the combination for each D sub i
	for i in range(data.shape[0]):
		average = 0.0

		for N in attrs:
			average += data.iloc[i, N]
		average = average/len(attrs) # do not explicitly need to divide, beacuse it is a comparison

		
		tmpList.append(average)

	data = data.assign(f=tmpList).sort_values('f', ascending=False, kind='mergesort').drop('f',axis=1)

	return data


def accList(data, precisionAt):
	truthList =data.iloc[:, -1].tolist()

	result = []

	for precision in precisionAt:
		accuracy = 0.0
		for i in range(precision):
			accuracy+=truthList[i]

		result.append(round((accuracy/precision)*100,1))

	return result

def accuracy(data, attrs, precisionAt):
	dataCP = copy.deepcopy(data)
	dataSet = combine(dataCP, attrs)
	result = accList(dataSet, precisionAt)

	return result
