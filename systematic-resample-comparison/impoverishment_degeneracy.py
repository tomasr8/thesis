import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import numpy as np
import math

def add_circle(ax, pos, radius, color):
    c = plt.Circle(pos, radius, facecolor=color, alpha=0.8, edgecolor="black")
    ax.add_artist(c)


fig, ax = plt.subplots(1)

ax.plot([0, 10], [6, 6], color="gray")
ax.plot([0, 10], [3, 3], color="gray")
ax.plot([0, 10], [0, 0], color="gray")

np.random.seed(0)



positions = np.random.uniform(0, 5, size=30)
for p in positions:
    add_circle(ax, [p, 6], (math.sqrt(2.5) - abs(p-2.5)**0.5)*0.3, color="lightcoral")

positions = np.random.uniform(4, 10, size=30)
for p in positions:
    add_circle(ax, [p, 6], (math.sqrt(3) - abs(p-7)**0.5)*0.3, color="lightcoral")


positions = np.random.uniform(2, 3, size=1)
for p in positions:
    add_circle(ax, [p, 3], (math.sqrt(2.5) - abs(p-2.5)**0.5)*0.3, color="lightcoral")

positions = np.random.uniform(6.5, 7.5, size=2)
for p in positions:
    add_circle(ax, [p, 3], (math.sqrt(3) - abs(p-7)**0.5)*0.3, color="lightcoral")


positions = np.random.uniform(0, 1.5, size=20)
sizes = np.random.uniform(0.05, 0.1, size=20)
for p, size in zip(positions, sizes):
    add_circle(ax, [p, 3], size, color="lightcoral")

positions = np.random.uniform(3.5, 5.5, size=20)
sizes = np.random.uniform(0.05, 0.1, size=20)
for p, size in zip(positions, sizes):
    add_circle(ax, [p, 3], size, color="lightcoral")

positions = np.random.uniform(8, 10, size=20)
sizes = np.random.uniform(0.05, 0.1, size=20)
for p, size in zip(positions, sizes):
    add_circle(ax, [p, 3], size, color="lightcoral")


positions = np.random.uniform(2.3, 2.7, size=15)
for p in positions:
    add_circle(ax, [p, 0], (math.sqrt(2.5) - abs(p-2.5)**0.5)*0.3, color="lightcoral")

positions = np.random.uniform(6.8, 7.2, size=15)
for p in positions:
    add_circle(ax, [p, 0], (math.sqrt(3) - abs(p-7)**0.5)*0.3, color="lightcoral")


ax.set_xticks([])
ax.set_yticks([])

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.axis("equal")

fig.tight_layout()
plt.show()