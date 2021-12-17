import math
from random import sample
from typing import Any, Union, Set

from src.sampling_simulator_util import Cardinality3, decompose3, rmse


def simulate(population1: Set[Any], population2: Set[Any], population3: Set[Any], sampling_rate1: float,
             sampling_rate2: Union[float, None] = None, sampling_rate3: Union[float, None] = None):

    if sampling_rate2 is None:
        sampling_rate2 = sampling_rate1

    if sampling_rate3 is None:
        sampling_rate3 = sampling_rate1

    n = decompose3(population1, population2, population3)

    # 個別サンプリングの結果を取得する
    n_actual = do_sampling(population1, population2, population3, sampling_rate1, sampling_rate2, sampling_rate3)

    # 個別サンプリングの場合の理論値の計算
    n_estimated = do_estimation(sampling_rate1, sampling_rate2, sampling_rate3, n)

    # 補正計算
    n_corrected = do_correction(n_actual, sampling_rate1, sampling_rate2, sampling_rate3)

    # 誤差計算
    probabilities_expected = n.normalized()
    err_actual = rmse(n_actual.normalized(), probabilities_expected)

    err_computed = rmse(n_estimated.normalized(), probabilities_expected)
    err_corrected = rmse(n_corrected.normalized(), probabilities_expected)

    print_result('expected ', n)
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
    n123_estimated = sampling_rate1 * sampling_rate2 * sampling_rate3 * n.size123

    n12_estimated = sampling_rate1 * sampling_rate2 * n.size12
    n13_estimated = sampling_rate1 * sampling_rate3 * n.size13
    n23_estimated = sampling_rate2 * sampling_rate3 * n.size23

    n1_estimated = sampling_rate1 * n.size1
    n2_estimated = sampling_rate2 * n.size2
    n3_estimated = sampling_rate3 * n.size3

    return Cardinality3(n1_estimated, n2_estimated, n3_estimated,
                        n12_estimated, n13_estimated, n23_estimated, n123_estimated)


# 補正計算
def do_correction(n_actual: Cardinality3, sampling_rate1: float, sampling_rate2: float,
                  sampling_rate3: float) -> Cardinality3:

    r1 = 1 / sampling_rate1
    r2 = 1 / sampling_rate2
    r3 = 1 / sampling_rate3

    n123_corrected = r1 * r2 * r3 * n_actual.size123

    n12_corrected = r1 * r2 * n_actual.size12
    n13_corrected = r1 * r3 * n_actual.size13
    n23_corrected = r2 * r3 * n_actual.size23

    n1_corrected = r1 * n_actual.size1
    n2_corrected = r2 * n_actual.size2
    n3_corrected = r3 * n_actual.size3

    return Cardinality3(n1_corrected, n2_corrected, n3_corrected,
                        n12_corrected, n13_corrected, n23_corrected, n123_corrected)
