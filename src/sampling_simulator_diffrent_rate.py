import math
from random import sample

from numpy.linalg import norm

from src.sampling_simulator_util import array, decompose_2


def simulate(population1, population2, n1, n12, n2, p1, p12, p2, sampling_rate1, sampling_rate2=None):

    if sampling_rate2 is None:
        sampling_rate2 = sampling_rate1

    # 理論値の計算
    # 抽出率が違う場合は考えられないので、ここでは小さい方の値である場合を想定する
    n1_expected, n12_expected, n2_expected = min(sampling_rate1, sampling_rate2) * array(n1, n12, n2)
    p12_expected, p1_expected, p2_expected = p12, p1, p2

    # 個別サンプリングの場合の理論値の計算
    n1_computed, n12_computed, n2_computed, p12_computed, p1_computed, p2_computed = \
        do_estimation(sampling_rate1, sampling_rate2, n1, n12, n2)

    # 個別サンプリングの結果を取得する
    n1_actual, n12_actual, n2_actual, p1_actual, p12_actual, p2_actual = \
        do_sampling(population1, population2, sampling_rate1, sampling_rate2)

    # 補正計算
    n1_corrected, n12_corrected, n2_corrected, p1_corrected, p12_corrected, p2_corrected = \
        do_correction(n1_actual, n12_actual, n2_actual, sampling_rate1, sampling_rate2)

    # 誤差計算
    probs_expected = array(p12_expected, p1_expected, p2_expected)
    err_actual = norm(array(p12_actual, p1_actual, p2_actual) - probs_expected)
    err_computed = norm(array(p12_computed, p1_computed, p2_computed) - probs_expected)
    err_corrected = norm(array(p12_corrected, p1_corrected, p2_corrected) - probs_expected)

    print_result('expected ', n12_expected, n1_expected, n2_expected, p12_expected, p1_expected, p2_expected)
    print_result('actual   ', n12_actual, n1_actual, n2_actual, p12_actual, p1_actual, p2_actual, err_actual)
    print_result('computed ', n12_computed, n1_computed, n2_computed, p12_computed, p1_computed, p2_computed, err_computed)
    print_result('corrected', n12_corrected, n1_corrected, n2_corrected, p12_corrected, p1_corrected, p2_corrected, err_corrected)


def print_result(header, n12, n1, n2, p12, p1, p2, err=math.nan):
    print(f'{header}: n12 = {round(n12)}, n1 = {round(n1)}, n2 = {round(n2)}, '
          f'p12 = {p12:.4f}, p1 = {p1:.4f}, p2 = {p2:.4f}, err = {err:.6f}')


# 個別サンプリング
def do_sampling(population1, population2, sampling_rate1, sampling_rate2):
    sample1 = set(sample(list(population1), int(len(population1) * sampling_rate1)))
    sample2 = set(sample(list(population2), int(len(population2) * sampling_rate2)))

    return decompose_2(sample1, sample2)


# 補正計算
def do_correction(n1_actual, n12_actual, n2_actual, sampling_rate1, sampling_rate2):

    # 抽出率は低いほうに合わせてサイズを落とし想定に合わせる
    sampling_rate = min(sampling_rate1, sampling_rate2)

    # 重複分の取りこぼしを補正
    n12_corrected = n12_actual / max(sampling_rate1, sampling_rate2)

    # 重複分を増やした分だけ減らす
    n1_corrected = sampling_rate / sampling_rate1 * (n1_actual - (n12_corrected - n12_actual))
    n2_corrected = sampling_rate / sampling_rate2 * (n2_actual - (n12_corrected - n12_actual))
    n_all_corrected = n1_corrected + n12_corrected + n2_corrected
    p1_corrected, p12_corrected, p2_corrected = array(n1_corrected, n12_corrected, n2_corrected) / n_all_corrected

    return n1_corrected, n12_corrected, n2_corrected, p1_corrected, p12_corrected, p2_corrected


# 個別サンプリングの場合の理論値の計算
def do_estimation(sampling_rate1, sampling_rate2, n1, n12, n2):
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの積となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = sampling_rate1 * sampling_rate2 * n12
    # サンプリングの総数から重複分を引く
    n1_computed, n2_computed = array(sampling_rate1, sampling_rate2) * array(n1 + n12, n12 + n2) - n12_computed
    n_all_computed = n1_computed + n2_computed + n12_computed
    p12_computed, p1_computed, p2_computed = array(n12_computed, n1_computed, n2_computed) / n_all_computed

    return n1_computed, n12_computed, n2_computed, p12_computed, p1_computed, p2_computed
