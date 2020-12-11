import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.patches as mpatches
import numpy as np

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

for i in range(cumsum.shape[0] - 1):
    a = cumsum[i]
    b = cumsum[i+1]

    if i != 0:
        ax.plot([i+1, i+1], [a, b], c="black")


    if i < cumsum.shape[0] - 2:
        ax.plot([i+1, i+2], [b, b], c="black")


for i, x in enumerate(xs):
    ax.plot([i+1, i+1], [0, x], color="black", alpha=0.5, linewidth=4)



ax.plot([0, 6], [0.6, 0.6], linestyle="--", c="firebrick")
ax.plot([6, 6], [0.5, xs[5]], linestyle="--", c="firebrick")

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

ax.set_ylim(0, 1.01)
ax.set_xlim(0, 9)


ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

cdf = mpatches.Patch(color="black", label="$P(\\mathbf{x})$")
weight = mpatches.Patch(color="black", alpha=0.5, label="$w^i$")
plt.legend(handles=[cdf, weight])


fig.tight_layout()
plt.show()