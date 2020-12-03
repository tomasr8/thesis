import numpy as np
import math

def stratified_resample_parallel(weights):
    N = weights.shape[0]
    indices = np.zeros(N, dtype=np.int32)
    cumsum = np.cumsum(weights)
    cumsum[-1] = 1.0

    rand = np.random.uniform(0, 1, N)

    for k in range(N):
        # rand = np.random.uniform()
        left = math.ceil(((cumsum[k] - weights[k]) * N) - rand[math.floor((cumsum[k] - weights[k]) * N)])

        if k == N-1:
            right = N
        else:
            right = math.ceil(((cumsum[k]) * N) - rand[math.floor(cumsum[k] * N)])

        print(k, math.floor((cumsum[k] - weights[k]) * N), math.floor(cumsum[k] * N))

        # print(left, right)

        for j in range(left, right):
            indices[j] = k

    return indices



def stratified_resample(weights):
    N = weights.shape[0]
    positions = (np.random.uniform(0, 1, N) + range(N)) / N

    indexes = np.zeros(N, dtype=np.int32)
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1.0

    i, j = 0, 0
    while i < N:
        if positions[i] < cumulative_sum[j]:
            # print(i, j)
            indexes[i] = j
            i += 1
        else:
            j += 1
    return indexes


def systematic_resample_parallel(weights, rand):
    N = weights.shape[0]
    indices = np.zeros(N, dtype=np.int32)
    cumsum = np.cumsum(weights)

    for k in range(N):
        left = math.ceil(((cumsum[k] - weights[k]) * N) - rand)
        right = math.ceil((cumsum[k] * N) - rand)

        for j in range(left, right):
            indices[j] = k

    return indices


def systematic_resample(weights, rand):
    N = weights.shape[0]

    # make N subdivisions, and choose positions with a consistent random offset
    positions = (rand + np.arange(N)) / N

    indexes = np.zeros(N, dtype=np.int32)
    cumulative_sum = np.cumsum(weights)
    # prevent float imprecision
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
    # np.random.seed(1)
    N = 50
    weights = np.abs(np.random.normal(0, 1, N).astype(np.float64))
    weights /= np.sum(weights)

    np.random.seed(0)
    indices1 = stratified_resample(weights)

    np.random.seed(0)
    indices2 = stratified_resample_parallel(weights)

    print(indices1)
    print(indices2)
    print(np.array_equal(indices1, indices2))

    print(systematic_resample_parallel(weights, 0.1))
