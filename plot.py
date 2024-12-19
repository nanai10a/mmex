import numpy
import os
import pandas
import sys

import matplotlib.colors
import matplotlib.pyplot

# helper functions
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# Define the custom interpolation function
def interpolate_colors():
    n_points = 500

    # Define the custom colors
    colors = [
        [100, 200, 200], # +1
        [50, 50, 150],   # transition
        [0, 0, 0],       # dark
        [150, 50, 50],   # transition
        [200, 200, 100]  # -1
    ]

    interpolated = []
    num_segments = len(colors) - 1
    points_per_segment = n_points // num_segments

    for i in range(num_segments):
        start_color = numpy.array(colors[i]) / 255.0
        end_color = numpy.array(colors[i + 1]) / 255.0
        segment = numpy.linspace(start_color, end_color, points_per_segment)
        interpolated.extend(segment)

    return numpy.array(interpolated)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

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

fig, axes = matplotlib.pyplot.subplots(num_i, num_j, figsize=(15, 15))
axes = axes.flatten()

# Create a custom colormap
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("custom_cmap", interpolate_colors())

for i in range(num_i):
    for j in range(num_j):
        surface = numpy.zeros((df['y'].max() + 1, df['x'].max() + 1))

        # Populate the surface with the corresponding data
        for _, row in df.iterrows():
            surface[int(row['y']), int(row['x'])] = row[f'm{i}{j}']

        # Calculate the max absolute value for color scaling
        abs_max = max(numpy.abs(float(df[f'm{i}{j}'].max())), numpy.abs(float(df[f'm{i}{j}'].min())))

        ax = axes[i * 4 + j]
        im = ax.imshow(surface, extent=(0, df['x'].max() + 1, df['y'].max() + 1, 0),
                       origin='upper', cmap=cmap, vmin=-abs_max, vmax=abs_max)  # Apply custom colormap with scaling
        fig.colorbar(im, ax=ax)
        ax.set_title(f'm{i}{j}')
        ax.axis('off')

matplotlib.pyplot.show()
