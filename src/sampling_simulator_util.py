from collections import namedtuple

import numpy as np


def array(*args):
    return np.array(args)


Stats2 = namedtuple('Stats', 'v1 v12 v2')


def decompose2(population1, population2):
    intersect = set(population1).intersection(population2)
    union = set(population1).union(population2)

    n_all = len(union)
    n12 = len(intersect)
    p12 = n12 / n_all
    n1 = len(population1) - n12
    n2 = len(population2) - n12
    p1 = n1 / n_all
    p2 = n2 / n_all

    return Stats2(n1, n12, n2), Stats2(p1, p12, p2)
