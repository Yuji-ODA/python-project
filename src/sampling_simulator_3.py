import math
from itertools import chain, product
from random import sample
from typing import Any, Union, Set

import numpy as np
from numpy.linalg import norm

from src.sampling_simulator_util import Cardinality3, decompose3


def simulate(population1: Set[Any], population2: Set[Any], population3: Set[Any], n: Cardinality3,
             sampling_rate1: float, sampling_rate2: Union[float, None] = None, sampling_rate3: Union[float, None] = None):

    if sampling_rate2 is None:
        sampling_rate2 = sampling_rate3 = sampling_rate1

    # 理論値の計算
    # 抽出率が違う場合は考えられないので、ここでは最小の値である場合を想定する
    n_expected = n.scaled(min(sampling_rate1, sampling_rate2, sampling_rate3))

    # 個別サンプリングの場合の理論値の計算
    n_estimated = do_estimation(sampling_rate1, sampling_rate2, sampling_rate3, n)

    # 個別サンプリングの結果を取得する
    n_actual = do_sampling(population1, population2, population3, sampling_rate1, sampling_rate2, sampling_rate3)

    # 補正計算
    n_corrected = do_correction(n_actual, sampling_rate1, sampling_rate2, sampling_rate3)

    # 誤差計算
    probabilities_expected = n_expected.normalized()
    err_actual = norm(n_actual.normalized() - probabilities_expected)

    err_computed = norm(n_estimated.normalized() - probabilities_expected)
    err_corrected = norm(n_corrected.normalized() - probabilities_expected)

    print_result('expected ', n_expected)
    print_result('actual   ', n_actual, err_actual)
    print_result('estimated', n_estimated, err_computed)
    print_result('corrected', n_corrected, err_corrected)


def print_result(header: str, n: Cardinality3, err: float = math.nan):
    print(f'{header}: n1 = {round(n.v1)}, n2 = {round(n.v2)}, n3 = {round(n.v3)}, n12 = {round(n.v12)}, '
          f'n13 = {round(n.v13)}, n23 = {round(n.v23)}, n123 = {round(n.v123)}, '
          f'p1 = {n.p1:.4f}, p2 = {n.p2:.4f}, p3 = {n.p3:.4f}, '
          f'p12 = {n.p12:.4f}, p13 = {n.p13:.4f}, p23 = {n.p23:.4f}, p123 = {n.p123:.4f}, err = {err:.6f}')


# 個別サンプリング
def do_sampling(population1: Set[Any], population2: Set[Any], population3: Set[Any],
                sampling_rate1: float, sampling_rate2: float, sampling_rate3: float) -> Cardinality3:
    sample1 = set(sample(list(population1), int(len(population1) * sampling_rate1)))
    sample2 = set(sample(list(population2), int(len(population2) * sampling_rate2)))
    sample3 = set(sample(list(population3), int(len(population3) * sampling_rate3)))

    return decompose3(sample1, sample2, sample3)


# 個別サンプリングの場合の理論値の計算
def do_estimation(sampling_rate1: float, sampling_rate2: float, sampling_rate3: float, n: Cardinality3) -> Cardinality3:
    # 個別サンプリングの場合の理論値の計算
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの積となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n123_estimated = sampling_rate1 * sampling_rate2 * sampling_rate3 * n.v123

    # サンプリングの総数から重複分を引く
    n12_estimated = sampling_rate1 * sampling_rate2 * (n.v12 + n.v123) - n123_estimated
    n13_estimated = sampling_rate1 * sampling_rate3 * (n.v13 + n.v123) - n123_estimated
    n23_estimated = sampling_rate2 * sampling_rate3 * (n.v23 + n.v123) - n123_estimated

    n1_estimated = sampling_rate1 * (n.v1 + n.v12 + n.v13 + n.v123) - n12_estimated - n13_estimated - n123_estimated
    n2_estimated = sampling_rate2 * (n.v2 + n.v12 + n.v23 + n.v123) - n12_estimated - n23_estimated - n123_estimated
    n3_estimated = sampling_rate3 * (n.v3 + n.v13 + n.v23 + n.v123) - n13_estimated - n23_estimated - n123_estimated

    return Cardinality3(n1_estimated, n2_estimated, n3_estimated,
                        n12_estimated, n13_estimated, n23_estimated, n123_estimated)


# 補正計算
def do_correction(n_actual: Cardinality3, sampling_rate1: float, sampling_rate2: float,
                  sampling_rate3: float) -> Cardinality3:

    sampling_rate_min, sampling_rate_mid, sampling_rate_max = sorted((sampling_rate1, sampling_rate2, sampling_rate3))

    # 補正
    # 重複分の取りこぼしを補正
    # 抽出率は低いほうに合わせてサイズを落とし想定に合わせる
    # n_actual.v123 = n123_computed = sampling_rate_min * sampling_rate_mid * sampling_rate_max * n.v123
    # n123_corrected = n123_expected = sampling_rate_min * n.v123
    #                = n_actual.v123 / (sampling_rate_mid * sampling_rate_max)
    n123_corrected = n_actual.v123 / (sampling_rate_mid * sampling_rate_max)

    odds1 = sampling_rate1 / (1 - sampling_rate1)
    odds2 = sampling_rate2 / (1 - sampling_rate2)
    odds3 = sampling_rate3 / (1 - sampling_rate3)

    # 各サンプルサイズをスケーリングしたのちに重複分を増やした分だけ引く
    # n12_corrected = n_expected.v12 = sampling_rate_min * n.v12
    # n_actual.v12 = n_estimated.v12 = sampling_rate1 * sampling_rate2 * (n.v12 + n.v123) - n_estimated.v123
    #              = sampling_rate1 * sampling_rate2 * (n.v12 + n.v123) - n_actual.v123
    #              = sampling_rate1 * sampling_rate2 * n.v12 + sampling_rate1 * sampling_rate2 * n.v123 - n_actual.v123
    #              = sampling_rate1 * sampling_rate2 * n.v12 + n_actual.v123 / sampling_rate3 - n_actual.v123
    #              = sampling_rate1 * sampling_rate2 * n.v12 + n_actual.v123 * (1 - sampling_rate3) / sampling_rate3
    #              = sampling_rate1 * sampling_rate2 / sampling_rate_min * n12_corrected +
    #                n_actual.v123 * (1 - sampling_rate3) / sampling_rate3
    # よって
    # n12_corrected = (n_actual.v12 - n_actual.v123 * (1 - sampling_rate3) / sampling_rate3)
    #                / (sampling_rate1 * sampling_rate2 / sampling_rate_min)
    r12 = sampling_rate_min / (sampling_rate1 * sampling_rate2)
    r13 = sampling_rate_min / (sampling_rate1 * sampling_rate3)
    r23 = sampling_rate_min / (sampling_rate2 * sampling_rate3)

    n12_corrected = r12 * (n_actual.v12 - n_actual.v123 / odds3)
    n13_corrected = r13 * (n_actual.v13 - n_actual.v123 / odds2)
    n23_corrected = r23 * (n_actual.v23 - n_actual.v123 / odds1)

    # n1_corrected = n_expected.v1 = sampling_rate_min * n.v1
    # n.v123 = n123_corrected / sampling_rate_min
    # n.v12 = n12_corrected / sampling_rate_min
    # n.v13 = n13_corrected / sampling_rate_min
    # n_actual.v1 = n_estimated.v1 = sampling_rate1 * n.size1 - n12_estimated - n13_estimated - n123_estimated
    #             = sampling_rate1 * n.size1 - n_actual.v12 - n_actual.v13 - n_actual.v123
    #             = sampling_rate1 * (n.v1 + n.v12 + n.v13 + n.v123) - n_actual.v12 - n_actual.v13 - n_actual.v123
    #             = sampling_rate1 / sampling_rate_min * (n1_corrected + n12_corrected + n13_corrected + n123_corrected)
    #              - n_actual.v12 - n_actual.v13 - n_actual.v123
    # よって
    # n1_corrected = sampling_rate_min / sampling_rate1 * (n_actual.v1 + n_actual.v12 + n_actual.v13 + n_actual.v123)
    #               - (n12_corrected + n13_corrected + n123_corrected)
    # v12について
    # kv12 = (sampling_rate_min / sampling_rate1 -
    #        1 / sampling_rate_min / (sampling_rate1 * sampling_rate2)) * n_actual.v12
    #      = (sampling_rate_min / sampling_rate1 - sampling_rate_min / sampling_rate1 / sampling_rate2) * n_actual.v12
    #      = sampling_rate_min / sampling_rate1 * (1 - 1 / sampling_rate2) * n_actual.v12
    #       - sampling_rate_min / sampling_rate1 * n_actual.v12 / odds2
    #
    # v13についても同様
    #
    # v123について
    # kv123 = sampling_rate_min / sampling_rate1 +
    #         sampling_rate_min / odds3 / (sampling_rate1 * sampling_rate2) +
    #         sampling_rate_min / odds2 / (sampling_rate1 * sampling_rate3) -
    #         1 / (sampling_rate_mid * sampling_rate_max)
    #       = sampling_rate_min / sampling_rate1 +
    #         sampling_rate_min / sampling_rate1 * (1 / (odds3 * sampling_rate2) + 1 / (odds2 * sampling_rate3)) -
    #         1 / (sampling_rate_mid * sampling_rate_max)
    #       = sampling_rate_min / sampling_rate1 * (1 + 1 / (odds3 * sampling_rate2) + 1 / (odds2 * sampling_rate3)) -
    #         1 / (sampling_rate_mid * sampling_rate_max)
    #       = sampling_rate_min / sampling_rate1 *
    #         (1 + 1 / (odds3 * sampling_rate2) + 1 / (odds2 * sampling_rate3) -
    #         sampling_rate1 / (sampling_rate_min * sampling_rate_mid * sampling_rate_max))
    #       = sampling_rate_min / sampling_rate1 *
    #         (1 + 1 / (odds3 * sampling_rate2) + 1 / (odds2 * sampling_rate3) -
    #         sampling_rate1 / (sampling_rate1 * sampling_rate2 * sampling_rate3))
    #       = sampling_rate_min / sampling_rate1 *
    #         (1 + 1 / (odds3 * sampling_rate2) + 1 / (odds2 * sampling_rate3) -
    #         1 / (sampling_rate2 * sampling_rate3))
    #       = sampling_rate_min / sampling_rate1 * \
    #         (1 + 1 / (sampling_rate3 / (1 - sampling_rate3) * sampling_rate2) +
    #         1 / (sampling_rate2 / (1 - sampling_rate2) * sampling_rate3) -
    #         1 / (sampling_rate2 * sampling_rate3))
    #       = sampling_rate_min / sampling_rate1 * \
    #         (1 + (1 - sampling_rate3) / (sampling_rate3 * sampling_rate2) +
    #         (1 - sampling_rate2) / (sampling_rate2 * sampling_rate3) -
    #         1 / (sampling_rate2 * sampling_rate3))
    #       = sampling_rate_min / sampling_rate1 *
    #         (1 + (1 - sampling_rate2 - sampling_rate3) / (sampling_rate3 * sampling_rate2))
    #       = sampling_rate_min / sampling_rate1 *
    #         (1 + 1 / (sampling_rate3 * sampling_rate2) - 1 / sampling_rate2 - 1 / sampling_rate3)
    #       = sampling_rate_min / sampling_rate1 *
    #         (1 - 1 / sampling_rate2 - 1 / sampling_rate3 * (1 - 1 / sampling_rate2))
    #       = sampling_rate_min / sampling_rate1 * (-1 / odds21 + 1 / sampling_rate3 * 1 / odds2)
    #       = sampling_rate_min / sampling_rate1 * (1 / odds2) * (1 - 1 / sampling_rate3))
    #       = sampling_rate_min / sampling_rate1 * (1 / odds2) * (1 / odds3)

    r1 = sampling_rate_min / sampling_rate1
    r2 = sampling_rate_min / sampling_rate2
    r3 = sampling_rate_min / sampling_rate3

    n1_corrected = r1 * (n_actual.v1 - (n_actual.v12 / odds2 + n_actual.v13 / odds3) + n_actual.v123 / odds2 / odds3)
    n2_corrected = r2 * (n_actual.v2 - (n_actual.v12 / odds1 + n_actual.v23 / odds3) + n_actual.v123 / odds1 / odds3)
    n3_corrected = r3 * (n_actual.v3 - (n_actual.v13 / odds1 + n_actual.v23 / odds2) + n_actual.v123 / odds1 / odds2)

    return Cardinality3(n1_corrected, n2_corrected, n3_corrected,
                        n12_corrected, n13_corrected, n23_corrected, n123_corrected)


if __name__ == '__main__':
    set1 = set(range(100000))
    set2 = set(chain(range(5000), range(80000, 200000)))
    set3 = set(chain(range(30000), range(150000, 250000)))

    n = decompose3(set1, set2, set3)

    for sampling_rate1, sampling_rate2, sampling_rate3 \
            in product(np.arange(.1, 1, .4), np.arange(.1, 1, .4), np.arange(.1, 1, .4)):
        print('=======================================================================================================')
        print(f'sampling_rate1: {sampling_rate1}, sampling_rate2: {sampling_rate2}, sampling_rate1: {sampling_rate3}')
        simulate(set1, set2, set3, n, sampling_rate1, sampling_rate2, sampling_rate3)
