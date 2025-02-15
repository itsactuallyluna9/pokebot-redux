#functions to iterate over, evaluate, and generate output from specific models

import random


def randomIndexes(n_indexes, max_value, min_value=1):
    indexes = []
    for i in range(n_indexes):
        indexes.append(random.choice([j for j in range(min_value, max_value)]))
    return indexes


indexes = sorted(randomIndexes(n_indexes=20, max_value=500))
