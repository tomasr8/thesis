import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import numpy as np

def plot_confidence_ellipse(ax, x, y, cov, n_std=1.0, edgecolor='fuchsia'):
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
    mean_x = x

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = y

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def plot_ellipse(ax, x, y, angle=45, scale=0.01, ell_radius_x=np.sqrt(10), ell_radius_y=np.sqrt(1), edgecolor='fuchsia'):
    ell_radius_x = np.sqrt(10)
    ell_radius_y = np.sqrt(1)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      edgecolor=edgecolor, facecolor="none", linestyle='--')

    transf = transforms.Affine2D() \
        .rotate_deg(angle) \
        .scale(scale, scale) \
        .translate(x, y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def plot_sensor_fov(ax, position, max_range, max_fov, color='gray', alpha=0.3):
    thetas = np.linspace(position[2] - max_fov/2, position[2] + max_fov/2)
    xs = max_range * np.cos(thetas)
    ys = max_range * np.sin(thetas)

    xs += position[0]
    ys += position[1]

    ax.fill(np.append(xs, position[0]), np.append(ys, position[1]), color=color, alpha=alpha)



def easy():
    fig, ax = plt.subplots()
    np.random.seed(0)

    ax.scatter([0.95], [1], marker="X", s=100, color="#576c7a")
    ax.scatter([1], [1], marker="X", s=100, color="#1f77b4")
    ax.arrow(0.96, 1, 0.03, 0, head_width = 0.005, width = 0.0005, ec ='firebrick', color="firebrick", length_includes_head=True)

    landmarks = np.array([
        [np.cos(0.7), np.sin(0.7)],
        [np.cos(0.3), np.sin(0.3)],
        [np.cos(-0.3), np.sin(-0.3)],
        [np.cos(-0.7), np.sin(-0.7)]
    ])/10 + 1

    measurements = landmarks + np.random.normal(0, 0.004, size=landmarks.shape)
    measurement_color = "#d57120"

    ax.scatter(landmarks[:, 0], landmarks[:, 1], marker="x", color="green")
    ax.scatter(measurements[:, 0], measurements[:, 1], marker="x", color=measurement_color)

    for i in range(4):

        r = np.random.normal(0, 0.0001)
        plot_confidence_ellipse(
            ax, landmarks[i, 0], landmarks[i, 1],
            np.eye(2)/5000 + np.diag([r, r]), edgecolor="green"
        )


    plot_ellipse(
        ax, measurements[0, 0], measurements[0, 1], 40, edgecolor=measurement_color
    )

    plot_ellipse(
        ax, measurements[1, 0], measurements[1, 1], 30, edgecolor=measurement_color
    )

    plot_ellipse(
        ax, measurements[2, 0], measurements[2, 1], -30, edgecolor=measurement_color
    )

    plot_ellipse(
        ax, measurements[3, 0], measurements[3, 1], -40, edgecolor=measurement_color
    )

    ax.scatter([1.14], [1], marker="x", color=measurement_color)
    plot_ellipse(
        ax, 1.14, 1, 0, edgecolor=measurement_color
    )

    plot_sensor_fov(ax, [1, 1, 0], 0.15, 0.6*np.pi, alpha=0.2)


    plt.axis("equal")
    ax.axis('off')
    fig.tight_layout()
    plt.show()



def hard():
    fig, ax = plt.subplots()
    np.random.seed(0)

    ax.scatter([0.95], [1], marker="X", s=100, color="#576c7a")
    ax.scatter([1], [1], marker="X", s=100, color="#1f77b4")
    ax.arrow(0.96, 1, 0.03, 0, head_width = 0.005, width = 0.0005, ec ='firebrick', color="firebrick", length_includes_head=True)

    landmarks = np.array([
        [np.cos(0.7), np.sin(0.7)],
        [np.cos(0.3), np.sin(0.3)],
        [np.cos(-0.3), np.sin(-0.3)],
        [np.cos(-0.7), np.sin(-0.7)]
    ])/10 + 1

    measurements = landmarks + np.random.normal(0, 0.02, size=landmarks.shape)
    measurement_color = "#d57120"

    ax.scatter(landmarks[:, 0], landmarks[:, 1], marker="x", color="green")
    ax.scatter(measurements[:, 0], measurements[:, 1], marker="x", color=measurement_color)

    for i in range(4):

        r = np.random.normal(0, 0.0001)
        plot_confidence_ellipse(
            ax, landmarks[i, 0], landmarks[i, 1],
            np.eye(2)/1000 + np.diag([r, r]), edgecolor="green"
        )

    scale=0.018

    plot_ellipse(
        ax, measurements[0, 0], measurements[0, 1], 40, edgecolor=measurement_color,
        scale=scale
    )

    plot_ellipse(
        ax, measurements[1, 0], measurements[1, 1], 30, edgecolor=measurement_color,
        scale=scale
    )

    plot_ellipse(
        ax, measurements[2, 0], measurements[2, 1], -30, edgecolor=measurement_color,
        scale=scale
    )

    plot_ellipse(
        ax, measurements[3, 0], measurements[3, 1], -40, edgecolor=measurement_color,
        scale=scale
    )

    ax.scatter([1.14], [1], marker="x", color=measurement_color)
    plot_ellipse(
        ax, 1.14, 1, 0, edgecolor=measurement_color, scale=scale
    )

    plot_sensor_fov(ax, [1, 1, 0], 0.15, 0.6*np.pi, alpha=0.2)


    plt.axis("equal")
    ax.axis('off')
    fig.tight_layout()
    plt.show()


def sequential_bad():
    fig, ax = plt.subplots()
    np.random.seed(0)

    ax.scatter([0.95], [1], marker="X", s=100, color="#576c7a")
    ax.scatter([1], [1], marker="X", s=100, color="#1f77b4")
    ax.arrow(0.96, 1, 0.03, 0, head_width = 0.005, width = 0.0005, ec ='firebrick', color="firebrick", length_includes_head=True)

    landmarks = np.array([
        [np.cos(0.4), np.sin(0.4)],
        [np.cos(-0.0), np.sin(-0.0)]
    ])/10 + 1

    measurements = np.array([
        [1.11, 1.04],
        [1.07, 0.966]
    ])

    measurement_color = "#d57120"

    ax.scatter(landmarks[:, 0], landmarks[:, 1], marker="x", color="green", s=50)
    ax.scatter(measurements[:, 0], measurements[:, 1], marker="x", color=measurement_color, s=50)

    ax.plot([landmarks[1, 0], measurements[0, 0]], [landmarks[1, 1], measurements[0, 1]], color="firebrick", linestyle="--")
    ax.plot([landmarks[0, 0], measurements[1, 0]], [landmarks[0, 1], measurements[1, 1]], color="firebrick", linestyle="--")

    plot_sensor_fov(ax, [1, 1, 0], 0.15, 0.6*np.pi, alpha=0.2)

    plt.axis("equal")
    ax.axis('off')
    fig.tight_layout()
    plt.show()


def sort_bad():
    fig, ax = plt.subplots()
    np.random.seed(0)

    ax.scatter([0.95], [1], marker="X", s=100, color="#576c7a")
    ax.scatter([1], [1], marker="X", s=100, color="#1f77b4")
    ax.arrow(0.96, 1, 0.03, 0, head_width = 0.005, width = 0.0005, ec ='firebrick', color="firebrick", length_includes_head=True)

    landmarks = np.array([
        [np.cos(0.4), np.sin(0.4)],
        [np.cos(-0.0), np.sin(-0.0)]
    ])/10 + 1

    measurements = np.array([
        [1.1, 1.015],
        [1.07, 0.966]
    ])

    measurement_color = "#d57120"

    ax.scatter(landmarks[:, 0], landmarks[:, 1], marker="x", color="green", s=50)
    ax.scatter(measurements[:, 0], measurements[:, 1], marker="x", color=measurement_color, s=50)

    ax.plot([landmarks[1, 0], measurements[0, 0]], [landmarks[1, 1], measurements[0, 1]], color="firebrick", linestyle="--")
    ax.plot([landmarks[0, 0], measurements[1, 0]], [landmarks[0, 1], measurements[1, 1]], color="firebrick", linestyle="--")

    plot_sensor_fov(ax, [1, 1, 0], 0.15, 0.6*np.pi, alpha=0.2)

    plt.axis("equal")
    ax.axis('off')
    fig.tight_layout()
    plt.show()


easy()
# hard()
# sequential_bad()
# sort_bad()