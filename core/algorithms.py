from math import sqrt

#Returns a distance-based similarity score for identifierA & identifierB
def similarityEuclidean(items, identifierA, identifierB):
    sharedItems = {}
    #Get list of mutually present items
    for item in items[identifierA]:
        if item in items[identifierB]:
            sharedItems[item] = 1

    if len(sharedItems) == 0:
        return 0

    #Add up the squares of all the differences
    sumOfSquares = sum([pow(items[identifierA][item] - items[identifierB][item], 2)
                        for item in items[identifierA] if item in items[identifierB]])

    return 1 / (1 + sumOfSquares)


#Returns the Pearson correlation coefficient for identifierA & identifierB
def similarityPearson(items, identifierA, identifierB):
    sharedItems = {}
    #Get list of mutually present items
    for item in items[identifierA]:
        if item in items[identifierB]:
            sharedItems[item] = 1

    #Find number of elements
    n = len(sharedItems)

    if n == 0:
        return 0

    #Add up all the items
    sum1 = sum([items[identifierA][item] for item in sharedItems])
    sum2 = sum([items[identifierB][item] for item in sharedItems])

    #Sum up the squares
    sum1Squared = sum([pow(items[identifierA][item], 2) for item in sharedItems])
    sum2Squared = sum([pow(items[identifierB][item], 2) for item in sharedItems])

    #Sum up the products
    sumsProduct = sum([items[identifierA][item] * items[identifierB][item] for item in sharedItems])

    #Calculate Pearson score
    number = sumsProduct - (sum1 * sum2 / n)
    denominator = sqrt((sum1Squared - pow(sum1, 2) / n) * (sum2Squared - pow(sum2, 2) / n))

    if denominator == 0:
        return 0
    r = number / denominator

    return r
