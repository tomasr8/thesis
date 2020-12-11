import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import numpy as np
import scipy.stats



def add_rectangle(ax, x, y, dx, dy, color, zorder=0):
    rect = patches.Rectangle((x, y), dx, dy, linewidth=1.5, edgecolor=color, facecolor="none", zorder=zorder)
    ax.add_patch(rect)


fig, ax = plt.subplots()

def bad_permutation(ax):
    N = 10
    Ai = [1, 1, 6, 2, 3, 3, 8, 9, 8, 6]
    for i in range(N):
        if i == 1:
            add_rectangle(ax, i, 2, 1, -1, "firebrick", 100)
        else:
            add_rectangle(ax, i, 2, 1, -1, "black")
        ax.text(i+0.4, 1.3, i+1, fontsize=16)

        if i == 1 or i == 3:
            ax.arrow(Ai[i]-0.5, 1, (i+1-Ai[i]), -3, head_width = 0.2, width = 0.01, ec ='firebrick', color="firebrick", length_includes_head=True)
        else:
            ax.arrow(Ai[i]-0.5, 1, (i+1-Ai[i]), -3, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)

    for i in range(N):
        if i == 1:
            add_rectangle(ax, i, -2, 1, -1, "firebrick", 100)
        else:
            add_rectangle(ax, i, -2, 1, -1, "black")
        ax.text(i+0.4, -2.7, Ai[i], fontsize=16)


def good_permutation(ax):
    N = 10
    Ai = [1, 2, 3, 1, 3, 6, 8, 8, 9, 6]
    for i in range(N):
        add_rectangle(ax, i, 2, 1, -1, "black")
        ax.text(i+0.4, 1.3, i+1, fontsize=16)

        ax.arrow(Ai[i]-0.5, 1, (i+1-Ai[i]), -3, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)

    for i in range(N):
        add_rectangle(ax, i, -2, 1, -1, "black")
        ax.text(i+0.4, -2.7, Ai[i], fontsize=16)



# good_permutation(ax)
bad_permutation(ax)

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.axis("equal")
ax.axis('off')

fig.tight_layout()
plt.show()




