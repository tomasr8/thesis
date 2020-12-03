import numpy as np
import time
import math
import matplotlib.pyplot as plt

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


def systematic_resample(weights, type, rand):
    N = weights.shape[0]

    rand = type(rand)
    positions = ((rand + np.arange(N).astype(type)) / N).astype(type)

    # positions = (np.random.uniform() + np.arange(N)) / N
    # positions = positions

    indexes = np.zeros(N, dtype=np.int32)
    cumulative_sum = np.cumsum(weights)
    # cumulative_sum[-1] = 1.0

    i, j = 0, 0
    while i < N:
        if j == N:
            break

        if positions[i] < cumulative_sum[j]:
            indexes[i] = j
            i += 1
        else:
            j += 1
    return indexes


def to_offspring(indices):
    N = indices.shape[0]
    offsprings = np.zeros(N, dtype=np.int32)

    for index in indices:
        offsprings[int(index)] += 1

    return offsprings


if __name__ == "__main__":

    MSE = {}

    sizes = [2**i for i in range(20, 21)]

    np.random.seed(18)
    for N in sizes:
        MSE[N] = []
        for _ in range(1):
            print(N)
            weights = np.abs(np.random.normal(0, 1, N).astype(np.float64))
            weights /= np.sum(weights)

            cumsum32 = np.cumsum(weights.astype(np.float32)).astype(np.float64)
            cumsum64 = np.cumsum(weights.astype(np.float64)).astype(np.float64)

            # print(np.mean(weights))

            # plt.plot(np.arange(N), cumsum32)
            # plt.plot(np.arange(N), cumsum64)

            # plt.plot(np.arange(N), cumsum64 - cumsum32)
            # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            # plt.show()

            rand = np.random.uniform()

            indices32 = systematic_resample(weights.astype(np.float32), np.float32, rand).astype(np.float64)
            indices64 = systematic_resample(weights.astype(np.float64), np.float64, rand).astype(np.float64)

            # indices32 = systematic_resample_parallel(weights.astype(np.float32), np.float32(rand)).astype(np.float64)
            # indices64 = systematic_resample_parallel(weights.astype(np.float64), np.float64(rand)).astype(np.float64)

            offsprings32 = to_offspring(indices32)
            offsprings64 = to_offspring(indices64)

            # mse = np.sum(np.square(offsprings32 - offsprings64)) / N
            # print("mse", mse)
            # MSE[N].append(mse)

            # plt.plot(np.arange(N), offsprings32, linewidth=1.0)
            # plt.plot(np.arange(N), offsprings64, alpha=0.9, linewidth=0.5)
            # plt.show()

            fig, ax = plt.subplots(2)
            ax[0].plot(np.arange(N), cumsum64 - cumsum32, color="#5c5c5c", linewidth=1.0)
            ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            # ax[1].set_xlabel("Weights")

            ax[1].plot(np.arange(N), offsprings32, linewidth=1.0)
            ax[1].plot(np.arange(N), offsprings64, alpha=0.9, linewidth=0.5)
            ax[1].legend(["Single precision", "Double precision"], loc='upper right')

            # fig.ylabel("")
 
            fig.tight_layout()
            plt.show()



    # for N in MSE:
    #     print(f"{N}: {np.mean(MSE[N])}")

    # plt.plot(sizes, [np.mean(MSE[N]) for N in MSE])
    # plt.show()



