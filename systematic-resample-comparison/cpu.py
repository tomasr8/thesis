import numpy as np
import time
import matplotlib.pyplot as plt


def systematic_resample(weights):
    N = weights.shape[0]

    positions = (np.random.uniform() + np.arange(N)) / N

    indexes = np.zeros(N, dtype=np.int32)
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1.0

    i, j = 0, 0
    while i < N:
        if positions[i] < cumulative_sum[j]:
            indexes[i] = j
            i += 1
        else:
            j += 1
    return indexes


if __name__ == "__main__":

    timings = {}

    for N in [2**i for i in range(10, 21)]:
        print(N)
        timings[N] = []
        np.random.seed(0)
        for _ in range(10):
            weights = np.abs(np.random.normal(0, 1, N).astype(np.float64))
            weights /= np.sum(weights)

            start = time.time()
            indices = systematic_resample(weights)
            timings[N].append(time.time() - start)
            
    for N in timings:
        print(f"{N}: {np.mean(timings[N])}")

    plt.plot(list(range(10, 21)), [np.mean(timings[N]) for N in timings])
    plt.show()