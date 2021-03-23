import math
import time
import numpy as np
import matplotlib.pyplot as plt


import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import pycuda.autoinit
from pycuda.autoinit import context
from pycuda.driver import limit

def is_valid_permutation(ancestors):
    N = len(ancestors)
    offsprings = [0] * N

    for a in ancestors:
        offsprings[a] += 1

    for i in range(N):
        if offsprings[i] > 0 and ancestors[i] != i:
            return False

    return True


if __name__ == "__main__":
    context.set_limit(limit.MALLOC_HEAP_SIZE, 100000 * 1024)  # heap size available to the GPU threads

    with open("permute.cu") as f:
        source = f.read()

    cuda_permute = SourceModule(source)
    N = 8192
    THREADS = 1024
    cuda_ancestors = cuda.mem_alloc(4 * N)
    cuda_aux = cuda.mem_alloc(4 * N)
    np.random.seed(0)

    for _ in range(1):
        ancestors = np.random.randint(0, N/4, size=N)
        ancestors = np.sort(ancestors).astype(np.int32)

    # ancestors = [0, 0, 5, 1, 2, 2, 7, 8, 7, 5]
    # ancestors = np.sort(ancestors).astype(np.int32)
    # N = len(ancestors)

        cuda.memcpy_htod(cuda_ancestors, ancestors)

        cuda_permute.get_function("reset")(
            cuda_aux,
            block=(THREADS, 1, 1), grid=(N//THREADS, 1, 1)
        )

        cuda_permute.get_function("compute_positions")(
            cuda_ancestors,
            cuda_aux,
            block=(THREADS, 1, 1), grid=(N//THREADS, 1, 1)
        )

        cuda_permute.get_function("permute")(
            cuda_ancestors,
            cuda_aux,
            np.int32(N//THREADS), np.int32(N),
            block=(THREADS, 1, 1)
        )

        result = np.zeros(N, dtype=np.int32)
        cuda.memcpy_dtoh(result, cuda_ancestors)
        print(is_valid_permutation(result))
        print(np.array_equal(ancestors, np.sort(result)))