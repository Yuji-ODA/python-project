import numpy as np


def array(*args):
    return np.array(args)


class Cardinality2:
    def __init__(self, v1: float, v12: float, v2: float):
        self.v1, self.v12, self.v2 = v1, v12, v2
        self.total_count = v1 + v12 + v2
        self.p1, self.p12, self.p2 = [v / self.total_count for v in (v1, v12, v2)]

    def normalize(self):
        return np.array((self.p1, self.p12, self.p2))


class Cardinality3:
    def __init__(self, v1: float, v2: float, v3: float, v12: float, v13: float, v23: float, v123: float):
        args = (v1, v2, v3, v12, v13, v23, v123)
        self.v1, self.v2, self.v3, self.v12, self.v13, self.v23, self.v123 = args
        self.total_count = sum(args)
        self.p1, self.p2, self.p3, self.p12, self.p13, self.p23, self.p123 = [v / self.total_count for v in args]

    def normalize(self):
        return np.array((self.p1, self.p2, self.p3, self.p12, self.p13, self.p23, self.p123))


def decompose2(population1, population2) -> Cardinality2:
    intersect = set(population1).intersection(population2)

    n12 = len(intersect)
    n1 = len(population1) - n12
    n2 = len(population2) - n12

    return Cardinality2(n1, n12, n2)
