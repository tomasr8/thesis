import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import numpy as np
import scipy.stats


def add_circle(ax, pos, radius, facecolor, edgecolor):
    c = plt.Circle(pos, radius, facecolor=facecolor, alpha=1, edgecolor=edgecolor)
    ax.add_artist(c)


def add_rectangle(ax, x, y, dx, dy, color):
    rect = patches.Rectangle((x, y), dx, dy, linewidth=1, edgecolor=color, facecolor=color)
    ax.add_patch(rect)

def draw_vertical_line(ax, x, y, dy):
    ax.plot([x, x], [y, y+dy], linestyle="-", color="black")

def draw_horizontal_line(ax, x, y, dx, color="black"):
    ax.plot([x, x+dx], [y, y], linestyle="--", color=color)


def multinomial():
    fig, ax = plt.subplots()

    cmap = plt.get_cmap('Set3')

    add_rectangle(ax, 0, 0, 1.5, 1, "#ff512e")
    add_rectangle(ax, 1.5, 0, 2.5, 1, "#ff962e")
    add_rectangle(ax, 4, 0, 1.5, 1, "#eaff2e")
    add_rectangle(ax, 5.5, 0, 4, 1, "#2effbd")
    add_rectangle(ax, 8.5, 0, 1.5, 1, "#b22eff")

    # draw_vertical_line(ax, 2, 0, 1)
    # draw_vertical_line(ax, 4, 0, 1)
    # draw_vertical_line(ax, 6, 0, 1)
    # draw_vertical_line(ax, 8, 0, 1)

    add_circle(ax, [2.2, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [3.5, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [6.5, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [7, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [8, 0.5], 0.15, "#2b2b2b", "none")


    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax.axis("equal")
    ax.axis('off')

    fig.tight_layout()
    plt.show()


def stratified():
    fig, ax = plt.subplots()

    cmap = plt.get_cmap('Set3')

    add_rectangle(ax, 0, 0, 1.5, 1, "#ff512e")
    add_rectangle(ax, 1.5, 0, 2.5, 1, "#ff962e")
    add_rectangle(ax, 4, 0, 1.5, 1, "#eaff2e")
    add_rectangle(ax, 5.5, 0, 4, 1, "#2effbd")
    add_rectangle(ax, 8.5, 0, 1.5, 1, "#b22eff")

    draw_vertical_line(ax, 0, 0, 1)
    draw_vertical_line(ax, 2, 0, 1)
    draw_vertical_line(ax, 4, 0, 1)
    draw_vertical_line(ax, 6, 0, 1)
    draw_vertical_line(ax, 8, 0, 1)

    add_circle(ax, [0.7, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [2.5, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [5.7, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [7.2, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [8.9, 0.5], 0.15, "#2b2b2b", "none")

    draw_horizontal_line(ax, 0, 0.5, 0.7)
    draw_horizontal_line(ax, 2, 0.5, 0.5)
    draw_horizontal_line(ax, 4, 0.5, 1.7)
    draw_horizontal_line(ax, 6, 0.5, 1.2)
    draw_horizontal_line(ax, 8, 0.5, 0.9)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax.axis("equal")
    ax.axis('off')

    fig.tight_layout()
    plt.show()


def systematic():
    fig, ax = plt.subplots()

    cmap = plt.get_cmap('Set3')

    add_rectangle(ax, 0, 0, 1.5, 1, "#ff512e")
    add_rectangle(ax, 1.5, 0, 2.5, 1, "#ff962e")
    add_rectangle(ax, 4, 0, 1.5, 1, "#eaff2e")
    add_rectangle(ax, 5.5, 0, 4, 1, "#2effbd")
    add_rectangle(ax, 8.5, 0, 1.5, 1, "#b22eff")

    draw_vertical_line(ax, 0, 0, 1)
    draw_vertical_line(ax, 2, 0, 1)
    draw_vertical_line(ax, 4, 0, 1)
    draw_vertical_line(ax, 6, 0, 1)
    draw_vertical_line(ax, 8, 0, 1)

    add_circle(ax, [1.2, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [3.2, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [5.2, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [7.2, 0.5], 0.15, "#2b2b2b", "none")
    add_circle(ax, [9.2, 0.5], 0.15, "#2b2b2b", "none")

    draw_horizontal_line(ax, 0, 0.5, 1.2)
    draw_horizontal_line(ax, 2, 0.5, 1.2)
    draw_horizontal_line(ax, 4, 0.5, 1.2)
    draw_horizontal_line(ax, 6, 0.5, 1.2)
    draw_horizontal_line(ax, 8, 0.5, 1.2)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax.axis("equal")
    ax.axis('off')

    fig.tight_layout()
    plt.show()



# multinomial()
# stratified()
systematic()


