import math
import numpy as np
import scipy
import scipy.stats
import matplotlib


matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    # 'text.latex.preamble': r"\usepackage{amsmath}"
})

# matplotlib.rc('text', usetex=True)
# matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
matplotlib.use("pgf")

import matplotlib.pyplot as plt



np.random.seed(0)

xs = np.linspace(1, 9, num=1000)
ys = 5*scipy.stats.norm.pdf(xs, loc=3, scale=0.5) + 5*scipy.stats.norm.pdf(xs, loc=6, scale=1)


fig, ax = plt.subplots()
fig.set_size_inches(w=5.02, h=3)
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.12, top=0.99)


ax.plot(xs, ys, color="firebrick", label=r"$p(x_k|z_k)$")
ax.axvline(3, 0, 0.955, linestyle="--", color="black")
ax.axvline(4.8, 0, 0.259, linestyle="--", color="black")

# ax[0].set_xlim(0, 6)
# ax[0].set_ylim(0, 6)
# ax[1].set_xlim(0, 6)
# ax[1].set_ylim(0, 6)

ax.set_xticks([3, 4.8])
ax.set_xticklabels([r"$\hat{x}^{MAP}$", r"$\hat{x}^{MMSE}$"], fontsize=13)

ax.set_yticks([])
ax.legend(fontsize=13)

# box = ax[0].get_position()
# ax[0].set_position([box.x0, box.y0 + box.height * 0.1,
#                  box.width, box.height * 0.9])

# box = ax[1].get_position()
# ax[1].set_position([box.x0, box.y0 + box.height * 0.1,
#                  box.width, box.height * 0.9])

# handles, labels = ax[0].get_legend_handles_labels()

# order = [2,0,1]
# fig.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc='lower center',
#           fancybox=False, shadow=False, ncol=3, columnspacing=1.0)



# plt.show()

plt.savefig('mmse_map.pgf')