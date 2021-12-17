import numpy as np


def array(*args):
    return np.array(args)


class Cardinality2:
    def __init__(self, n1: float, n12: float, n2: float):
        self.size1, self.size12, self.size2 = n1, n12, n2
        self.v1, self.v12, self.v2 = n1 - n12, n12, n2 - n12
        self.total_count = n1 - n12 + n2
        self.p1, self.p12, self.p2 = [v / self.total_count for v in (self.v1, self.v12, self.v2)]

    def values(self):
        return np.array((self.v1, self.v12, self.v2))

    def normalized(self):
        return np.array((self.p1, self.p12, self.p2))

    def scaled(self, multiplier: float):
        return self.__class__(*[v * multiplier for v in (self.v1, self.v12, self.v2)])


class Cardinality3:
    def __init__(self, n1: float, n2: float, n3: float, n12: float, n13: float, n23: float, n123: float):
        self.size1, self.size2, self.size3, self.size12, self.size13, self.size23, self.size123 = n1, n2, n3, n12, n13, n23, n123
        self.v1, self.v2, self.v3 = n1 - n12 - n13 + n123, n2 - n12 - n23 + n123, n3 - n13 - n23 + n123
        self.v12, self.v13, self.v23, self.v123 = n12 - n123, n13 - n123, n23 - n123, n123
        parts = [self.v1, self.v2, self.v3, self.v12, self.v13, self.v23, self.v123]
        self.total_count = sum(parts)
        self.p1, self.p2, self.p3, self.p12, self.p13, self.p23, self.p123 = [v / self.total_count for v in parts]

    def values(self):
        return np.array((self.v1, self.v2, self.v3, self.v12, self.v13, self.v23, self.v123))

    def normalized(self):
        return np.array((self.p1, self.p2, self.p3, self.p12, self.p13, self.p23, self.p123))

    def scaled(self, multiplier: float):
        return self.__class__(*[v * multiplier for v
                                in (self.v1, self.v2, self.v3, self.v12, self.v13, self.v23, self.v123)])


def decompose2(population1, population2) -> Cardinality2:
    intersect = set(population1).intersection(population2)
    return Cardinality2(len(population1), len(intersect), len(population2))


def decompose3(population1, population2, population3) -> Cardinality3:
    intersect12 = set(population1).intersection(population2)
    intersect13 = set(population1).intersection(population3)
    intersect23 = set(population2).intersection(population3)
    intersect123 = intersect12.intersection(intersect13)

    n123 = len(intersect123)
    n12 = len(intersect12)
    n13 = len(intersect13)
    n23 = len(intersect23)
    n1 = len(population1)
    n2 = len(population2)
    n3 = len(population3)

    return Cardinality3(n1, n2, n3, n12, n13, n23, n123)


def rmse(seq1: np.ndarray, seq2: np.ndarray) -> float:
    return np.linalg.norm(seq1 - seq2) / np.sqrt(len(seq1))
