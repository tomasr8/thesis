import numpy as np
import time
import matplotlib.pyplot as plt
import json

with open("results.json") as f:
    results = json.load(f)

size = results["size"]

fig, ax = plt.subplots(2)

ax[0].plot(
    np.log2(size),
    [1000*y for y in results["cpu"]],
    marker="o", linestyle="--", fillstyle="none"
)
ax[0].plot(
    np.log2(size),
    [1000*y for y in results["gpu"]],
    marker="o", linestyle="--", fillstyle="none"
)

speedup = [a/b for a, b in zip(results["cpu"], results["gpu"])]
ax[1].plot(np.log2(size), speedup, marker="o", linestyle="--", fillstyle="none", color="black")

plt.show()