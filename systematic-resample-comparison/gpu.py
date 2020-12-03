import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.autoinit import context
from pycuda.driver import limit
import matplotlib.pyplot as plt
from cuda_load import load_cuda_modules
import math


def systematic_resample_parallel(weights, rand):
    N = weights.shape[0]
    indices = np.zeros(N, dtype=np.int32)
    cumsum = np.cumsum(weights)

    for k in range(N):
        left = math.ceil(((cumsum[k] - weights[k]) * N) - rand)
        right = math.ceil((cumsum[k] * N) - rand)

        # print("cpu", left, right, (cumsum[k] - weights[k]) * N, (cumsum[k] * N))

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


def is_power(n):
    return (n & (n-1) == 0) and n != 0

# def cumsum_prepare(N, THREADS_PER_BLOCK):
#     assert is_power(N)
#     assert is_power(THREADS_PER_BLOCK)

#     block_size = 2 * THREADS_PER_BLOCK
#     smem = block_size
    
#     if N <= block_size:
#         nthreads = N//2
#         nblocks = 1
#         smem = N
#     else:
#         nthreads = THREADS_PER_BLOCK
#         nblocks = N//block_size
#         smem = block_size
    
#     cuda_d_in = cuda.mem_alloc(4 * N)
#     cuda_d_scan = cuda.mem_alloc(4 * N)

#     cuda_d_sums = cuda.mem_alloc(4 * nblocks)
#     cuda_d_incr = cuda.mem_alloc(4 * nblocks)


#     return cuda_d_in, cuda_d_scan, cuda_d_sums, cuda_d_incr


def compute_cumsum(modules, weights, THREADS_PER_BLOCK):
    N = weights.shape[0]

    assert is_power(N)
    assert is_power(THREADS_PER_BLOCK)
    
    block_size = 2 * THREADS_PER_BLOCK
    smem = block_size
    
    if N <= block_size:
        nthreads = N//2
        nblocks = 1
        smem = 8*N
    else:
        nthreads = THREADS_PER_BLOCK
        nblocks = N//block_size
        smem = 8*block_size

    print(nblocks, nthreads)

    # cuda_d_in = cuda.mem_alloc(4 * N)
    # cuda_d_scan = cuda.mem_alloc(4 * N)

    # cuda_d_sums = cuda.mem_alloc(4 * nblocks)
    # cuda_d_incr = cuda.mem_alloc(4 * nblocks)

    # cuda.memcpy_htod(cuda_d_in, weights)


    if nblocks == 1:
        modules["cumsum"].get_function("block_scan")(
            cuda_d_in, cuda_d_scan, cuda_d_sums,
            np.int32(N), np.int32(0),
            grid=(1, 1, 1), block=(nthreads, 1, 1), shared=smem
        )

    else:
        modules["cumsum"].get_function("block_scan")(
            cuda_d_in, cuda_d_scan, cuda_d_sums,
            np.int32(block_size), np.int32(1),
            grid=(nblocks, 1, 1), block=(nthreads, 1, 1), shared=smem
        )

        modules["cumsum"].get_function("block_scan")(
            cuda_d_sums, cuda_d_incr, cuda_d_incr,
            np.int32(nblocks), np.int32(0),
            grid=(1, 1, 1), block=(nblocks//2, 1, 1), shared=smem
        )

        modules["cumsum"].get_function("add_partial_sums")(
            cuda_d_scan, cuda_d_incr,
            grid=(nblocks, 1, 1), block=(nthreads, 1, 1)
        )


    # cumsum = np.zeros(N, dtype=np.float32)
    # cuda.memcpy_dtoh(cumsum, cuda_d_scan)
    # return cumsum


if __name__ == "__main__":
    context.set_limit(limit.MALLOC_HEAP_SIZE, 100000 * 1024 * 15)
    timings = []
    N = 524288 * 2
    THREADS_PER_BLOCK = 1024
    cuda_modules = load_cuda_modules()


    assert is_power(N)
    assert is_power(THREADS_PER_BLOCK)
    
    block_size = 2 * THREADS_PER_BLOCK
    smem = block_size
    
    if N <= block_size:
        nthreads = N//2
        nblocks = 1
        smem = 8*N
    else:
        nthreads = THREADS_PER_BLOCK
        nblocks = N//block_size
        smem = 8*block_size

    
    # cuda_d_in = cuda.mem_alloc(8 * N)
    cuda_d_scan = cuda.mem_alloc(8 * N)
    # cuda_d_sums = cuda.mem_alloc(8 * nblocks)
    # cuda_d_incr = cuda.mem_alloc(8 * nblocks)


    # cuda_d_in, cuda_d_scan, cuda_d_sums, cuda_d_incr = cumsum_prepare(N, THREADS_PER_BLOCK)
    cuda_weights = cuda.mem_alloc(8 * N)
    # cuda_cumsum = cuda.mem_alloc(8 * N)
    cuda_indices = cuda.mem_alloc(8 * N)
    indices = np.zeros(N, dtype=np.int32)


    cuda_modules["resample"].get_function("init_rng")(
        np.int32(0),
        block=(1, 1, 1)
    )

    np.random.seed(0)
    for _ in range(10):
        weights = np.abs(np.random.normal(0, 1, N).astype(np.float64))
        weights /= np.sum(weights)

        # print("AVERAGE:", np.mean(weights))

        cumsum = np.cumsum(weights)
        exclusive_cumsum = np.zeros(N+1, dtype=np.float64)
        exclusive_cumsum[1:] = cumsum
        exclusive_cumsum = exclusive_cumsum[:-1]
        cuda.memcpy_htod(cuda_d_scan, exclusive_cumsum)


        # cuda.memcpy_htod(cuda_d_in, weights)
        cuda.memcpy_htod(cuda_weights, weights)


        start = cuda.Event()
        end = cuda.Event()
        start.record()

        # compute_cumsum(cuda_modules, weights, THREADS_PER_BLOCK)

        rand = 0.2

        
        # cuda_modules["resample"].get_function("systematic")(
        #     cuda_weights, cuda_d_scan, np.int32(N), np.float32(rand), cuda_indices,
        #     block=(THREADS_PER_BLOCK, 1, 1)
        # )

        cuda_modules["resample"].get_function("init_rng")(
            np.int32(N), np.int32(THREADS_PER_BLOCK),
            block=(THREADS_PER_BLOCK, 1, 1)
        )

        cuda_modules["resample"].get_function("stratified")(
            cuda_weights, cuda_d_scan, np.int32(N), np.int32(THREADS_PER_BLOCK), cuda_indices,
            block=(THREADS_PER_BLOCK, 1, 1)
        )

        end.record()
        end.synchronize()
        timings.append(start.time_till(end))

        cuda.memcpy_dtoh(indices, cuda_indices)

        # print(indices)
        # print(systematic_resample(weights, rand))
        # print("Differences", np.sum(indices != systematic_resample(weights, rand)))

        # plt.plot(np.arange(N), indices)
        # plt.plot(np.arange(N), systematic_resample(weights, rand))
        # plt.show()

        # cumsum32 = np.zeros(N, dtype=np.float64)
        # cuda.memcpy_dtoh(cumsum32, cuda_d_scan)
        # cumsum32 = cumsum32.astype(np.float64)

        # plt.plot(np.arange(N), exclusive_cumsum - cumsum32)
        # plt.show()

        # print(systematic_resample_parallel(weights, rand))

        # print(np.array_equal(indices, systematic_resample(weights, rand)))
        # print(np.array_equal(indices, systematic_resample_parallel(weights, rand)))



    print(f"{N}: {np.mean(timings)/1000}")





