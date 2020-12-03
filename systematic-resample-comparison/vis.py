import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import numpy as np

def plot_confidence_ellipse(x, y, ax, n_std=1.0, edgecolor='fuchsia'):
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      edgecolor=edgecolor, facecolor="none", linestyle='--')

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def find_closest(X, thresh):
    mean = np.mean(X, axis=0)
    X = X[np.square(X - mean).sum(axis=1) < thresh]
    return X


xs = np.linspace(0, 9, num=1000)
ys = 0.07 * np.square(xs)


particles = [
    np.random.multivariate_normal(mean=[0, 0], cov=np.eye(2)*0.05, size=500),
    np.random.multivariate_normal(mean=[5, 0.07*5**2], cov=[[0.15, -0.12],[-0.06, 0.15]], size=500),
    np.random.multivariate_normal(mean=[9, 0.07*9**2], cov=[[0.4, -0.25],[-0.25, 0.4]], size=500)
]

particles_resampled = [
    np.random.multivariate_normal(mean=[0, 0], cov=np.eye(2)*0.05, size=500),
    np.random.multivariate_normal(mean=[5, 0.07*5**2], cov=np.array([[0.15, -0.12],[-0.06, 0.15]])/3, size=500),
    np.random.multivariate_normal(mean=[9, 0.07*9**2], cov=np.array([[0.4, -0.25],[-0.25, 0.4]])/8, size=500)
]


print(particles[0].shape)

fig, ax = plt.subplots(2, 1)

ax[0].plot(xs, ys, alpha=.9)
ax[0].scatter(particles[0][:, 0], particles[0][:, 1], s=1, c="orange")
ax[0].scatter(particles[1][:, 0], particles[1][:, 1], s=1, c="orange")
ax[0].scatter(particles[2][:, 0], particles[2][:, 1], s=1, c="orange")

# plot_confidence_ellipse(ax, [0, 0], np.eye(2)*0.05, n_std=3, edgecolor="gray")
plot_confidence_ellipse(particles[0][:, 0], particles[0][:, 1], ax[0], n_std=3, edgecolor="fuchsia")
plot_confidence_ellipse(particles[1][:, 0], particles[1][:, 1], ax[0], n_std=3, edgecolor="fuchsia")
plot_confidence_ellipse(particles[2][:, 0], particles[2][:, 1], ax[0], n_std=3, edgecolor="fuchsia")
# plot_confidence_ellipse(ax, [9, 0.07*9**2], np.array([[0.2, 0],[0.25, 0.2]]), n_std=3, edgecolor="gray")

particles_best = [
    find_closest(particles_resampled[0], thresh=0.05),
    find_closest(particles_resampled[1], thresh=0.05),
    find_closest(particles_resampled[2], thresh=0.07)
]



ax[1].plot(xs, ys, alpha=.9)
ax[1].scatter(particles_resampled[0][:, 0], particles_resampled[0][:, 1], s=1, c="orange")
ax[1].scatter(particles_resampled[1][:, 0], particles_resampled[1][:, 1], s=1, c="orange")
ax[1].scatter(particles_resampled[2][:, 0], particles_resampled[2][:, 1], s=1, c="orange")

ax[1].scatter(particles_best[0][:, 0], particles_best[0][:, 1], s=1, c="green")
ax[1].scatter(particles_best[1][:, 0], particles_best[1][:, 1], s=1, c="green")
ax[1].scatter(particles_best[2][:, 0], particles_best[2][:, 1], s=1, c="green")

plot_confidence_ellipse(particles_resampled[0][:, 0], particles_resampled[0][:, 1], ax[1], n_std=3, edgecolor="fuchsia")
plot_confidence_ellipse(particles_resampled[1][:, 0], particles_resampled[1][:, 1], ax[1], n_std=3, edgecolor="fuchsia")
plot_confidence_ellipse(particles_resampled[2][:, 0], particles_resampled[2][:, 1], ax[1], n_std=3, edgecolor="fuchsia")

plt.axis("equal")
plt.gca().set_aspect('equal', adjustable='box')

ax[0].set_xticks([])
ax[0].set_yticks([])

ax[1].set_xticks([])
ax[1].set_yticks([])

fig.tight_layout()
plt.show()