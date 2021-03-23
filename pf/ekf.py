import math
import numpy as np
import scipy
import scipy.stats
import matplotlib.pyplot as plt

def f(xk, uk):
    return xk + np.cos(uk)

# def f(xk, uk):
    # return xk + 1

def h(xk):
    return (xk**2)/20

def fj(xk, uk):
    return np.array([1.0])

def hj(xk):
    return np.array([xk/10.0])

def predict(xk, uk, P, Q):
    F = fj(xk, uk)
    xk = f(xk, uk)
    P = F @ P @ F.T + Q
    return xk, P, Q

def update(xk, zk, P, Q, R):
    H = hj(xk)
    y = np.array([zk - h(xk)])

    S = (H @ P @ H.T) + R
    K = P @ H.T @ np.linalg.pinv(S)
    xk += K @ y
    P = (np.eye(1) - K @ H) @ P

    return xk, P


ground = [0]
est = [0]
var = [1]
# vk = math.sqrt(10)
# nk = math.sqrt(1)
P = np.eye(1)
Q = np.eye(1)
R = np.eye(1)

np.random.seed(4)
vk = np.random.normal(0, math.sqrt(10), 99)
nk = np.random.normal(0, math.sqrt(1), 99)


for k in range(1, 100):
    # w = np.random.normal(0, vk)
    # v = np.random.normal(0, nk)

    ground.append(f(ground[-1], k) + vk[k-1])
    z = h(ground[-1]) + nk[k-1]

    x, P, Q = predict(est[-1], k, P, Q)
    x, P = update(x, z, P, Q, R)
    var.append(P[0])

    est.append(x)


fig, ax = plt.subplots(figsize=(12, 6))

# ax.plot(var)
ax.plot(np.arange(len(ground)), ground, c="red")
ax.plot(np.arange(len(est)), est, c="fuchsia")
ax.legend(["Ground truth", "Filter estimate"])
plt.show()

