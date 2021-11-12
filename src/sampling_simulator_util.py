import numpy as np


def array(*args):
    return np.array(args)


class Cardinality2:
    def __init__(self, v1: float, v12: float, v2: float):
        self.v1 = v1
        self.v12 = v12
        self.v2 = v2

    def sum(self):
        return self.v1 + self.v12 + self.v2

    def normalize(self):
        return array(self.v1, self.v12, self.v2) / self.sum()


def decompose2(population1, population2) -> Cardinality2:
    intersect = set(population1).intersection(population2)

    n12 = len(intersect)
    n1 = len(population1) - n12
    n2 = len(population2) - n12

    return Cardinality2(n1, n12, n2)
