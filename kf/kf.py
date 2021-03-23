import math
import numpy as np
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

np.random.seed(0)
N = 40

u = 1

w = 15
v = 10

ground = [0]
no_filter = [0]
measurements = [0]
est = [0]
var = [w]

wk = np.random.normal(0, w, N)
vk = np.random.normal(0, v, N)

for k in range(1, N+1):
    ground.append(ground[-1] + u + wk[k-1])
    no_filter.append(no_filter[-1] + u)
    z = ground[-1] + vk[k-1]
    measurements.append(z)

    x = est[-1] + u
    P = var[-1] + v

    x = x*P/(P+v) + z*v/(P+v)
    P = (P*v)/(P+v)

    est.append(x)
    var.append(P)


fig, ax = plt.subplots(2)
fig.set_size_inches(w=5.02, h=4.5)

ax[0].plot(np.arange(len(ground)), ground, c="green", label="Ground truth")
ax[0].errorbar(np.arange(len(est)), est, c="orange", yerr=var, ms=5, label="Filter estimate")
ax[0].scatter(np.arange(len(measurements)), measurements, c="fuchsia", s=12, label="Measurements", zorder=1000)
ax[0].plot(np.arange(len(no_filter)), no_filter, c="black", label="No filter")

fig.subplots_adjust(left=0.08, right=0.99, bottom=0.07, top=0.99)
fig.subplots_adjust(hspace=0.4)


box = ax[0].get_position()
ax[0].set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis

handles, labels = ax[0].get_legend_handles_labels()
order = [0,3,2,1]
ax[0].legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=False, shadow=False, ncol=2, columnspacing=1.0)
# ax[0].legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc="upper right", fontsize=12)


ax[1].plot(np.arange(len(var)), var, label=r"$\hat{\sigma}$")
ax[1].legend(loc="upper right", fontsize=12)

box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

# fig.tight_layout(pad=0.5)
# fig.subplots_adjust(left=0.07, right=0.99)


# plt.show()

plt.savefig('kf_1d.pgf')