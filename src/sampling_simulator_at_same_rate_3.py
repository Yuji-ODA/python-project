import math
from itertools import chain
from random import sample

import numpy as np
from numpy.linalg import norm

from src.sampling_simulator_util import decompose3, Cardinality3, array


def simulate(population1, population2, population3, n, sampling_rate):

    # 個別サンプリング
    sample1 = set(sample(list(population1), int(n.size1 * sampling_rate)))
    sample2 = set(sample(list(population2), int(n.size2 * sampling_rate)))
    sample3 = set(sample(list(population3), int(n.size3 * sampling_rate)))

    n_actual = decompose3(sample1, sample2, sample3)

    # 理論値の計算
    n_expected = n.scaled(sampling_rate)

    # 個別サンプリングの場合の理論値の計算
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの３乗となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n123_computed = (sampling_rate ** 3) * n.v123

    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの２乗となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = (sampling_rate ** 2) * (n.v12 + n.v123) - n123_computed
    n13_computed = (sampling_rate ** 2) * (n.v13 + n.v123) - n123_computed
    n23_computed = (sampling_rate ** 2) * (n.v23 + n.v123) - n123_computed

    # サンプリングの総数から重複分を引く
    n1_computed = sampling_rate * n.size1 - n12_computed - n13_computed - n123_computed
    n2_computed = sampling_rate * n.size2 - n12_computed - n23_computed - n123_computed
    n3_computed = sampling_rate * n.size3 - n13_computed - n23_computed - n123_computed

    n_computed = Cardinality3(n1_computed, n2_computed, n3_computed, n12_computed, n13_computed, n23_computed,
                              n123_computed)

    # 補正
    # 重複分の取りこぼしを補正
    # n123_corrected = n123_expected = sampling_rate * n.v123
    # n123_actual = n123_computed = (sampling_rate ** 3) * n.v123
    #             = (sampling_rate ** 2) * n123_corrected
    n123_corrected = n_actual.v123 / (sampling_rate ** 2)

    # n12_corrected = n12_expected = sampling_rate * n.v12
    # n12_actual = n12_computed = (sampling_rate ** 2) * (n.v12 + n.v123) - n123_computed
    #            = (sampling_rate ** 2) * (n.v12 + n.v123) - n_actual.v123
    #            = (sampling_rate ** 2) * n.v12 + (sampling_rate ** 2) * n_actual.v123 - n_actual.v123
    #            = (sampling_rate ** 2) * n.v12 + n_actual.v123 / sampling_rate - n_actual.v123
    #            = (sampling_rate ** 2) * n.v12 + n_actual.v123 * (1 - sampling_rate) / sampling_rate
    #            = sampling_rate * n12_corrected + n_actual.v123 * (1 - sampling_rate) / sampling_rate
    # n12_corrected = (n_actual.v12 - n_actual.v123 * (1 - sampling_rate) / sampling_rate) / sampling_rate
    odds = sampling_rate / (1 - sampling_rate)
    n12_corrected, n13_corrected, n23_corrected = \
        (array(n_actual.v12, n_actual.v13, n_actual.v23) - n_actual.v123 / odds) / sampling_rate

    # n1_corrected = n1_expected = sampling_rate * n.v1
    # n.v123 = n123_corrected / sampling_rate
    # n.v12 = n12_corrected / sampling_rate
    # n.v13 = n13_corrected / sampling_rate
    # n_actual.v1 = n1_computed = sampling_rate * n.size1 - n12_computed - n13_computed - n123_computed
    #             = sampling_rate * n.size1 - n_actual.v12 - n_actual.v13 - n_actual.v123
    #             = sampling_rate * (n.v1 + n.v12 + n.v13 + n.v123) - n_actual.v12 - n_actual.v13 - n_actual.v123
    #             = sampling_rate * (n1_corrected + n12_corrected + n13_corrected + n123_corrected) / sampling_rate - n_actual.v12 - n_actual.v13 - n_actual.v123
    #             = n1_corrected + n12_corrected + n13_corrected + n123_corrected - n_actual.v12 - n_actual.v13 - n_actual.v123
    # n1_corrected = n_actual.v1 - (n12_corrected + n13_corrected + n123_corrected - n_actual.v12 - n_actual.v13 - n_actual.v123)
    # n1_corrected = n_actual.v1 - (n12_corrected + n13_corrected + n123_corrected - n_actual.v12 - n_actual.v13 - n_actual.v123)
    # n2_corrected = n_actual.v2 - (n12_corrected + n23_corrected + n123_corrected - n_actual.v12 - n_actual.v23 - n_actual.v123)
    # n3_corrected = n_actual.v3 - (n13_corrected + n23_corrected + n123_corrected - n_actual.v13 - n_actual.v23 - n_actual.v123)

    # n1_corrected = n_actual.v1 - (n12_corrected + n13_corrected - n_actual.v12 - n_actual.v13) - n_actual.v123 * (sampling_rate ** -2 - 1)
    # n1_corrected = n_actual.v1 - (n12_corrected - n_actual.v12) - (n13_corrected - n_actual.v13) - n_actual.v123 * (sampling_rate ** -2 - 1)
    # n1_corrected = n_actual.v1 - ((n_actual.v12 - n_actual.v123 * (1 - sampling_rate) / sampling_rate) / sampling_rate - n_actual.v12) - ((n_actual.v13 - n_actual.v123 * (1 - sampling_rate) / sampling_rate) / sampling_rate - n_actual.v13) - n_actual.v123 * (sampling_rate ** -2 - 1)
    # n1_corrected = n_actual.v1 - (n_actual.v12 / sampling_rate - n_actual.v12) - (n_actual.v13 / sampling_rate - n_actual.v13) - n_actual.v123 * (sampling_rate ** -2 - 1) + 2 * n_actual.v123 * (1 - sampling_rate) / sampling_rate ** 2
    # odds = sampling_rate / (1 - sampling_rate)
    # n1_corrected = n_actual.v1 - (n_actual.v12 + n_actual.v13) / odds - n_actual.v123 * (sampling_rate ** -2 - 1 - 2 * (1 - sampling_rate) / sampling_rate ** 2)

    n1_corrected = n_actual.v1 - (n_actual.v12 + n_actual.v13) / odds + n_actual.v123 / odds ** 2
    n2_corrected = n_actual.v2 - (n_actual.v12 + n_actual.v23) / odds + n_actual.v123 / odds ** 2
    n3_corrected = n_actual.v3 - (n_actual.v13 + n_actual.v23) / odds + n_actual.v123 / odds ** 2

    n_corrected = Cardinality3(n1_corrected, n2_corrected, n3_corrected,
                               n12_corrected, n13_corrected, n23_corrected, n123_corrected)

    # 誤差計算
    probs_expected = n_expected.normalized()
    err_actual = norm(n_actual.normalized() - probs_expected)
    err_computed = norm(n_computed.normalized() - probs_expected)
    err_corrected = norm(n_corrected.normalized() - probs_expected)

    print_result('expected ', n_expected)
    print_result('actual   ', n_actual, err_actual)
    print_result('computed ', n_computed, err_computed)
    print_result('corrected', n_corrected, err_corrected)


def print_result(header, n, err=math.nan):
    print(f'{header}: n1 = {round(n.v1)}, n2 = {round(n.v2)}, n3 = {round(n.v3)}, '
          f'n12 = {round(n.v12)}, n13 = {round(n.v13)}, n23 = {round(n.v23)}, n123 = {round(n.v123)}, '
          f'p1 = {n.p1:.4f}, p2 = {n.p2:.4f}, p3 = {n.p3:.4f}, '
          f'p12 = {n.p12:.4f}, p13 = {n.p13:.4f}, p23 = {n.p23:.4f}, p123 = {n.p123:.4f}, err = {err:.6f}')


if __name__ == '__main__':
    set1 = set(range(100000))
    set2 = set(chain(range(5000), range(80000, 200000)))
    set3 = set(chain(range(30000), range(150000, 250000)))

    n = decompose3(set1, set2, set3)

    print(n.values(), n.normalized())

    for sampling_rate in np.arange(.1, 1, .1):
        print('=======================================================================================================')
        print(f'sampling_rate: {sampling_rate}')
        simulate(set1, set2, set3, n, sampling_rate)
