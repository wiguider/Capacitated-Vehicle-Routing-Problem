import math


def euclidean_distance(vector1, vector2):
    return float(math.sqrt(sum([(float(v2) - float(v1)) ** 2 for v1, v2 in zip(vector1, vector2)])))





