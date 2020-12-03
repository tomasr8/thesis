#include <float.h>

/**
 * Exclusive prefix sum implementation
 * Requires that the length of the data is a power of 2 and
 * the number of threads in a block is also a power of 2.
 * Otherwise it will access illegal memory.
 */
__global__ void block_scan(double *input, double *output, double *block_sums, int n, int save_block_sums) {
    extern __shared__ double shared_mem[];
    const int bx = blockIdx.x * blockDim.x;
    const int tx = threadIdx.x;
    const int px = bx + tx;
    int offset = 1;

    // copy everything to shared memory
    // every thread copies two values
    shared_mem[2*tx]   = input[2*px];
    shared_mem[2*tx+1] = input[2*px+1];

    ////
    // up sweep
    ////
    for (int d = n >> 1; d > 0; d >>= 1) {
        __syncthreads();

        if (tx < d) {
            int ai = offset * (2*tx+1) - 1;
            int bi = offset * (2*tx+2) - 1;

            shared_mem[bi] += shared_mem[ai];
        }
        offset <<= 1;
    }

    if (tx == 0) {
        if (save_block_sums == 1) {
            // save block sum if we run in multiple blocks
            block_sums[blockIdx.x] = shared_mem[n-1];
        }
        // clear last element
        shared_mem[n-1] = 0;
    }

    ////
    // down sweep
    ////
    for (int d = 1; d < n; d <<= 1) {
        offset >>= 1;
        __syncthreads();

        if (tx < d) {
            int ai = offset * (2*tx+1) - 1;
            int bi = offset * (2*tx+2) - 1;

            // swap
            double t = shared_mem[ai];
            shared_mem[ai]  = shared_mem[bi];
            shared_mem[bi] += t;
        }
    }
    __syncthreads();

    // save scan result
    output[2*px]   = shared_mem[2*tx];
    output[2*px+1] = shared_mem[2*tx+1];
}

// __global__ void block_scan_32(float *input, float *output, float *block_sums, int n, int save_block_sums) {
//     extern __shared__ float shared_mem[];
//     const int bx = blockIdx.x * blockDim.x;
//     const int tx = threadIdx.x;
//     const int px = bx + tx;
//     int offset = 1;

//     // copy everything to shared memory
//     // every thread copies two values
//     shared_mem[2*tx]   = input[2*px];
//     shared_mem[2*tx+1] = input[2*px+1];

//     ////
//     // up sweep
//     ////
//     for (int d = n >> 1; d > 0; d >>= 1) {
//         __syncthreads();

//         if (tx < d) {
//             int ai = offset * (2*tx+1) - 1;
//             int bi = offset * (2*tx+2) - 1;

//             shared_mem[bi] += shared_mem[ai];
//         }
//         offset <<= 1;
//     }

//     if (tx == 0) {
//         if (save_block_sums == 1) {
//             // save block sum if we run in multiple blocks
//             block_sums[blockIdx.x] = shared_mem[n-1];
//         }
//         // clear last element
//         shared_mem[n-1] = 0;
//     }

//     ////
//     // down sweep
//     ////
//     for (int d = 1; d < n; d <<= 1) {
//         offset >>= 1;
//         __syncthreads();

//         if (tx < d) {
//             int ai = offset * (2*tx+1) - 1;
//             int bi = offset * (2*tx+2) - 1;

//             // swap
//             float t = shared_mem[ai];
//             shared_mem[ai]  = shared_mem[bi];
//             shared_mem[bi] += t;
//         }
//     }
//     __syncthreads();

//     // save scan result
//     output[2*px]   = shared_mem[2*tx];
//     output[2*px+1] = shared_mem[2*tx+1];
// }


__global__ void add_partial_sums(double *output, double *block_sums) {
    const size_t bx = 2 * blockDim.x * blockIdx.x;
    const size_t tx = threadIdx.x;
    double block_sum = block_sums[blockIdx.x];

    output[bx + 2*tx]   += block_sum;
    output[bx + 2*tx+1] += block_sum;
}

// __global__ void add_partial_sums_32(float *output, float *block_sums) {
//     const size_t bx = 2 * blockDim.x * blockIdx.x;
//     const size_t tx = threadIdx.x;
//     float block_sum = block_sums[blockIdx.x];

//     output[bx + 2*tx]   += block_sum;
//     output[bx + 2*tx+1] += block_sum;
// }


// __global__ void block_psum_mine(
//     float *g_in, float *g_out, int n)
// {
//     extern __shared__ float smem[];
//     const int tx = threadIdx.x;
//     int offset = 1;

//     int old_n = n;

    
//     if(old_n % 2 == 0) {
//         if(tx < old_n/2) {
//             smem[2*tx]   = g_in[2*tx];
//             smem[2*tx+1] = g_in[2*tx+1];
//         }
//     } else {
//         if(tx < old_n/2) {
//             smem[2*tx]   = g_in[2*tx];
//             smem[2*tx+1] = g_in[2*tx+1];
//         } else if(tx == old_n/2) {
//             smem[2*tx]   = g_in[2*tx];
//             smem[2*tx+1]   = 0;
//         }
//     }

//     if (tx == 0) {
//         for(int i = 0; i < old_n; i++) {
//             printf("%d: %f\,", i, smem[i]);
//         }
//         printf("\n");
//     }

//     // init

//     if(n % 2 != 0) {
//         n++;
//     }

//     ////
//     // up sweep
//     ////
//     for (int d = n >> 1; d > 0; d >>= 1) {
//         __syncthreads();

//         if (tx < d) {
//             int ai = offset * (2*tx+1) - 1;
//             int bi = offset * (2*tx+2) - 1;

//             printf("%d: %d, %d\n", d, ai, bi);

//             smem[bi] += smem[ai];
//         }
//         offset <<= 1;
//     }

//     // save block sum and clear last element
//     if (tx == 0) {
//         for(int i = 0; i < n; i++) {
//             printf("%d: %f\,", i, smem[i]);
//         }
//         printf("\n");
//         smem[n-1] = 0;
//     }

//     ////
//     // down sweep
//     ////
//     for (int d = 1; d < n; d <<= 1) {
//         offset >>= 1;
//         __syncthreads();

//         if (tx < d) {
//             int ai = offset * (2*tx+1) - 1;
//             int bi = offset * (2*tx+2) - 1;

//             printf("%d> %d, %d\n", offset, tx);
//             printf("%d: %d, %d\n", d, ai, bi);

//             // swap
//             printf("%d swapping %d %d\n", d, ai, bi);
//             printf("%d swapping %d %d\n", d, offset, tx);
//             float t = smem[ai];
//             smem[ai]  = smem[bi];
//             smem[bi] += t;
//         }

//         printf("%d here\n", d);
//     }
//     __syncthreads();

//     if(old_n % 2 == 0) {
//         if(tx < old_n/2) {
//             g_out[2*tx]   = smem[2*tx];
//             g_out[2*tx+1] = smem[2*tx+1];
//         }
//     } else {
//         if(tx < old_n/2) {
//             g_out[2*tx]   = smem[2*tx];
//             g_out[2*tx+1] = smem[2*tx+1];
//         } else if(tx == n/2) {
//             g_out[2*tx]   = smem[2*tx];
//         }
//     }
// }