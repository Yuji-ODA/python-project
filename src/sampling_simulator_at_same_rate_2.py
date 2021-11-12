import math
from random import sample

import numpy as np
from numpy.linalg import norm

from src.sampling_simulator_util import array, decompose2, Cardinality2


def simulate(population1, population2, n, sampling_rate):

    # 個別サンプリング
    sample1 = set(sample(list(population1), int(n.size1 * sampling_rate)))
    sample2 = set(sample(list(population2), int(n.size2 * sampling_rate)))

    n_actual = decompose2(sample1, sample2)

    # 理論値の計算
    n_expected = n.scaled(sampling_rate)

    # 個別サンプリングの場合の理論値の計算
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの二乗となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = (sampling_rate ** 2) * n.v12
    # サンプリングの総数から重複分を引く
    n1_computed, n2_computed = array(n.size1, n.size2) * sampling_rate - n12_computed
    n_computed = Cardinality2(n1_computed, n12_computed, n2_computed)

    # 補正
    # 重複分の取りこぼしを補正
    n12_corrected = n_actual.v12 / sampling_rate
    # 重複分を増やした分だけ減らす
    # n_computed.v12 = n_actual.v12 = (sampling_rate ** 2) * n.v12
    # n_corrected.v1 = n_expected.v1 = n.v1 * sampling_rate
    # n_computed.v1 = n_actual.v1 = n.size1 * sampling_rate - n_actual.v12
    #             = (n.v1 + n.v12) * sampling_rate - n_actual.v12
    #             = (n1_corrected / sampling_rate + n_actual.v12 / (sampling_rate ** 2)) * sampling_rate - n_actual.v12
    #             = n1_corrected + n_actual.v12 / sampling_rate - n_actual.v12
    #             = n1_corrected + n_actual.v12 * (1 - sampling_rate) / sampling_rate
    odds = sampling_rate / (1 - sampling_rate)
    n1_corrected, n2_corrected = array(n_computed.v1, n_computed.v2) - n_actual.v12 / odds

    n_corrected = Cardinality2(n1_corrected, n12_corrected, n2_corrected)

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
    print(f'{header}: n1 = {round(n.v1)}, n12 = {round(n.v12)}, n2 = {round(n.v2)}, '
          f'p1 = {n.p1:.4f}, p12 = {n.p12:.4f}, p2 = {n.p2:.4f}, err = {err:.6f}')


if __name__ == '__main__':
    set1 = set(range(100000))
    set2 = set(range(50000, 200000))

    n = decompose2(set1, set2)

    for sampling_rate in np.arange(.1, 1, .1):
        print('=======================================================================================================')
        print(f'sampling_rate: {sampling_rate}')
        simulate(set1, set2, n, sampling_rate)
