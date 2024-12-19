import numpy
import os
import pandas
import sys

import matplotlib.pyplot

if len(sys.argv) != 2:
    print('Usage: python plot.py <path>')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print('Couldn\'t find file: {sys.argv[1]}')
    sys.exit(1)

# Load your DataFrame
df = pandas.read_csv(sys.argv[1])

# Initialize variables to store the maximum values of i and j
num_i = 0
num_j = 0

# Iterate through the column names to find the maximum i and j values
for name in df.columns:
    if name.startswith('m') and len(name) == 3:
        name_i = int(name[1]) + 1
        name_j = int(name[2]) + 1

        if name_i > num_i:
            num_i = name_i

        if name_j > num_j:
            num_j = name_j

# pandasのSeriesをビン分割して、分布のヒートマップとして使用する
num_bins = 100  # 目盛りの粗さを調整するためのビン数

fig, axes = matplotlib.pyplot.subplots(1, num_i * num_j, figsize=(20, 10))
axes = axes.flatten()

for i in range(num_i):
    for j in range(num_j):
        m_col = f'm{i}{j}'
        b_col = f'b{i}{j}'

        # ビン分割
        df[b_col] = pandas.cut(df[m_col], bins=num_bins)

        # 各ビンごとの出現頻度を計算
        bin_counts = df[b_col].value_counts().sort_index()

        # データをヒートマップ表示 (縦方向に修正)
        heat_data = numpy.array([bin_counts.values]).reshape(-1, 1)  # 縦方向に配列変換
        ax = axes[i * num_j + j]
        im = ax.imshow(heat_data, aspect='auto', cmap='viridis')

        # 軸の設定
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([0, len(bin_counts) - 1])
        ax.set_yticklabels([bin_counts.index.min().left, bin_counts.index.max().right])
        ax.set_title(m_col)

matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()
