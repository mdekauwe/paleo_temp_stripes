#!/usr/bin/env python

"""
Plot warming stripes for the last 500 Mya of temperature variability.

Temperature data from:

* Scotese et al. (2021) Phanerozoic paleotemperatures: The earth’s changing
climate during the last 540 million years. Earth-Science Reviews, 215, 103503

https://www.sciencedirect.com/science/article/pii/S0012825221000027

Using code from:

https://matplotlib.org/matplotblog/posts/warming-stripes/
https://github.com/spestana/ulmo-warming-stripes/blob/main/warming-stripes.ipynb

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (14.11.2022)"
__email__ = "mdekauwe@gmail.com"

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import pandas as pd
import sys
import numpy as np

# Using data from the global temperature model presented in Scotese et al.,
# which includes estimates of global average temperate (GAT)
df = pd.read_csv("data/temp.csv")

GAT_mean = df.GAT.mean()

# Calculate the annual anomaly between the annual mean temp and the overall mean
df["anomaly"] = df.GAT - GAT_mean

# rectangle lower left y coordinate, minimum anomaly value
rect_ll_y = df['anomaly'].min()

# rectangle height, range between min and max anomaly values
rect_height = np.abs(df['anomaly'].max() - df['anomaly'].min())
year_start = df.Age[0]
year_end = df.Age.iloc[-1] + 1


upp = df['anomaly'].max()
low = df['anomaly'].min()


cmap = ListedColormap([
    '#08306b', '#08519c', '#2171b5', '#4292c6',
    '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
    '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
])

# create a collection with a rectangle for each year
col = PatchCollection([
    Rectangle((x, rect_ll_y), 1, rect_height)
    for x in range(year_start, year_end)
])
print(rect_ll_y)
print(rect_height)

fig = plt.figure(figsize=(10, 1))
plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# set up the axes
#ax = fig.add_axes([0, 0, 1, 1])
ax = fig.add_axes([1, 1, 1, 1])
#ax.set_axis_off()



col.set_array(df['anomaly'])
col.set_cmap(cmap)
col.set_clim(-rect_height/2, rect_height/2) # set the limits of our colormap



ax.add_collection(col)
ax.set_xlim(540, 0)

ax.plot(df['anomaly'], linestyle='-', lw=0.5, color='k')
ax.axhline(0, linestyle='--', color='k', lw=0.5)

ax.set_ylim(low, upp)
ax.set_xlabel("Years (Mya)")
ax.set_ylabel("Temperature anomaly\n($^\circ$C)")
fig.savefig('paleo_warming_stripes.png', dpi=300, bbox_inches='tight')
