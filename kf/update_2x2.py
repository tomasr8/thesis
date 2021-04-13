import math
import numpy as np
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def divide(arr):
    return [x/255.0 for x in arr]

def plot_confidence_ellipse(mean, cov, ax, n_std=1.0, edgecolor='fuchsia', facecolor="#a8a8a8", zorder=0):
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      edgecolor=edgecolor, facecolor=facecolor, linestyle='--', linewidth=1.5, zorder=zorder)

    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = mean[0]

    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = mean[1]

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


np.random.seed(0)

ground_position = [2.8, 1.8]
estimate = np.array([3.4, 3.4])
estimate_cov = np.array([
    [4.5, -2],
    [-2, 4.5]
], dtype=np.float)

measurement = np.array([2.0, 2.2])
measurement_cov = np.array([
    [3, 1.5],
    [1.5, 2]
])

residual = (measurement - estimate).T
residual_cov = estimate_cov + measurement_cov
gain = estimate_cov @ np.linalg.inv(residual_cov)
new_estimate = estimate + gain @ residual
new_estimate_cov = (np.eye(2) - gain) @ estimate_cov

fig, ax = plt.subplots(2, 1)
fig.set_size_inches(w=5.02, h=5)
fig.subplots_adjust(hspace=0.1)
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.1, top=0.99)

# blue = [
#     "#1f77b4", divide([31, 119, 180, 100])
# ]

# orange = [
#     "#ff7f0e", divide([255, 127, 14, 100])
# ]

# green = [
#     "#2ca02c", divide([44, 160, 44, 100])
# ]

ALPHA = 70

blue = [
    "#1C77C3", divide([28, 119, 195, ALPHA])
]

orange = [
    "#F39237", divide([243, 146, 55, ALPHA])
]

green = [
    "#2CA03F", divide([44, 160, 63, ALPHA])
]

purple = [
    "#D36582", divide([211, 101, 130, ALPHA])
]

black = [
    "#36382E", divide([54, 56, 46, ALPHA])
]


plot_confidence_ellipse(estimate, estimate_cov, ax[1], n_std=1.0, edgecolor=blue[0], facecolor=blue[1], zorder=10)
plot_confidence_ellipse(measurement, measurement_cov, ax[1], n_std=1.0, edgecolor=orange[0], facecolor=orange[1], zorder=11)
plot_confidence_ellipse(new_estimate, new_estimate_cov, ax[1], n_std=1.0, edgecolor=green[0], facecolor=green[1], zorder=12)
ax[1].scatter(estimate[0], estimate[1], marker="o", color=blue[0], label="Current estimate", zorder=1000)
ax[1].scatter(measurement[0], measurement[1], marker="o", color=orange[0], label="Measurement", zorder=1001)
ax[1].scatter(new_estimate[0], new_estimate[1], marker="o", color=green[0], zorder=1002)

ax[1].set_xlim(0, 6)
ax[1].set_ylim(0, 6)
ax[1].set_xticks([])
ax[1].set_yticks([])

# box = ax[0].get_position()
# ax[0].set_position([box.x0, box.y0 + box.height * 0.1,
#                  box.width, box.height * 0.9])

# box = ax[1].get_position()
# ax[1].set_position([box.x0, box.y0 + box.height * 0.1,
#                  box.width, box.height * 0.9])

# handles, labels = ax[1].get_legend_handles_labels()

# order = [0,1]
# fig.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc='lower center',
#           fancybox=False, shadow=False, ncol=3, columnspacing=1.0)


legend_elements = [
                   Line2D([0], [0], marker='s', color='w', label=r'$p(x_k|z_{1:k-1})$',
                          markerfacecolor=blue[0], markersize=13),
                    Line2D([0], [0], marker='s', color='w', label=r'$p(z_k|x_{k})$',
                          markerfacecolor=orange[0], markersize=13),
                Line2D([0], [0], marker='s', color='w', label=r'$p(x_k|z_k$)',
                          markerfacecolor=green[0], markersize=13)]

fig.legend(handles=legend_elements, loc='lower center',
          fancybox=False, shadow=False, ncol=3, columnspacing=1.0)


# ============================

estimate = 3
estimate_var = 0.9

measurement = 5.5
measurement_var = 0.5

residual = (measurement - estimate)
residual_var = estimate_var + measurement_var
gain = estimate_var / residual_var
new_estimate = estimate + gain * residual
new_estimate_var = (1 - gain) * estimate_var

xs = np.linspace(0, 7, num=1000)

ax[0].plot(xs, scipy.stats.norm.pdf(xs, loc=estimate, scale=estimate_var), color=blue[0])
ax[0].plot(xs, scipy.stats.norm.pdf(xs, loc=measurement, scale=measurement_var), color=orange[0])
ax[0].plot(xs, scipy.stats.norm.pdf(xs, loc=new_estimate, scale=new_estimate_var), color=green[0])

ax[0].fill_between(xs, 0, scipy.stats.norm.pdf(xs, loc=estimate, scale=estimate_var), color=blue[1], zorder=10)
ax[0].fill_between(xs, 0, scipy.stats.norm.pdf(xs, loc=measurement, scale=measurement_var), color=orange[1], zorder=11)
ax[0].fill_between(xs, 0, scipy.stats.norm.pdf(xs, loc=new_estimate, scale=new_estimate_var), color=green[1], zorder=12)

ax[0].set_xticks([])
ax[0].set_yticks([])

# print(plt.rcParams['axes.prop_cycle'].by_key()['color'])

# plt.show()

plt.savefig('kf_update_2.pgf')