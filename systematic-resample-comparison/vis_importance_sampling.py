import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import numpy as np
import scipy.stats


fig, ax = plt.subplots(figsize=(8, 8))


xs = np.linspace(0, 10, num=1000)

def px(xs):
    return 6*scipy.stats.norm.pdf(xs, loc=3, scale=0.5) + \
           4*scipy.stats.norm.pdf(xs, loc=5, scale=1)

def qx(xs):
    return 20*scipy.stats.norm.pdf(xs, loc=6, scale=2)

target = px(xs)
proposal = qx(xs)

np.random.seed(2)
samples = np.random.normal(loc=6, scale=2, size=100)
samples = samples[(samples > 0) & (samples < 10)]


ax.plot(xs, target)
ax.plot(xs, proposal)

for sample in samples:
    ax.plot([sample, sample], [-1, -2 ], color="black")

    weight = px(sample)/qx(sample)
    ax.plot([sample, sample], [-3, -3 - weight/2.5], color="black")


ax.axis("equal")
ax.axis('off')

ax.legend(["Target $p(x)$", "Proposal $q(x)$"])

fig.tight_layout()
plt.show()