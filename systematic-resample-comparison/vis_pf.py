import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import numpy as np
import scipy.stats



def add_rectangle(ax, x, y, dx, dy, color, linestyle="-"):
    rect = patches.Rectangle((x, y), dx, dy, linewidth=1.5, edgecolor=color, facecolor="#e8e8e8", linestyle=linestyle)
    ax.add_patch(rect)


def sis(ax):
    add_rectangle(ax, 0, 0, 2.5, 1, "royalblue")
    add_rectangle(ax, 4, 0, 2.5, 1, "royalblue")
    add_rectangle(ax, 8, 0, 2.5, 1, "royalblue")
    add_rectangle(ax, 6, -2.5, 2.5, 1, "royalblue", "--")


    style = "Simple, tail_width=0.5, head_width=6, head_length=8"
    kw = dict(arrowstyle=style, color="k")
    # arrow = patches.FancyArrowPatch((5.75, 1.1), (9.25, 1.1),
    #                             connectionstyle="arc3,rad=-.6", **kw)
    # ax.add_patch(arrow)

    # arrow = patches.FancyArrowPatch((8.75, -0.1), (8.35, -2.5),
    #                             connectionstyle="arc3,rad=-.6", **kw)
    # ax.add_patch(arrow)


    style = "Simple, tail_width=0.5, head_width=6, head_length=8"
    kw = dict(arrowstyle=style, color="k")
    arrow = patches.FancyArrowPatch((2.6, 0.5), (3.9, 0.5), **kw)
    ax.add_patch(arrow)

    arrow = patches.FancyArrowPatch((6.6, 0.5), (7.9, 0.5), **kw)
    ax.add_patch(arrow)


    arrow = patches.FancyArrowPatch((9.25, -0.1), (8.6, -2), connectionstyle="arc3,rad=-.2", **kw)
    ax.add_patch(arrow)

    arrow = patches.FancyArrowPatch((5.9, -2), (5.25, -0.1), connectionstyle="arc3,rad=-.2", **kw)
    ax.add_patch(arrow)

    ax.text(1.25, 0.5, "Draw from\nprior $p(x)$", ha="center", va="center", color="black")
    ax.text(5.25, 0.5, "Draw from\nproposal $q(x)$", ha="center", va="center")
    ax.text(9.25, 0.5, "Update weights", ha="center", va="center")
    ax.text(7.25, -2, "Estimate state", ha="center", va="center")



    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax.axis("equal")
    ax.axis('off')


def pf(ax):
    add_rectangle(ax, 0, 0, 2.5, 1, "royalblue")
    add_rectangle(ax, 4, 0, 2.5, 1, "royalblue")
    add_rectangle(ax, 8, 0, 2.5, 1, "royalblue")
    add_rectangle(ax, 8, -2.5, 2.5, 1, "royalblue", "--")
    add_rectangle(ax, 4, -2.5, 2.5, 1, "royalblue", "--")


    style = "Simple, tail_width=0.5, head_width=6, head_length=8"
    kw = dict(arrowstyle=style, color="k")

    style = "Simple, tail_width=0.5, head_width=6, head_length=8"
    kw = dict(arrowstyle=style, color="k")
    arrow = patches.FancyArrowPatch((2.6, 0.5), (3.9, 0.5), **kw)
    ax.add_patch(arrow)

    arrow = patches.FancyArrowPatch((6.6, 0.5), (7.9, 0.5), **kw)
    ax.add_patch(arrow)


    arrow = patches.FancyArrowPatch((9.25, -0.1), (9.25, -1.4), **kw)
    ax.add_patch(arrow)

    arrow = patches.FancyArrowPatch((7.9, -2), (6.6, -2), **kw)
    ax.add_patch(arrow)

    arrow = patches.FancyArrowPatch((5.25, -1.4), (5.25, -0.1), **kw)
    ax.add_patch(arrow)

    ax.text(1.25, 0.5, "Draw from\nprior $p(x)$", ha="center", va="center", color="black")
    ax.text(5.25, 0.5, "Draw from\nproposal $q(x)$", ha="center", va="center")
    ax.text(9.25, 0.5, "Update weights", ha="center", va="center")
    ax.text(9.25, -2, "Estimate state", ha="center", va="center")
    ax.text(5.25, -2, "Resample particles", ha="center", va="center")




    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax.axis("equal")
    ax.axis('off')


fig, ax = plt.subplots(1)


sis(ax)
# pf(ax)
# fig.tight_layout()
plt.show()
# import matplotlib
# for name, hex in matplotlib.colors.cnames.items():
#     print(name, hex)