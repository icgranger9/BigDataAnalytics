import pandas as pd
import math

# use diversity as defined in Eye Movement paper page 337 part B
def calculateDiversity(data, attrsA, attrsB):
    sum = 0.0
    for i in range(data.shape[0]):
        aSum = 0.0
        aMax = data.iloc[0, attrsA[0]]
        aMin = aMax
        aTempSum = 0.0

        bSum = 0.0
        bMax = data.iloc[0, attrsB[0]]
        bMin = bMax
        bTempSum = 0.0

        for n in attrsA:
            aTempSum += data.iloc[i, n]
        aSum += aTempSum
        aMax = max(aTempSum, aMax)
        aMin = min(aTempSum, aMax)

        for n in attrsB:
            bTempSum += data.iloc[i, n]
        bSum += bTempSum
        bMax = max(bTempSum, bMax)
        bMin = min(bTempSum, bMin)

        sum += math.pow(aSum - bSum, 2) / (len(attrsA) + len(attrsB))
    sum = math.sqrt(sum)
    maxDifference = max(abs(aMax-bMin), abs(aMax-bMin))

    return [sum, maxDifference]
