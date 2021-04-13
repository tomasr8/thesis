import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.patches as mpatches
import numpy as np

# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
# })

xs = np.array([
    0.1,
    0.07,
    0.15,
    0.12,
    0.06,
    0.25,
    0.1,
    0.15,
])



cumsum = np.cumsum(xs)
print(cumsum)
cumsum = np.insert(cumsum, 0, 0)

fig, ax = plt.subplots(1)
fig.set_size_inches(w=5.02, h=4)
fig.subplots_adjust(left=0.08, right=0.99, bottom=0.1, top=0.98)


for i in range(cumsum.shape[0] - 1):
    a = cumsum[i]
    b = cumsum[i+1]

    if i != 0:
        ax.plot([i+1, i+1], [a, b], c="firebrick", linestyle="--")

    if i < cumsum.shape[0] - 2:
        ax.plot([i+1, i+2], [b, b], c="firebrick")


for i, x in enumerate(xs):
    ax.plot([i+1, i+1], [0, x], color="black", alpha=0.7, linewidth=4)
    ax.plot([i+1], [cumsum[i+1]], marker="o", markerfacecolor='firebrick', markeredgecolor="firebrick", markersize=5)

    if i < len(xs) - 1:
        ax.plot([i+2], [cumsum[i+1]], marker="o", markerfacecolor='white', markeredgecolor="firebrick", markersize=5, zorder=20)

ax.plot([8, 9], [1.0, 1.0], c="firebrick")
plt.plot([0, 1], [0, 0], c="firebrick", clip_on=False, zorder=10)
plt.plot([1], [0], marker="o", markerfacecolor='white', markeredgecolor="firebrick", markersize=5, clip_on=False, zorder=10)

ax.plot([0, 6], [0.595, 0.595], linestyle="dotted", c="royalblue")
ax.plot([6, 6], [0.5, xs[5]], linestyle="dotted", c="royalblue")

ticks = np.arange(8) + 1
ax.set_xticks(ticks)

labels = [f"$x^{i}$" for i in ticks]
ax.set_xticklabels(labels)

# dic = { 1.0 : "some custom text"}
# labels = [ticks[i] if t not in dic.keys() else dic[t] for i,t in enumerate(ticks)]
## or 
# labels = [dic.get(t, ticks[i]) for i,t in enumerate(ticks)]



# plt.axis("equal")
# plt.gca().set_aspect('equal', adjustable='box')

# ax[0].set_xticks([])
# ax[0].set_yticks([])

ax.set_ylim(0, 1.05)
ax.set_xlim(0, 9.2)


ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

cdf = mpatches.Patch(color="firebrick", label="$P(x)$")
weight = mpatches.Patch(color="black", alpha=0.7, label="$w^i$")
plt.legend(handles=[cdf, weight])


# fig.tight_layout()
# plt.show()

plt.savefig('cdf.pgf')