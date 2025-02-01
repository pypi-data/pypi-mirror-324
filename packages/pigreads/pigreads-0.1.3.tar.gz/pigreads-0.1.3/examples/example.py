#!/bin/env python3
"""
Run a simulation
"""

from __future__ import annotations

import sys
from pathlib import Path

import ithildin as ith
import numpy as np

import pigreads as pig


def main():
    random = np.random.default_rng(seed=0)

    R = 11.05
    z, y, x = np.mgrid[0:1, -R:R:200j, -R:R:200j]
    dz, dy, dx = pig.deltas(z, y, x)
    r = np.linalg.norm((x, y, z), axis=0)

    inhom = np.ones_like(x, dtype=int)
    inhom[r > R] = 0
    inhom *= random.uniform(0, 1, size=x.shape) > 0.1

    models = pig.Models()
    models.add("marcotte2017dynamical", diffusivity_u=1.0, diffusivity_v=0.05)

    states = models.resting_states(inhom, Nframes=100)
    states[0, np.linalg.norm(((x + 8), y, z), axis=0) < 2, 0] = 1
    states[0, y < 0, 1] = 2

    diffusivity = pig.diffusivity_matrix(Df=0.03)

    weights = pig.weights(dz, dy, dx, inhom, diffusivity)

    Nt = 200
    dt = 0.025
    for it in range(states.shape[0] - 1):
        states[it + 1] = pig.run(models, inhom, weights, states[it], Nt=Nt, dt=dt)

    # plot data with Matplotlib
    import matplotlib.pyplot as plt

    plt.imshow(states[-1, 0, :, :, 0])
    plt.show()

    # write to disk via Ithildin
    log, variables = pig.to_ithildin(Nt * dt, dt, dz, dy, dx, models, states, inhom)
    sd = ith.SimData(log=ith.Log(data=log))
    sd.vars = variables
    sd.to_npz("results/" + Path(sys.argv[0]).stem + ".npz")


if __name__ == "__main__":
    main()
