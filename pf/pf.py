import math
import numpy as np
import scipy
import scipy.stats
import matplotlib.pyplot as plt
from filterpy.monte_carlo import systematic_resample, multinomial_resample, stratified_resample

# https://sci-hub.se/10.1016/j.micpro.2016.07.017

def get_initial_particles(n):
    return np.random.uniform(-2, 2, n), np.ones(n, dtype=np.float64) / n

def get_measurement(x, nk):
    return (x**2)/20 + np.random.normal(loc=0, scale=nk)

# def predict(particles, k, vk):
#     return particles + 1/(5+particles) + 1 + \
#         np.random.normal(loc=0, scale=vk, size=particles.shape[0])

# def predict(particles, k, vk):
#     return particles + 1 + \
#         np.random.normal(loc=0, scale=vk, size=particles.shape[0])

def predict(particles, k, vk):
    return particles/2 + (25*particles)/(1+particles**2) + \
        8*np.cos(1.2*k) + \
        np.random.normal(loc=0, scale=vk, size=particles.shape[0])

def update(particles, weights, zk, nk):
    weights *= scipy.stats.norm((particles**2)/20, nk).pdf(zk)

    weights += 1.e-300      # avoid round-off to zero
    weights /= np.sum(weights) # normalize

    return weights

def resample(particles, weights, fn=systematic_resample):
    indices = fn(weights)
    particles[:] = particles[indices]
    weights.fill(1.0 / particles.shape[0])

    return particles, weights


def neff(weights):
    return 1. / np.sum(np.square(weights))


def estimate(particles, weights):
    return np.average(particles, weights=weights)
    # var  = np.average((pos - mean)**2, weights=weights, axis=0)


# def f(x, k, vk):
#     return x + 1/(5+x) + 1 + \
#         np.random.normal(loc=0, scale=vk)

# def f(x, k, vk):
#     return x + 1 + \
#         np.random.normal(loc=0, scale=vk)

def f(x, k, vk):
    return x/2 + (25*x)/(1+x**2) + 8*np.cos(1.2*k) + \
        np.random.normal(loc=0, scale=vk)


def likelihood(xk, zk, nk):
    return scipy.stats.norm((xk**2)/20, nk).pdf(zk)

def rmse(xk, xk_prime):
    xk = np.array(xk)
    xk_prime = np.array(xk_prime)
    return np.sqrt(np.mean(np.square(xk - xk_prime)))


np.random.seed(0)
vk = math.sqrt(10)
nk = math.sqrt(1)

def run_pf(N, k, vk, nk, fn):
    particles, weights = get_initial_particles(N)
    ground_truth = [0]
    estimates = [0]

    for k in range(1, 75):
        ground_truth.append(f(ground_truth[-1], k, vk))
        zk = get_measurement(ground_truth[-1], nk)
        particles = predict(particles, k, vk)
        weights = update(particles, weights, zk, nk)

        # print(f"Ground truth: {ground_truth}")
        # print(f"Estimate: {estimate(particles, weights)}")
        estimates.append(estimate(particles, weights))
        # print(f"RMSE: {rmse(ground_truth, estimates)}")

        # idx = np.random.choice(N, 100)
        # plt.scatter(np.ones(100)*k, particles[idx], c=weights[idx], s=7)

        if neff(weights) < 0.5*N:
            # print(k, "Resample")
            particles, weights = resample(particles, weights, fn=fn)

    print(f"RMSE: {rmse(ground_truth, estimates)}")
    return rmse(ground_truth, estimates)

    # plt.plot(np.arange(len(ground_truth)), ground_truth, c="green")
    # plt.plot(np.arange(len(ground_truth)), estimates, c="orange")

    # plt.show()


N = 1000
k = 75

mean_rmse = []
for _ in range(100):
    r = run_pf(N, k, vk, nk, multinomial_resample)
    mean_rmse.append(r)

print(np.mean(mean_rmse))