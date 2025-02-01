from __future__ import annotations

import re
from typing import Any

import numpy as np
import pytest

import pigreads as pig


def test_structure():
    "Check that the model metadata structured correctly."
    assert isinstance(pig.models(), str)

    models = pig.Models()

    assert isinstance(models.available, dict)
    for name, model in models.available.items():
        assert isinstance(name, str)
        assert isinstance(model, dict)
        for key in model:
            assert isinstance(key, str)
        assert isinstance(model["id"], int)
        assert isinstance(model["name"], str)
        assert isinstance(model["description"], str)
        assert isinstance(model["dois"], list)
        for doi in model["dois"]:
            assert isinstance(doi, str)
            assert re.match(r"^https://doi.org/10\.", doi)
        for dictname in ["variables", "parameters"]:
            assert isinstance(model[dictname], dict)
            for varname, value in model[dictname].items():
                assert isinstance(varname, str)
                assert isinstance(value, (float, int))


def test_data_double():
    assert pig._core.models() == pig._core_double.models()


def test_str():
    pig.Models("marcotte2017dynamical")


def test_info():
    models = pig.Models()
    key = "marcotte2017dynamical"
    assert models.available[key] == models.info(key)


def test_info_empty():
    models = pig.Models()
    with pytest.raises(KeyError):
        models.info("")


def test_add():
    key = "marcotte2017dynamical"
    models = pig.Models(
        [
            (key, {}),
            (key, {"eps": 1}),
        ]
    )
    models.add(key)
    models.add(key, eps=2)
    assert models[0] == models.info(key)
    assert models[0] == models[2]
    assert models[1]["parameters"]["eps"] == 1
    assert models[3]["parameters"]["eps"] == 2


def test_Nv():
    key = "marcotte2017dynamical"
    models = pig.Models()
    models.add(key)
    assert models.Nv == 2


def test_resting_states():
    models = pig.Models()
    models.add("gray1983autocatalytic")
    models.add("courtemanche1998ionic")
    inhom = np.array([[[0, 1], [2, 3]]], dtype=int)
    states = models.resting_states(inhom, Nframes=2)
    assert states.shape == (2, *inhom.shape, models.Nv)
    assert np.all(np.isnan(states[0, 0, 0, 0, :]))
    assert np.all(np.isnan(states[:, inhom == 0, :]))
    assert states[0, 0, 0, 1, 0] == 1
    assert states[0, 0, 0, 1, 1] == 0
    assert abs(-81.18 - states[0, 0, 1, 0, 0]) < 1e-6
    assert abs(0.002908 - states[0, 0, 1, 0, 1]) < 1e-6
    assert states[0, 0, 1, 1, 0] == 1
    assert states[0, 0, 1, 1, 1] == 0
    assert np.allclose(states[1, inhom != 0, :], 0)


def test_array():
    models = pig.Models()
    models.add("marcotte2017dynamical", eps=2)
    models.add("gray1983autocatalytic")
    a = models.array
    assert a.ndim == 1
    assert a.shape[0] == 11
    assert a[0] == models[0]["id"]
    assert a[6] == models[1]["id"]
    assert np.allclose(a[1:6], [4.0062, 0.20031, 1.389, 2.0, 1.5415])
    assert np.allclose(a[7:], [1.0, 0.5, 0.055, 0.062])


def test_sim0d():
    z, y, x = np.mgrid[0:1, 0:3, 0:3]
    dz, dy, dx = pig.deltas(z, y, x)
    inhom = np.ones_like(x, dtype=int)

    for modelname in pig.Models().available:
        models = pig.Models(modelname)
        states: np.ndarray[Any, Any] = models.resting_states(inhom, Nframes=2).astype(
            np.float32
        )
        weights = pig.weights(dz, dy, dx, inhom, diffusivity=0)
        states[1] = pig.run(models, inhom, weights, states[0], Nt=2, dt=1e-10)
