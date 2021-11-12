import math
from itertools import chain
from random import sample

from numpy.linalg import norm

from src.sampling_simulator_util import array, decompose3


def simulate(population1, population2, population3, n, sampling_rate):

    # 個別サンプリング
    sample1 = set(sample(list(population1), int(n.size1 * sampling_rate)))
    sample2 = set(sample(list(population2), int(n.size2 * sampling_rate)))
    sample3 = set(sample(list(population3), int(n.size3 * sampling_rate)))

    n_actual = decompose3(sample1, sample2, sample3)

    # 理論値の計算
    n12_expected, n1_expected, n2_expected = sampling_rate * array(n.v12, n.v1, n.v2)
    p12_expected, p1_expected, p2_expected = n.p12, n.p1, n.p2

    # 個別サンプリングの場合の理論値の計算
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの二乗となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = (sampling_rate ** 2) * n.v12
    # サンプリングの総数から重複分を引く
    n1_computed, n2_computed = array(n.size1, n.size2) * sampling_rate - n12_computed
    n_all_computed = n1_computed + n2_computed + n12_computed
    p12_computed, p1_computed, p2_computed = array(n12_computed, n1_computed, n2_computed) / n_all_computed

    # 補正
    # 重複分の取りこぼしを補正
    n12_corrected = n_actual.v12 / sampling_rate
    # 重複分を増やした分だけ減らす
    n_all_corrected, n1_corrected, n2_corrected = array(n_actual.total_count, n_actual.v1, n_actual.v2) - (n12_corrected - n_actual.v12)
    p12_corrected, p1_corrected, p2_corrected = array(n12_corrected, n1_corrected, n2_corrected) / n_all_corrected

    # 誤差計算
    probs_expected = array(p12_expected, p1_expected, p2_expected)
    err_actual = norm(array(n_actual.p12, n_actual.p1, n_actual.p2) - probs_expected)
    err_computed = norm(array(p12_computed, p1_computed, p2_computed) - probs_expected)
    err_corrected = norm(array(p12_corrected, p1_corrected, p2_corrected) - probs_expected)

    print_result('expected ', n12_expected, n1_expected, n2_expected, p12_expected, p1_expected, p2_expected)
    print_result('actual   ', n_actual.v12, n_actual.v1, n_actual.v2, n_actual.p12, n_actual.p1, n_actual.p2, err_actual)
    print_result('computed ', n12_computed, n1_computed, n2_computed, p12_computed, p1_computed, p2_computed, err_computed)
    print_result('corrected', n12_corrected, n1_corrected, n2_corrected, p12_corrected, p1_corrected, p2_corrected, err_corrected)


def print_result(header, n12, n1, n2, p12, p1, p2, err=math.nan):
    print(f'{header}: n12 = {round(n12)}, n1 = {round(n1)}, n2 = {round(n2)}, '
          f'p12 = {p12:.4f}, p1 = {p1:.4f}, p2 = {p2:.4f}, err = {err:.6f}')


if __name__ == '__main__':
    set1 = set(range(100000))
    set2 = set(chain(range(5000), range(50000, 200000)))
    set3 = set(chain(range(30000), range(150000, 250000)))

    n = decompose3(set1, set2, set3)

    print(n.values())

    simulate(set1, set2, set3, n, 0.1)
