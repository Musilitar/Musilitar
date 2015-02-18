from math import sqrt


# ---
# Module for Machine Learning algorithms
# ---


# Copyright:
# SEGARAN (T.)
# Programming Collective Intelligence
# Sebastopol
# O’Reilly Media, Inc.
# 2007
# pp. 11-13


# Returns a distance-based similarity score for identifier_a & identifier_b
def similarity_euclidean(items, identifier_a, identifier_b):
    shared_items = {}
    # Get list of mutually present items
    for item in items[identifier_a]:
        if item in items[identifier_b]:
            shared_items[item] = 1

    if len(shared_items) == 0:
        return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(items[identifier_a][item] - items[identifier_b][item], 2)
                          for item in items[identifier_a] if item in items[identifier_b]])

    return 1 / (1 + sum_of_squares)


# Returns the Pearson correlation coefficient for identifier_a & identifier_b
def similarity_pearson(items, identifier_a, identifier_b):
    shared_items = {}
    # Get list of mutually present items
    for item in items[identifier_a]:
        if item in items[identifier_b]:
            shared_items[item] = 1

    # Find number of elements
    n = len(shared_items)

    if n == 0:
        return 0

    # Add up all the items
    sum1 = sum([items[identifier_a][item] for item in shared_items])
    sum2 = sum([items[identifier_b][item] for item in shared_items])

    # Sum up the squares
    sum1_squared = sum([pow(items[identifier_a][item], 2) for item in shared_items])
    sum2_squared = sum([pow(items[identifier_b][item], 2) for item in shared_items])

    # Sum up the products
    sums_product = sum([items[identifier_a][item] * items[identifier_b][item] for item in shared_items])

    # Calculate Pearson score
    number = sums_product - (sum1 * sum2 / n)
    denominator = sqrt((sum1_squared - pow(sum1, 2) / n) * (sum2_squared - pow(sum2, 2) / n))

    if denominator == 0:
        return 0
    r = number / denominator

    return r
