import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import numpy as np
import scipy.stats

def add_circle(ax, pos, radius, color):
    c = plt.Circle(pos, radius, facecolor=color, alpha=0.8, edgecolor="black")
    ax.add_artist(c)


fig, ax = plt.subplots()


xs = np.linspace(0, 9, num=1000)
ys = 2*(0.4 * scipy.stats.norm.pdf(xs, loc=3, scale=0.5) + 0.6 * scipy.stats.norm.pdf(xs, loc=6, scale=0.5))

ax.plot(xs, ys, color="firebrick")

ys = 2*(0.4 * scipy.stats.norm.pdf(xs, loc=3, scale=0.3) + 0.6 * scipy.stats.norm.pdf(xs, loc=6, scale=0.3)) - 4.5
ax.plot(xs, ys, color="firebrick")

add_circle(ax, [3, -1], 0.25, "firebrick")
add_circle(ax, [2.4, -1], 0.15, "firebrick")
add_circle(ax, [3.6, -1], 0.15, "firebrick")
add_circle(ax, [2, -1], 0.1, "firebrick")
add_circle(ax, [4, -1], 0.1, "firebrick")
add_circle(ax, [1.7, -1], 0.05, "firebrick")
add_circle(ax, [4.3, -1], 0.07, "firebrick")

add_circle(ax, [4.5, -1], 0.03, "firebrick")

add_circle(ax, [6, -1], 0.3, "firebrick")
add_circle(ax, [5.4, -1], 0.2, "firebrick")
add_circle(ax, [6.6, -1], 0.2, "firebrick")
add_circle(ax, [5, -1], 0.1, "firebrick")
add_circle(ax, [7, -1], 0.1, "firebrick")
add_circle(ax, [4.7, -1], 0.07, "firebrick")
add_circle(ax, [7.3, -1], 0.05, "firebrick")


# ==================================================
# ==================================================
# ==================================================
# ==================================================

y = -5.5

add_circle(ax, [3, y], 0.3, "firebrick")
add_circle(ax, [2.7, y], 0.2, "firebrick")
add_circle(ax, [3.3, y], 0.2, "firebrick")
add_circle(ax, [2.5, y], 0.15, "firebrick")
add_circle(ax, [3.5, y], 0.15, "firebrick")

add_circle(ax, [6, y], 0.4, "firebrick")
add_circle(ax, [5.6, y], 0.3, "firebrick")
add_circle(ax, [6.4, y], 0.3, "firebrick")
add_circle(ax, [5.3, y], 0.2, "firebrick")
add_circle(ax, [6.7, y], 0.2, "firebrick")


ax.arrow(8.5, -1.9, 0, -0.7, head_width = 0.2, width = 0.01, ec ='black', color="black")
ax.arrow(0.5, -1.9, 0, -0.7, head_width = 0.2, width = 0.01, ec ='black', color="black")

# ax.annotate('default arrow', xy=(0.35,0.3), xytext=(0.6,0.3),
            # arrowprops={'arrowstyle': '->'}, va='center')

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.axis("equal")
# ax.set_xlim(2, 7)
ax.set_ylim(-10, 5)

ax.axis('off')

# fig.tight_layout()
plt.show()