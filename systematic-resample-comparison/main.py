import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.autoinit import context
from pycuda.driver import limit

from cuda_load import load_cuda_modules


def cumsum_prepare(N, THREADS_PER_BLOCK):
    nthreads = THREADS_PER_BLOCK
    block_size = 2 * nthreads
    smem = block_size * 4

    if N % block_size == 0:
        n = N
    else:
        n = (1+N//block_size)*block_size

    nblocks = n//block_size

    cuda_d_in = cuda.mem_alloc(4 * N)
    cuda_d_scan = cuda.mem_alloc(4 * n)
    cuda_d_sums = cuda.mem_alloc(4 * nblocks)
    cuda_d_incr = cuda.mem_alloc(4 * nblocks)

    return cuda_d_in, cuda_d_scan, cuda_d_sums, cuda_d_incr


def compute_cumsum(modules, weights, cuda_d_in, cuda_d_scan, cuda_d_sums, cuda_d_incr, THREADS_PER_BLOCK):
    N = weights.shape[0]
    nthreads = THREADS_PER_BLOCK
    block_size = 2 * nthreads
    smem = block_size * 4

    if N % block_size == 0:
        n = N
    else:
        n = (1+N//block_size)*block_size

    nblocks = n//block_size

    cuda.memcpy_htod(cuda_d_in, weights)

    modules["cumsum"].get_function("block_psum")(
        cuda_d_in, cuda_d_scan, cuda_d_sums,
        np.int32(block_size), np.int32(1),
        grid=(nblocks, 1, 1), block=(nthreads, 1, 1), shared=smem
    )


    modules["cumsum"].get_function("block_psum")(
        cuda_d_sums, cuda_d_incr, cuda_d_sums,
        np.int32(block_size), np.int32(0),
        grid=(1, 1, 1), block=(nthreads, 1, 1), shared=smem
    )


    modules["cumsum"].get_function("scatter_incr")(
        cuda_d_scan, cuda_d_incr,
        grid=(nblocks, 1, 1), block=(nthreads, 1, 1)
    )


def compute_resample(modules, cuda_weights, cuda_indices, cuda_cumsum, n, rand, threads):
    modules["resample"].get_function("systematic")(
        cuda_weights, cuda_cumsum, np.int32(n), np.float32(rand), cuda_indices,
        block=(threads, 1, 1)
    )


N = 1024 * 77
THREADS_PER_BLOCK = 1024
cuda_modules = load_cuda_modules(THREADS=THREADS_PER_BLOCK)

weights = np.random.uniform(0, 1, N).astype(np.float32)
weights /= np.sum(weights)

indices = np.zeros(N, dtype=np.float32)
cuda_indices = cuda.mem_alloc(4 * N)
cuda_cumsum = cuda.mem_alloc(4 * N)
cuda.memcpy_htod(cuda_indices, indices)

cuda_d_in, cuda_d_scan, cuda_d_sums, cuda_d_incr = cumsum_prepare(weights.shape[0], THREADS_PER_BLOCK)
compute_cumsum(cuda_modules, weights, cuda_d_in, cuda_d_scan, cuda_d_sums, cuda_d_incr, THREADS_PER_BLOCK)








