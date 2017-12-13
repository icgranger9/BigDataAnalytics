import pandas as pd
import math

# use diversity as defined in Eye Movement paper page 337 part B
def calculateDiversity(data, attrsA, attrsB):
    sum = 0.0
    for i in range(data.shape[0]):
        aSum = 0.0
        bSum = 0.0
        for n in attrsA:
            aSum += data.iloc[i, n]
        for n in attrsB:
            bSum += data.iloc[i, n]
        sum += math.pow(aSum - bSum, 2) / (len(attrsA) + len(attrsB))
    sum = math.sqrt(sum)
    return sum
