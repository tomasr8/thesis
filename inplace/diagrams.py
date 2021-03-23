import math
import numpy as np
import scipy
import scipy.stats
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as patches
import matplotlib.transforms as transforms


def add_rectangle(ax, x, y, dx, dy, color, facecolor="none", zorder=0):
    rect = patches.Rectangle((x, y), dx, dy, linewidth=1.5, edgecolor=color, facecolor=facecolor, zorder=zorder)
    ax.add_patch(rect)


fig, ax = plt.subplots()


def simple_permutation(ax):
    N = 5

    Ai1 = [2, 3, 1, 4, 5]
    for i in range(N):
        add_rectangle(ax, i, 2, 1, -1, "black")
        ax.text(i+0.4, 1.3, Ai1[i], fontsize=16)

    Ai1 = [3, 1, 2, 4, 5]
    for i in range(N):
        add_rectangle(ax, i, -1, 1, -1, "black")
        ax.text(i+0.4, -1.7, Ai1[i], fontsize=16)

    ax.arrow(0.5, -1, 2, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(1.5, -1, -1, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(2.5, -1, -1, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(3.5, -1, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(4.5, -1, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)

    Ai1 = [1, 2, 3, 4, 5]
    for i in range(N):
        add_rectangle(ax, i, -4, 1, -1, "black")
        ax.text(i+0.4, -4.7, Ai1[i], fontsize=16)

    ax.arrow(0.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(1.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(2.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(3.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(4.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)

    ax.text(-1, 1.3, r"$a$", fontsize=16)
    ax.text(-1, -1.7, r"$d$", fontsize=16)
    ax.text(-1, -4.7, r"$c$", fontsize=16)


def hard_permutation(ax):
    N = 5

    Ai1 = [2, 2, 1, 3, 1]
    for i in range(N):
        add_rectangle(ax, i, 2, 1, -1, "black")
        ax.text(i+0.4, 1.3, Ai1[i], fontsize=16)

    Ai1 = [3, 1, 4, 2, 1]
    for i in range(N):
        add_rectangle(ax, i, -1, 1, -1, "black")
        ax.text(i+0.4, -1.7, Ai1[i], fontsize=16)

    ax.arrow(0.5, -1, 2, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(1.5, -1, -1, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(2.5, -1, -1, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(3.5, -1, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(4.5, -1, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)

    Ai1 = [1, 2, 3, 2, 1]
    for i in range(N):
        add_rectangle(ax, i, -4, 1, -1, "black")
        ax.text(i+0.4, -4.7, Ai1[i], fontsize=16)

    ax.arrow(0.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(1.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(2.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(3.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)
    ax.arrow(4.5, -4, 0, 2, head_width = 0.2, width = 0.01, ec ='royalblue', color="royalblue", length_includes_head=True)

    ax.text(-1, 1.3, r"$a$", fontsize=16)
    ax.text(-1, -1.7, r"$d$", fontsize=16)
    ax.text(-1, -4.7, r"$c$", fontsize=16)

    ax.text(6, -0.15, r"$(0)$", fontsize=14)
    ax.text(6, -1.15, r"$(1)$", fontsize=14)
    ax.text(6, -2.15, r"$(2)$", fontsize=14)
    ax.text(6, -3.15, r"$(3)$", fontsize=14)

    Ai1 = [6, 6, 6, 6, 6]
    for i in range(N):
        add_rectangle(ax, i+7, 0.5, 1, -1, "black")
        ax.text(i+0.4+7, -0.2, Ai1[i], fontsize=16)
        
    Ai1 = [3, 1, 4, 6, 6]
    for i in range(N):
        add_rectangle(ax, i+7, -0.5, 1, -1, "black")
        ax.text(i+0.4+7, -1.2, Ai1[i], fontsize=16)


    Ai1 = [3, 1, 4, 2, 6]
    for i in range(N):
        add_rectangle(ax, i+7, -1.5, 1, -1, "black")
        ax.text(i+0.4+7, -2.2, Ai1[i], fontsize=16)


    Ai1 = [3, 1, 4, 2, 1]
    for i in range(N):
        add_rectangle(ax, i+7, -2.5, 1, -1, "black")
        ax.text(i+0.4+7, -3.2, Ai1[i], fontsize=16)

    add_rectangle(ax, 7, -0.5, 1, -1, "royalblue", facecolor="#dbe5ff")
    add_rectangle(ax, 1+7, -0.5, 1, -1, "royalblue", facecolor="#dbe5ff")
    add_rectangle(ax, 2+7, -0.5, 1, -1, "royalblue", facecolor="#dbe5ff")
    add_rectangle(ax, 3+7, -1.5, 1, -1, "royalblue", facecolor="#dbe5ff")
    add_rectangle(ax, 4+7, -2.5, 1, -1, "royalblue", facecolor="#dbe5ff")

# simple_permutation(ax)
hard_permutation(ax)


ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.axis("equal")
ax.axis('off')

fig.tight_layout()
plt.show()




