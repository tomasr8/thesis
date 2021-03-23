import numpy as np

def systematic_resample(weights):
    N = weights.shape[0]

    # make N subdivisions, and choose positions with a consistent random offset
    positions = (np.random.random() + np.arange(N)) / N

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




print(systematic_resample(np.random.normal(size=100)))
print(systematic_resample(np.random.normal(size=100)))
print(systematic_resample(np.random.normal(size=100)))
print(systematic_resample(np.random.normal(size=100)))
print(systematic_resample(np.random.normal(size=100)))
