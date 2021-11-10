from random import sample

import numpy as np


def main(population1, population2):

    size1 = len(population1)
    size2 = len(population2)

    intersect = set(population1).intersection(population2)
    intersect_size = len(intersect)
    union = set(population1).union(population2)
    union_size = len(union)

    p1 = (size1 - intersect_size) / union_size
    p2 = (size2 - intersect_size) / union_size
    p12 = intersect_size / union_size

    print(f'p1: {p1}, p2: {p2}, p12: {p12}')

    for sampling_rate in np.arange(0.1, 1, 0.1):
        print('==============================================================')
        print(f'sampling rate: {sampling_rate}')

        # 個別サンプリング
        sample1 = set(sample(list(population1), int(size1 * sampling_rate)))
        sample2 = set(sample(list(population2), int(size2 * sampling_rate)))

        sample_intersection = sample1.intersection(sample2)
        sample_union_size_actual = len(sample1.union(sample2))
        n12_actual = len(sample_intersection)
        p12_actual = n12_actual / sample_union_size_actual

        # 理論値の計算
        n12_expected = sampling_rate * intersect_size
        p12_expected = p12

        # 個別サンプリングの場合の理論値の計算
        # 各サンプリングで選ばれる確率はsampling_rateに等しいので重複する確率はsampling_rateの二乗となる
        # これに母集合の重複数をかけて重複数の期待値を得る
        n12_computed = (sampling_rate ** 2) * intersect_size
        sample_union_size_computed = sampling_rate * (size1 + size2 - n12_computed)
        p12_computed = n12_computed / sample_union_size_computed

        # 補正
        # 重複分の取りこぼしを補正
        n12_corrected = n12_actual / sampling_rate
        # 重複分を増やした分だけ全体数を減らす
        sample_union_size_corrected = sample_union_size_actual - (n12_corrected - n12_actual)
        p12_corrected = n12_corrected / sample_union_size_corrected

        print(f'expected: {n12_expected}, proportion: {p12_expected}')
        print(f'actual: {n12_actual}, proportion: {p12_actual}')
        print(f'computed: {n12_computed}, proportion: {p12_computed}')
        print(f'corrected: {n12_corrected}, proportion: {p12_corrected}')


if __name__ == '__main__':
    set1 = set(range(100000, 300000))
    set2 = set(range(200000, 600000))

    main(set1, set2)
