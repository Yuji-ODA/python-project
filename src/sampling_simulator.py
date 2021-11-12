import math
from random import sample

from numpy.linalg import norm

from src.sampling_simulator_util import array, decompose2, Stats2


def simulate(population1, population2, n, p, sampling_rate1, sampling_rate2=None):

    if sampling_rate2 is None:
        sampling_rate2 = sampling_rate1

    # 理論値の計算
    # 抽出率が違う場合は考えられないので、ここでは小さい方の値である場合を想定する
    n1_expected, n12_expected, n2_expected = min(sampling_rate1, sampling_rate2) * array(n.v1, n.v12, n.v2)
    n_stats_expected = Stats2(n1_expected, n12_expected, n2_expected)
    p_stats_expected = p

    # 個別サンプリングの場合の理論値の計算
    n_computed, p_computed = do_estimation(sampling_rate1, sampling_rate2, n)

    # 個別サンプリングの結果を取得する
    n_actual, p_actual = do_sampling(population1, population2, sampling_rate1, sampling_rate2)

    # 補正計算
    n_corrected, p_corrected = do_correction(n_actual, sampling_rate1, sampling_rate2)

    # 誤差計算
    probabilities_expected = array(p_stats_expected.v1, p_stats_expected.v12, p_stats_expected.v2)
    err_actual = norm(array(p_actual.v1, p_actual.v12, p_actual.v2) - probabilities_expected)
    err_computed = norm(array(p_computed.v1, p_computed.v12, p_computed.v2) - probabilities_expected)
    err_corrected = norm(array(p_corrected.v1, p_corrected.v12, p_corrected.v2) - probabilities_expected)

    print_result('expected ', n_stats_expected, p_stats_expected)
    print_result('actual   ', n_actual, p_actual, err_actual)
    print_result('computed ', n_computed, p_computed, err_computed)
    print_result('corrected', n_corrected, p_corrected, err_corrected)


def print_result(header, n, p, err=math.nan):
    print(f'{header}: n1 = {round(n.v1)}, n12 = {round(n.v1)}, n2 = {round(n.v2)}, '
          f'p1 = {p.v1:.4f}, p12 = {p.v12:.4f}, p2 = {p.v2:.4f}, err = {err:.6f}')


# 個別サンプリング
def do_sampling(population1, population2, sampling_rate1, sampling_rate2):
    sample1 = set(sample(list(population1), int(len(population1) * sampling_rate1)))
    sample2 = set(sample(list(population2), int(len(population2) * sampling_rate2)))

    return decompose2(sample1, sample2)


# 補正計算
def do_correction(n_actual, sampling_rate1, sampling_rate2):

    # 抽出率は低いほうに合わせてサイズを落とし想定に合わせる
    sampling_rate = min(sampling_rate1, sampling_rate2)

    # 重複分の取りこぼしを補正
    n12_corrected = n_actual.v12 / max(sampling_rate1, sampling_rate2)

    # 各サンプルサイズをスケーリングしたのちに重複分を増やした分だけ引く
    n1_corrected = sampling_rate / sampling_rate1 * (n_actual.v1 + n_actual.v12) - n12_corrected
    n2_corrected = sampling_rate / sampling_rate2 * (n_actual.v12 + n_actual.v2) - n12_corrected
    n_all_corrected = n1_corrected + n12_corrected + n2_corrected
    p1_corrected, p12_corrected, p2_corrected = array(n1_corrected, n12_corrected, n2_corrected) / n_all_corrected

    return Stats2(n1_corrected, n12_corrected, n2_corrected), Stats2(p1_corrected, p12_corrected, p2_corrected)


# 個別サンプリングの場合の理論値の計算
def do_estimation(sampling_rate1, sampling_rate2, n):
    # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの積となる
    # これに母集合の重複数をかけて重複数の期待値を得る
    n12_computed = sampling_rate1 * sampling_rate2 * n.v12
    # サンプリングの総数から重複分を引く
    size1 = n.v1 + n.v12
    size2 = n.v12 + n.v2
    n1_computed, n2_computed = array(sampling_rate1, sampling_rate2) * array(size1, size2) - n12_computed
    n_all_computed = n1_computed + n2_computed + n12_computed
    p12_computed, p1_computed, p2_computed = array(n12_computed, n1_computed, n2_computed) / n_all_computed

    return Stats2(n1_computed, n12_computed, n2_computed), Stats2(p12_computed, p1_computed, p2_computed)
