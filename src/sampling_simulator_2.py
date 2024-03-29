import math
from random import sample
from typing import Any, Union, Set

from src.sampling_simulator_util import decompose2, Cardinality2, rmse


def simulate(population1: Set[Any], population2: Set[Any],
             sampling_rate1: float, sampling_rate2: Union[float, None] = None):

    if sampling_rate2 is None:
        sampling_rate2 = sampling_rate1

    n = decompose2(population1, population2)

    # 個別サンプリングの結果を取得する
    n_actual = do_sampling(population1, population2, sampling_rate1, sampling_rate2)

    # 個別サンプリングの場合の理論値の計算
    n_estimated = do_estimation(sampling_rate1, sampling_rate2, n)

    # 補正計算
    n_corrected = do_correction(n_actual, sampling_rate1, sampling_rate2)

    # 誤差計算
    probabilities_expected = n.normalized()
    err_actual = rmse(n_actual.normalized(), probabilities_expected)

    err_computed = rmse(n_estimated.normalized(), probabilities_expected)
    err_corrected = rmse(n_corrected.normalized(), probabilities_expected)

    print_result('expected ', n)
    print_result('actual   ', n_actual, err_actual)
    print_result('estimated', n_estimated, err_computed)
    print_result('corrected', n_corrected, err_corrected)


def print_result(header: str, n: Cardinality2, err: float = math.nan):
    print(f'{header}: n1 = {round(n.v1)}, n12 = {round(n.v12)}, n2 = {round(n.v2)}, '
          f'p1 = {n.p1:.4f}, p12 = {n.p12:.4f}, p2 = {n.p2:.4f}, err = {err:.6f}')


# 個別サンプリング
def do_sampling(population1: Set[Any], population2: Set[Any],
                sampling_rate1: float, sampling_rate2: float) -> Cardinality2:
    sample1 = set(sample(list(population1), int(len(population1) * sampling_rate1)))
    sample2 = set(sample(list(population2), int(len(population2) * sampling_rate2)))

    return decompose2(sample1, sample2)


# 個別サンプリングの場合の理論値の計算
def do_estimation(sampling_rate1: float, sampling_rate2: float, n: Cardinality2) -> Cardinality2:
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの積となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_estimated = sampling_rate1 * sampling_rate2 * n.size12

    # サンプリングの総数から重複分を引く
    # n1_estimated = sampling_rate1 * (n.v1 + n.v12) - n12_estimated
    # n1_estimated = sampling_rate1 * (n.v1 + (1 - sampling_rate2) * n.v12)
    # n2_estimated = sampling_rate2 * (n.v12 + n.v2) - n12_estimated
    # n2_estimated = sampling_rate2 * (n.v2 + (1 - sampling_rate1) * n.v12)
    n1_estimated = sampling_rate1 * n.size1
    n2_estimated = sampling_rate2 * n.size2

    return Cardinality2(n1_estimated, n12_estimated, n2_estimated)


# 補正計算
def do_correction(n_actual: Cardinality2, sampling_rate1: float, sampling_rate2: float) -> Cardinality2:

    r1 = 1 / sampling_rate1
    r2 = 1 / sampling_rate2

    # 重複分の取りこぼしを補正
    # n_estimated.v12 = n_actual.v12 = sampling_rate1 * sampling_rate2 * n.v12
    # n12_corrected = n.v12
    #               = n_actual.v12 / (sampling_rate1 * sampling_rate2)
    # n12_corrected = r1 * r2 * n_actual.v12
    n12_corrected = r1 * r2 * n_actual.size12

    # 各サンプルサイズをスケーリングしたのちに重複分を増やした分だけ引く
    # n1_corrected = n.v1
    # n_estimated.v1 = n_actual.v1 = sampling_rate1 * (n.v1 + n.v12) - n_estimated.v12
    #                = sampling_rate1 * (n1_corrected + n_actual.v12 / (sampling_rate1 * sampling_rate2)) - n_actual.v12
    #                = sampling_rate1 * n1_corrected + n_actual.v12 / sampling_rate2 - n_actual.v12
    # n1_corrected = r1 * (n_actual.v1 - (r2 - 1) * n_actual.v12)
    # n2_corrected = r2 * (n_actual.v2 - (r1 - 1) * n_actual.v12)
    n1_corrected = r1 * n_actual.size1
    n2_corrected = r2 * n_actual.size2

    return Cardinality2(n1_corrected, n12_corrected, n2_corrected)
