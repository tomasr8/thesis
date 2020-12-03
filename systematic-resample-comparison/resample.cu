#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <curand_kernel.h>

#define THREADS 1048576

extern "C" {
// __device__ curandState_t* states[THREADS];
__device__ double r[THREADS];
__device__ curandState_t *state;

/**
 * Parallel Systematic Resample
 * Requires cumsum to be an exclusive cumsum i.e. start with 0.
 *
 * Uses double precision to prevent imprecision of floats for higher values of n.
 */
__global__ void systematic(double *weights, double *cumsum, int n, int threads, double rand, int *indices) {
    int block_id = blockIdx.x + blockIdx.y * gridDim.x;
    int idx = block_id * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x;

    int left;
    int right;
    for (int k = idx; k < n; k += threads) {
        left = (int)ceil(((cumsum[k]) * n) - rand);
        right = (int)ceil(((cumsum[k] + weights[k]) * n) - rand);

        for(int j = left; j < right; j++) {
            indices[j] = k;
        }
    }
}

__global__ void init_rng(int seed)
{

    state = new curandState_t;
    curand_init(seed, 0, 0, state);

    // int block_id = blockIdx.x + blockIdx.y * gridDim.x;
    // int idx = block_id * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x;
    
    // // for (int k = idx; k < THREADS; k += 1024) {
    // curandState_t* s = new curandState_t;
    // curand_init(seed, idx, 0, s);
    // double u = (double)curand_uniform(s);
    // r[idx] = u;
    // }
}

__global__ void draw_uniform(int n, int threads)
{

    int block_id = blockIdx.x + blockIdx.y * gridDim.x;
    int idx = block_id * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x;

    for (int k = idx; k < n; k += threads) {
        double u = (double)curand_uniform(state);
        r[k] = u;
    }

    
    // // for (int k = idx; k < THREADS; k += 1024) {
    // curandState_t* s = new curandState_t;
    // curand_init(seed, idx, 0, s);
    // double u = (double)curand_uniform(s);
    // r[idx] = u;
    // }
}

__global__ void stratified(double *weights, double *cumsum, int n, int threads, int *indices) {
    int block_id = blockIdx.x + blockIdx.y * gridDim.x;
    int idx = block_id * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x;

    int left;
    int right;
    for (int k = idx; k < n; k += threads) {
        left = ceil(((cumsum[k]) * n) - r[(int)floor((cumsum[k]) * n)]);

        if(k == n-1) {
            right = n;
        } else {
            right = ceil(((cumsum[k] + weights[k]) * n) - r[(int)floor((cumsum[k] + weights[k]) * n)]);
        }

        for(int j = left; j < right; j++) {
            indices[j] = k;
        }
    }
}

}
