import numpy as np
from collections import defaultdict

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

    print(aux)

    # out = ancestors[:]

    for i, a in enumerate(ancestors):
        if a == i:
            continue

        # if aux[i] == -2:
        #     continue

        print("looking for", i, aux[i])

        pos = aux[i]
        if pos != -1:
            elem = ancestors[pos]
            print(f"swapping {i} {pos}")

            # aux[elem] = i
            ancestors[i], ancestors[pos] = ancestors[pos], ancestors[i]

    return ancestors


ancestors = [0, 0, 5, 1, 2, 2, 7, 8, 7, 5]

print(is_valid_permutation(ancestors))

permutation = permute(ancestors[:])
print(ancestors)
print(permutation)
print(is_valid_permutation(permutation))