import math
from random import sample
from typing import Any, Union, Set

from numpy.linalg import norm

from src.sampling_simulator_util import array, decompose2, Cardinality2


def simulate(population1: Set[Any], population2: Set[Any], n: Cardinality2,
             sampling_rate1: float, sampling_rate2: Union[float, None] = None):

    if sampling_rate2 is None:
        sampling_rate2 = sampling_rate1

    # 理論値の計算
    # 抽出率が違う場合は考えられないので、ここでは小さい方の値である場合を想定する
    n1_expected, n12_expected, n2_expected = min(sampling_rate1, sampling_rate2) * array(n.v1, n.v12, n.v2)
    n_expected = Cardinality2(n1_expected, n12_expected, n2_expected)

    # 個別サンプリングの場合の理論値の計算
    n_computed = do_estimation(sampling_rate1, sampling_rate2, n)

    # 個別サンプリングの結果を取得する
    n_actual = do_sampling(population1, population2, sampling_rate1, sampling_rate2)

    # 補正計算
    n_corrected = do_correction(n_actual, sampling_rate1, sampling_rate2)

    # 誤差計算
    probabilities_expected = n_expected.normalized()
    err_actual = norm(n_actual.normalized() - probabilities_expected)

    err_computed = norm(n_computed.normalized() - probabilities_expected)
    err_corrected = norm(n_corrected.normalized() - probabilities_expected)

    print_result('expected ', n_expected)
    print_result('actual   ', n_actual, err_actual)
    print_result('computed ', n_computed, err_computed)
    print_result('corrected', n_corrected, err_corrected)


def print_result(header: str, n: Cardinality2, err: float = math.nan):
    print(f'{header}: n1 = {round(n.v1)}, n12 = {round(n.v1)}, n2 = {round(n.v2)}, '
          f'p1 = {n.p1:.4f}, p12 = {n.p12:.4f}, p2 = {n.p2:.4f}, err = {err:.6f}')


# 個別サンプリング
def do_sampling(population1: Set[Any], population2: Set[Any],
                sampling_rate1: float, sampling_rate2: float) -> Cardinality2:
    sample1 = set(sample(list(population1), int(len(population1) * sampling_rate1)))
    sample2 = set(sample(list(population2), int(len(population2) * sampling_rate2)))

    return decompose2(sample1, sample2)


# 補正計算
def do_correction(n_actual: Cardinality2, sampling_rate1: float, sampling_rate2: float) -> Cardinality2:

    # 抽出率は低いほうに合わせてサイズを落とし想定に合わせる
    sampling_rate = min(sampling_rate1, sampling_rate2)

    # 重複分の取りこぼしを補正
    n12_corrected = n_actual.v12 / max(sampling_rate1, sampling_rate2)

    # 各サンプルサイズをスケーリングしたのちに重複分を増やした分だけ引く
    n1_corrected = sampling_rate / sampling_rate1 * (n_actual.v1 + n_actual.v12) - n12_corrected
    n2_corrected = sampling_rate / sampling_rate2 * (n_actual.v12 + n_actual.v2) - n12_corrected

    return Cardinality2(n1_corrected, n12_corrected, n2_corrected)


# 個別サンプリングの場合の理論値の計算
def do_estimation(sampling_rate1: float, sampling_rate2: float, n: Cardinality2) -> Cardinality2:
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの積となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = sampling_rate1 * sampling_rate2 * n.v12
    # サンプリングの総数から重複分を引く
    n1_computed, n2_computed = array(sampling_rate1, sampling_rate2).dot(array(n.size1, n.size2)) - n12_computed

    return Cardinality2(n1_computed, n12_computed, n2_computed)
