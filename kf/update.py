import math
import numpy as np
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from matplotlib.colors import to_rgba

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def divide(arr):
    return [x/255.0 for x in arr]

def plot_confidence_ellipse(mean, cov, ax, n_std=1.0, edgecolor='fuchsia', facecolor="#a8a8a8"):
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      edgecolor=edgecolor, facecolor=facecolor, linestyle='--')

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

ground_position = [3, 3]
estimate = np.array([3.6, 3.6])
estimate_cov = np.array([
    [4.5, -1],
    [-1, 4.5]
], dtype=np.float)

measurement = np.array([2.5, 2.7])
measurement_cov = np.array([
    [2, 0.5],
    [0.5, 0.4]
])

residual = (measurement - estimate).T
print(residual)
residual_cov = estimate_cov + measurement_cov
print(residual_cov)
gain = estimate_cov @ np.linalg.inv(residual_cov)
new_estimate = estimate + gain @ residual
new_estimate_cov = (np.eye(2) - gain) @ estimate_cov

print(new_estimate, new_estimate_cov)

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(w=5.02, h=3)
fig.subplots_adjust(left=0.05, right=0.99, bottom=0.15, top=0.95)


plot_confidence_ellipse(estimate, estimate_cov, ax[0], n_std=1.0, edgecolor='#ffbc47', facecolor=divide([255, 216, 148, 100]))
plot_confidence_ellipse(measurement, measurement_cov, ax[0], n_std=1.0, edgecolor='#a8a8a8', facecolor=divide([168, 168, 168, 100]))
ax[0].scatter(estimate[0], estimate[1], marker="x", color="orange", label="Current estimate", zorder=1000)
ax[0].scatter(measurement[0], measurement[1], marker="o", color="#858585", label="Measurement", zorder=1000)
ax[0].scatter(ground_position[0], ground_position[1], marker="x", color="green", label="Ground truth", zorder=1000)


plot_confidence_ellipse(new_estimate, new_estimate_cov, ax[1], n_std=1.0, edgecolor='#ffbc47', facecolor=divide([255, 216, 148, 100]))
ax[1].scatter(new_estimate[0], new_estimate[1], marker="x", color="orange", zorder=1000)
ax[1].scatter(ground_position[0], ground_position[1], marker="x", color="green", zorder=1001)

ax[0].set_xlim(0, 6)
ax[0].set_ylim(0, 6)
ax[1].set_xlim(0, 6)
ax[1].set_ylim(0, 6)

ax[0].set_yticks([0, 2, 4, 6])
ax[1].set_yticks([0, 2, 4, 6])

box = ax[0].get_position()
ax[0].set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

handles, labels = ax[0].get_legend_handles_labels()

order = [0,1,2]
fig.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc='lower center',
          fancybox=False, shadow=False, ncol=3, columnspacing=1.0)





# plt.show()

plt.savefig('kf_update.pgf')