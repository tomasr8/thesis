import numpy as np
from collections import defaultdict
import time

def is_valid_permutation(ancestors):
    N = len(ancestors)
    offsprings = [0] * N

    for a in ancestors:
        offsprings[a] += 1

    for i in range(N):
        if offsprings[i] > 0 and ancestors[i] != i:
            return False

    return True


def permute(ancestors):
    N = len(ancestors)
    aux = [-1] * N

    for i in range(N):
        aux[ancestors[i]] = i

    for i, a in enumerate(ancestors):
        if a == i:
            continue

        pos = aux[i]
        if pos != -1:
            aux[ancestors[i]], aux[ancestors[pos]] = aux[ancestors[pos]], aux[ancestors[i]]
            ancestors[i], ancestors[pos] = ancestors[pos], ancestors[i]

    return ancestors


def permute2(ancestors):
    N = len(ancestors)
    aux = [-1] * N

    for i in range(N):
        aux[ancestors[i]] = i

    for i, a in enumerate(ancestors):
        if a == i:
            continue

        j = i
        while aux[j] != -1:
            pos = aux[j]
            elem = ancestors[pos]

            aux[ancestors[j]], aux[ancestors[pos]] = aux[ancestors[pos]], aux[ancestors[j]]
            ancestors[j], ancestors[pos] = ancestors[pos], ancestors[j]

            j = pos

    return ancestors


def needs_swap(ancestors, aux, i):
    a = ancestors[i]
    return a != i and aux[i] != -1

def is_end(ancestors, aux, i):
    a = ancestors[i]
    return ancestors[a] == a or aux[a] != i

def permute3(ancestors):
    N = len(ancestors)
    aux = [-1] * N

    for i in range(N):
        aux[ancestors[i]] = i

    print(aux)
    # for i in range(N):
    #     print(i, is_end(ancestors, aux, i))

    for i in range(N):
        if is_end(ancestors, aux, i):
            # print(i)
            j = i
            while needs_swap(ancestors, aux, j):
                pos = aux[j]
                print(i, "swapping", j, pos, ancestors[j], ancestors[pos])

                aux[ancestors[j]], aux[ancestors[pos]] = aux[ancestors[pos]], aux[ancestors[j]]
                ancestors[j], ancestors[pos] = ancestors[pos], ancestors[j]

                j = pos

            # print(ancestors)


    return ancestors


def permute4(ancestors):
    N = len(ancestors)
    aux = [-1] * N

    for i in range(N):
        aux[ancestors[i]] = i

    # print(aux)
    # for i in range(N):
    #     print(i, is_end(ancestors, aux, i))

    for i in range(N):
        if is_end(ancestors, aux, i):
            # print(i)
            j = i
            while needs_swap(ancestors, aux, j):
                pos = aux[j]
                # print(i, "swapping", j, pos)

                if aux[ancestors[j]] == j:
                    # print(ancestors[j], ancestors[j], "<-", pos)
                    aux[ancestors[j]] = pos

                if aux[ancestors[pos]] == pos:
                    # print(ancestors[pos], ancestors[pos], "<-", j)
                    aux[ancestors[pos]] = j

                # aux[ancestors[j]], aux[ancestors[pos]] = aux[ancestors[pos]], aux[ancestors[j]]
                ancestors[j], ancestors[pos] = ancestors[pos], ancestors[j]

                j = pos

            # print(ancestors)


    return ancestors

# ancestors = [0, 2, 3, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 11, 12]
# ancestors = np.sort(ancestors)
# print(ancestors)
# # print(is_valid_permutation(ancestors))

# permutation = permute4(ancestors[:])
# print(permutation)
# print(is_valid_permutation(permutation))

np.random.seed(1)
N = 10000
ancestors = np.random.randint(0, N/4, size=N)
ancestors = np.sort(ancestors)
# print(ancestors)
print(is_valid_permutation(ancestors))

# aux = [-1] * N
start = time.time()

permutation = permute4(np.copy(ancestors))
# print(permutation)
print(time.time() - start)
print(is_valid_permutation(permutation))

# print(np.sort(permutation))
# print(np.sum(ancestors), np.sum(permutation))


print(np.array_equal(ancestors, np.sort(permutation)))
# print(ancestors == np.sort(permutation))
# print(ancestors)
# print(np.sort(permutation))
