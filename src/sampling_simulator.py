import math
from random import sample

from numpy.linalg import norm

from src.sampling_simulator_util import array, decompose_2


def simulate(population1, population2, n1, n12, n2, p1, p12, p2, sampling_rate):

    size1 = n1 + n12
    size2 = n2 + n12

    sampling_rate1 = sampling_rate2 = sampling_rate

    # 個別サンプリング
    sample1 = set(sample(list(population1), int(size1 * sampling_rate1)))
    sample2 = set(sample(list(population2), int(size2 * sampling_rate2)))

    n1_actual, n12_actual, n2_actual, p1_actual, p12_actual, p2_actual = decompose_2(sample1, sample2)
    n_all_actual = n1_actual + n12_actual + n2_actual

    # 理論値の計算
    n12_expected, n1_expected, n2_expected = sampling_rate * array(n12, n1, n2)
    p12_expected, p1_expected, p2_expected = p12, p1, p2

    # 個別サンプリングの場合の理論値の計算
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの二乗となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = (sampling_rate ** 2) * n12
    # サンプリングの総数から重複分を引く
    n1_computed, n2_computed = array(size1, size2) * sampling_rate - n12_computed
    n_all_computed = n1_computed + n2_computed + n12_computed
    p12_computed, p1_computed, p2_computed = array(n12_computed, n1_computed, n2_computed) / n_all_computed

    # 補正
    # 重複分の取りこぼしを補正
    n12_corrected = n12_actual / sampling_rate
    # 重複分を増やした分だけ減らす
    n_all_corrected, n1_corrected, n2_corrected = array(n_all_actual, n1_actual, n2_actual) - (n12_corrected - n12_actual)
    p12_corrected, p1_corrected, p2_corrected = array(n12_corrected, n1_corrected, n2_corrected) / n_all_corrected

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
