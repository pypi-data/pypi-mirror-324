# Pigreads: Python-integrated GPU-enabled reaction diffusion solver
# Copyright (c) 2024 Desmond Kabus. All rights reserved.

"""
Pigreads Python module
----------------------

This Python module is the main interface to set up and run Pigreads simulations
solving the reaction-diffusion equations with OpenCL and NumPy:

.. math::

    \\partial_t \\underline{u}
    =
    \\underline{P} \\nabla \\cdot \\mathbf D \\nabla \\underline{u}
    +
    \\underline{r}(\\underline{u})

for :math:`\\underline{u}(t, \\mathbf x)`, :math:`t\\in[0, T]`, and
:math:`\\mathbf x\\in\\Omega\\subset\\mathbb R^3`, with initial conditions and
no-flux boundary conditions.

The following equations define a simpler example with only two variables,
:math:`\\underline{u} = (u, v)`, with no diffusion in :math:`v`, and
homogeneous and isotropic diffusion:

.. math::

    \\begin{aligned}
    \\partial_t u
    &=
    D \\nabla^2 u
    +
    r_u(u, v)
    \\\\
    \\partial_t v
    &=
    r_v(u, v)
    \\end{aligned}

Pigreads performs the most expensive calculations on graphics cards
using OpenCL, see :py:func:`run` and :py:func:`weights`. Input and output as well
as setting up and interacting with the simulation should be done in Python,
with the exception of adding source terms, so-called stimulus currents.
Pigreads uses the simplistic finite-differences method and forward-Euler time
stepping.

A Pigreads simulation is usually defined in the following steps:
First, define the geometry of the medium. In this example, we use a 2D plane
with 200 points in both x and y::

    import pigreads as pig
    import numpy as np

    R = 11.05
    z, y, x = np.mgrid[0:1, -R:R:200j, -R:R:200j]
    dz, dy, dx = pig.deltas(z, y, x)
    r = np.linalg.norm((x, y, z), axis=0)

Pigreads is optimised for three-dimensional space. For
lower-dimensional simulations, set the number of points in additional
dimensions to one, as done above for the z-dimension.

Calculations are performed at all points with periodic boundary conditions.
The integer field ``inhom`` defines which points are inside (1) the medium and outside (0)::

    inhom = np.ones_like(x, dtype=int)
    inhom[r > R] = 0

Values of inhom larger than zero can be used to select one of multiple models,
i.e., reaction terms :math:`\\underline{r}`. For an ``inhom`` value of 1,
``models[0]`` is used; and ``models[1]`` for a value of 2, etc. One or more of the
available models can be selected using an instance of the :py:class:`Models`
class::

    models = pig.Models()
    models.add("marcotte2017dynamical", diffusivity_u=1.0, diffusivity_v=0.05)

This class also has a function to create an array of the same shape as ``inhom``
in space but for a given number of frames in time. The first frame is filled
with the appropriate resting values for each model. Initial conditions can then
be set in the 0th frame::

    states = models.resting_states(inhom, Nframes=100)
    states[0, np.linalg.norm(((x + 8), y, z), axis=0) < 2, 0] = 1
    states[0, y < 0, 1] = 2

Note that states has five indices, in this order: time, z, y, x, state variable.
This indexing is consistently used in Pigreads and NumPy.

The calculation of the diffusion term :math:`\\underline{P} \\nabla \\cdot
\\mathbf D \\nabla \\underline{u}` is implemented as a weighted sum of neighbouring points.
The weights can be calculated using the function :py:func:`weights`, which also requires the
diffusivity_matrix :math:`D` as input, which is set using :py:func:`diffusivity_matrix`::

    diffusivity = pig.diffusivity_matrix(Df=0.03)
    weights = pig.weights(dz, dy, dx, inhom, diffusivity)

Finally, the simulation can be started using :py:func:`run`, which does ``Nt``
forward-Euler steps and only returns the final states after those steps::

    Nt = 200
    dt = 0.025
    for it in range(states.shape[0] - 1):
        states[it + 1] = pig.run(models, inhom, weights, states[it], Nt=Nt, dt=dt)

Full examples can be found in the ``examples`` folder in the Git repository of
this project.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

import numpy as np
import yaml

from pigreads import _core, _core_double  # pylint: disable=import-self

from ._core import models
from ._version import version as __version__

dtype: type = np.single
cl: _core.OpenCLWrapper | None = None
cl_double: _core_double.OpenCLWrapper_double | None = None


def weights(
    dz: float = 1.0,
    dy: float = 1.0,
    dx: float = 1.0,
    inhom: np.ndarray[Any, Any] | None = None,
    diffusivity: np.ndarray[Any, Any] | float = 1.0,
    double_precision: bool = False,
) -> np.ndarray[Any, Any]:
    """
    Calculate the weights for the diffusion term in the reaction-diffusion
    equation.

    :param dz: The distance between points in the z-dimension, see :py:func:`deltas`.
    :param dy: The distance between points in the y-dimension.
    :param dx: The distance between points in the x-dimension.
    :param inhom: A 3D array with integer values, encoding which model to use at each point. \
            Its value is zero for points outside the medium and one or more for points inside. \
            If ``None``, all points are considered inside the medium.
    :param diffusivity: The diffusivity matrix, see :py:func:`diffusivity_matrix`. \
            If a scalar is given, the matrix is isotropic with the same value in all directions.
    :param double_precision: If ``True``, use double precision for calculations.
    :return: Weight matrix for the diffusion term, A 5D array of shape (1, Nz, Ny, Nx, 19).
    """

    assert dz > 0
    assert dy > 0
    assert dx > 0

    if inhom is None:
        inhom = np.ones(shape=(1, 1, 1))
    assert inhom.ndim == 3

    mask = inhom > 0
    mask.shape = (1, *mask.shape, 1)

    diffusivity = np.array(diffusivity)
    assert isinstance(diffusivity, np.ndarray)
    if diffusivity.ndim == 0:
        diffusivity = diffusivity_matrix(Df=float(diffusivity.item()))
    assert diffusivity.ndim == 4
    assert diffusivity.shape[-1] == 6

    args = dz, dy, dx, mask, diffusivity

    global cl, cl_double  # noqa: PLW0603  # pylint: disable=global-statement
    if double_precision:
        if cl_double is None:
            cl_double = _core_double.setup()
        return _core_double.weights(cl_double, *args)
    if cl is None:
        cl = _core.setup()
    return _core.weights(cl, *args)


def run(
    models: Models,  # pylint: disable=redefined-outer-name
    inhom: np.ndarray[Any, Any],
    weights: np.ndarray[Any, Any],  # pylint: disable=redefined-outer-name
    states: np.ndarray[Any, Any],
    stim_signal: np.ndarray[Any, Any] | None = None,
    stim_shape: np.ndarray[Any, Any] | None = None,
    Nt: int = 1,  # pylint: disable=invalid-name
    dt: float = 0.001,
    double_precision: bool = False,
) -> np.ndarray[Any, Any]:
    """
    Run a Pigreads simulation.

    :param models: The models to be used in the simulation, see :py:class:`Models`.
    :param inhom: A 3D array with integer values, encoding which model to use at each point. \
            Its value is zero for points outside the medium and one or more for points inside. \
            Values larger than zero are used to select one of multiple models: \
            1 for ``models[0]``, 2 for ``models[1]``, etc.
    :param weights: The weights for the diffusion term, see :py:func:`weights`.
    :param states: The initial states of the simulation, a 4D array of shape \
            (Nz, Ny, Nx, Nv), see :py:func:`Models.resting_states`.
    :param stim_signal: A 2D array with the stimulus signal at each time point \
            for all variables, with shape (Nt, Nv). If ``None``, no stimulus is applied.
    :param stim_shape: A 3D array specifying the shape of the stimulus, \
            with shape (Nz, Ny, Nx). If ``None``, no stimulus is applied
    :param Nt: The number of time steps to run the simulation for.
    :param dt: The time step size.
    :param double_precision: If ``True``, use double precision for calculations.
    :return: The final states of the simulation, a 4D array of shape (Nz, Ny, Nx, Nv).
    """
    assert Nt > 0
    assert dt > 0
    assert isinstance(models, Models)
    assert len(models) > 0, "must add at least one model"
    assert inhom.ndim == 3

    if stim_signal is None:
        stim_signal = np.zeros((1, 1, 1, 1, 1))
    else:
        assert stim_signal.ndim == 2
        stim_signal = np.reshape(
            stim_signal, (stim_signal.shape[0], 1, 1, 1, stim_signal.shape[1])
        )

    if stim_shape is None:
        stim_shape = np.zeros((1, 1, 1, 1, 1))
    else:
        assert stim_shape.ndim == 3
        stim_shape = np.where(inhom > 0, stim_shape, 0)
        stim_shape.shape = (1, *stim_shape.shape, 1)  # type: ignore[union-attr]

    args = (
        models.array,
        np.reshape(inhom, (*inhom.shape, 1)),
        weights,
        states,
        stim_signal,
        stim_shape,
        Nt,
        dt,
    )

    global cl, cl_double  # noqa: PLW0603  # pylint: disable=global-statement
    if double_precision:
        if cl_double is None:
            cl_double = _core_double.setup()
        return _core_double.run(cl_double, *args)  # type: ignore[arg-type]
    if cl is None:
        cl = _core.setup()
    return _core.run(cl, *args)  # type: ignore[arg-type]


def get_upper_triangle(
    matrix: np.ndarray[Any, Any],
) -> np.ndarray[Any, Any]:
    """
    Convert a 3x3 matrix to a 6D vector, with the diagonal and upper triangle
    of the matrix as elements in the order xx, yy, zz, yz, xz, xy. Additional
    dimensions are supported, but the last two dimensions must each have size
    3.

    :param matrix: A 3x3 matrix.
    :return: A 6D vector.
    """

    matrix = np.array(matrix)
    assert matrix.ndim >= 2, "matrix must have at least two dimensions"
    assert matrix.shape[-1] == 3, "matrix must be a 3x3 matrix (in the last two axes)"
    assert matrix.shape[-2] == 3, "matrix must be a 3x3 matrix (in the last two axes)"
    assert np.allclose(matrix[..., 1, 2], matrix[..., 2, 1]), (
        "The yz and zy components of matrix need to be the same"
    )
    assert np.allclose(matrix[..., 0, 2], matrix[..., 2, 0]), (
        "The xz and zx components of matrix need to be the same"
    )
    assert np.allclose(matrix[..., 0, 1], matrix[..., 1, 0]), (
        "The xy and yx components of matrix need to be the same"
    )
    triag: np.ndarray[Any, Any] = np.stack(
        (
            matrix[..., 0, 0],  # xx
            matrix[..., 1, 1],  # yy
            matrix[..., 2, 2],  # zz
            matrix[..., 1, 2],  # yz
            matrix[..., 0, 2],  # xz
            matrix[..., 0, 1],  # xy
        ),
        axis=-1,
    )
    return triag


def normalise_vector(
    f: np.ndarray[Any, Any] | list[int] | tuple[int, int, int],
) -> np.ndarray[Any, Any]:
    """
    Normalise a 3D vector to unit length.

    :param f: A 3D vector over space with shape (Nz, Ny, Nx, 3).
    :return: A 5D vector with shape (Nz, Ny, Nx, 3, 1).
    """

    f = np.array(f, dtype=dtype)
    assert isinstance(f, np.ndarray)
    assert f.ndim >= 1, "f must be a 3D vector"
    assert f.ndim <= 4, "too many dimensions for f"
    assert f.shape[-1] == 3, "f must be a 3D vector (in the last axis)"
    while f.ndim < 4:
        f.shape = (1, *f.shape)
    norm = np.linalg.norm(f, axis=-1)
    nonzero = norm > 0
    norm.shape = (*norm.shape, 1)
    f[nonzero] /= norm[nonzero]
    f.shape = (*f.shape, 1)
    assert f.ndim == 5, "f must have 5 dimensions: z, y, x, row, col"
    assert f.shape[-1] == 1, "f must be a 3D column vector"
    assert f.shape[-2] == 3, "f must be a 3D column vector"
    return f


def diffusivity_matrix(
    f: np.ndarray[Any, Any] | list[int] | tuple[int, int, int] | None = None,
    n: np.ndarray[Any, Any] | list[int] | tuple[int, int, int] | None = None,
    Df: np.ndarray[Any, Any] | float = 1.0,  # pylint: disable=invalid-name
    Ds: np.ndarray[Any, Any] | float | None = None,  # pylint: disable=invalid-name
    Dn: np.ndarray[Any, Any] | float | None = None,  # pylint: disable=invalid-name
    dtype: type = dtype,  # pylint: disable=redefined-outer-name
) -> np.ndarray[Any, Any]:
    """
    Define a diffusivity matrix :math:`\\textbf D` for the reaction-diffusion equation.

    If ``f`` and ``n`` are given, the matrix is defined as:

    .. math::

        \\textbf D = \\textbf D_s \\textbf I + (\\textbf D_f - \\textbf D_s)
        \\textbf f \\textbf f^\\mathrm{T} + (\\textbf D_n - \\textbf D_s)
        \\textbf n \\textbf n^\\mathrm{T}

    :param f: The main direction of diffusion, i.e., the fibre direction. \
            3D vector over space with shape (Nz, Ny, Nx, 3). Optional if :math:`D_f=D_s=D_n`.
    :param n: The direction of weakest diffusion, i.e., the direction normal to the fibre sheets. \
            A 3D vector over space with shape (Nz, Ny, Nx, 3). Optional if :math:`D_s=D_n`.
    :param Df: The diffusivity in the direction of the fibres, :math:`\\mathbf{f}`.
    :param Ds: The diffusivity in the fibre sheets, but normal to :math:`\\mathbf{f}`. \
            If ``None``, :math:`D_s` is set to :math:`D_f`.
    :param Dn: The diffusivity in the direction normal to the fibre sheets, \
            i.e., along :math:`\\mathbf{n}`. \
            If ``None``, :math:`D_n` is set to :math:`D_s`.
    :param dtype: The data type of the output array.
    """

    if Ds is None:
        Ds = Df

    if Dn is None:
        Dn = Ds

    if f is None:
        assert np.allclose(Df, Ds), "If Df!=Ds, f must be given"
        f = [0, 0, 0]

    if n is None:
        assert np.allclose(Ds, Dn), "If Ds!=Dn, n must be given"
        n = [0, 0, 0]

    f = normalise_vector(f)
    n = normalise_vector(n)
    eye = np.eye(3, dtype=dtype)
    eye.shape = (1, 1, 1, 3, 3)

    D = get_upper_triangle(  # pylint: disable=invalid-name
        Ds * eye
        + (Df - Ds) * f * np.swapaxes(f, -1, -2)
        + (Dn - Ds) * n * np.swapaxes(n, -1, -2)
    )
    assert D.ndim == 4
    assert D.shape[-1] == 6
    return D


class Models(list[dict[str, Any]]):
    """
    This class stores the models to be used in a Pigreads simulation. It
    behaves like a dictionary :py:class:`dict`. The models are defined in C++
    code. Their metadata is stored YAML format in the :py:func:`models`
    function. The class variable :py:attr:`available` is a dictionary of all
    available models.

    Models are added to an instance of this class using the :py:meth:`add`
    method, or as a list of tuples in the constructor. The order of the models
    is the order in which they are used in the simulation. ``models[0]`` is used
    at ``inhom`` values of 1, ``models[1]`` at 2, etc.

    :param tuples_key_kwargs: A list of tuples with the model key and keyword \
    arguments encoding parameter names and values to be passed to the \
    :py:meth:`add` method. If a string is given, it is treated the name of the \
    first model to be added with no keyword arguments. If ``None``, no \
    models are added.
    """

    available: dict[str, dict[str, Any]] = yaml.safe_load(models())
    """
    Dictionary of all available models.
    """

    def __init__(
        self, tuples_key_kwargs: list[tuple[str, dict[str, float]]] | str | None = None
    ):
        super().__init__(self)
        if tuples_key_kwargs is None:
            tuples_key_kwargs = []
        elif isinstance(tuples_key_kwargs, str):
            tuples_key_kwargs = [(tuples_key_kwargs, {})]
        for key, kwargs in tuples_key_kwargs:
            self.add(key, **kwargs)

    def add(self, key: str, **kwargs: Any) -> None:
        """
        Add a model to the list of models.

        :param key: The key of the model to be added.
        :param kwargs: Parameter names and their values to be passed to the model.
        """
        model = deepcopy(self.info(key))
        for param, value in kwargs.items():
            assert param in model["parameters"], (
                f"Unknown parameter: {param}.\n\n"
                + yaml.safe_dump(dict(model["parameters"]), sort_keys=False)
            )
            model["parameters"][param] = value
        model["key"] = key
        self.append(model)

    @classmethod
    def info(cls, key: str) -> dict[str, Any]:
        """
        Get the metadata of a model.

        :param key: The key of the model.
        :return: A dictionary with the metadata of the model.
        """
        try:
            return deepcopy(cls.available[key])
        except KeyError as e:
            e.add_note(  # type: ignore[attr-defined]
                "\nAvailable models:\n- " + "\n- ".join(cls.available.keys()) + "\n"
            )
            raise e

    @property
    def array(self) -> np.ndarray[Any, Any]:
        """
        Represent the models as a 2D array with the model IDs and all
        parameters to be passed to the C++ code.
        """
        arr = []
        for model in self:
            arr.append(model["id"])
            arr.extend(model["parameters"].values())
        ret: np.ndarray[Any, Any] = np.array(arr, dtype=dtype)
        return ret

    @property
    def Nv(self) -> int:  # pylint: disable=invalid-name
        """
        The maximum number of state variables in the models.
        """
        return max(len(model["variables"]) for model in self)

    def resting_states(
        self,
        inhom: np.ndarray[Any, Any],
        Nframes: int = 1,  # pylint: disable=invalid-name
    ) -> np.ndarray[Any, Any]:
        """
        Create an array of states and fill the first frame with the resting
        values of the models depending on the ``inhom`` values.

        :param inhom: A 3D array with integer values, encoding which model to use at each point. \
                Its value is zero for points outside the medium and one or more for points inside. \
                Values larger than zero are used to select one of multiple models: \
                1 for ``models[0]``, 2 for ``models[1]``, etc.

        :param Nframes: The number of frames in time.
        :return: A 5D array of shape (Nframes, Nz, Ny, Nx, Nv).
        """

        model_count = len(self)
        assert model_count > 0, "must add at least one model"
        assert inhom.ndim == 3
        inhom = inhom.astype(int)
        mask = inhom > 0
        states: np.ndarray[Any, Any] = np.zeros(
            shape=(Nframes, *inhom.shape, self.Nv), dtype=dtype
        )
        for imodel, model in enumerate(self):
            for iv, resting in enumerate(model["variables"].values()):
                states[0, mask * ((inhom - 1) % model_count == imodel), iv] = resting
        states[:, ~mask, :] = np.nan
        return states


def to_ithildin(
    framedur: float,
    dt: float,
    dz: float,
    dy: float,
    dx: float,
    models: Models,  # pylint: disable=redefined-outer-name
    states: np.ndarray[Any, Any],
    inhom: np.ndarray[Any, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, np.ndarray[Any, Any]]]:
    """
    Convert the output of a Pigreads simulation to an Ithildin SimData object.

    While originally designed for a different reaction-diffusion solver,
    the Python module for Ithildin is useful to analyse Pigreads simulations.

    :param framedur: The duration between subsequent frames, usually in milliseconds.
    :param dt: The time step size used in :py:func:`run`, usually in milliseconds.
    :param dz: The distance between points in the z-dimension, see :py:func:`deltas`.
    :param dy: The distance between points in the y-dimension.
    :param dx: The distance between points in the x-dimension.
    :param models: The models used in the simulation, see :py:class:`Models`.
    :param states: The states of the simulation, a 5D array of shape \
            (Nt, Nz, Ny, Nx, Nv), see :py:func:`Models.resting_states` and :py:func:`run`.
    :param inhom: A 3D array with integer values, encoding which model to use at each point. \
            Its value is zero for points outside the medium and one or more for points inside. \
            If ``None``, all points are considered inside the medium.
    :return: Tuple of an Ithildin log file as a string \
            and a dictionary of the variables by variable name.

    Usage::

        import ithildin as ith
        log, variables = pig.to_ithildin(Nt * dt, dt, dz, dy, dx, models, states, inhom)
        sd = ith.SimData(log=ith.Log(data=log))
        sd.vars = variables
    """

    Nt, Nz, Ny, Nx, _ = states.shape  # pylint: disable=invalid-name

    timestamp = datetime.now()

    log = {
        "Ithildin log version": 2,
        "Simulation parameters": {
            "Ithildin library version": f"pigreads {__version__}",
            "Timestep dt": dt,
            "Frame duration": framedur,
            "Number of frames to take": Nt,
            "Serial number": int(timestamp.strftime(r"%Y%m%d%H%M%S")),
            "Name of simulation series": "pigreads",
        },
        "Geometry parameters": {
            "Number of dimensions": 3,
            "Voxel size": [dx, dy, dz],
            "Domain size": [Nx, Ny, Nz],
        },
        "Start date": timestamp.isoformat(),
    }

    for i, model in enumerate(models):
        key = "Model parameters"
        if i > 0:
            key += f" {i}"
        log[key] = {
            "Model type": model["name"],
            "Class": model["key"],
            "Citation": "\n".join(model["dois"]),
            "Parameters": model["parameters"],
            "Initial values": model["variables"],
            "Variable names": list(model["variables"].keys()),
            "Number of vars": len(model["variables"]),
        }

    shape = (-1, Nz, Ny, Nx)
    variables: dict[str, np.ndarray[Any, Any]] = {
        v: states[..., iv].reshape(shape)
        for iv, v in enumerate(models[0]["variables"].keys())
    }
    if inhom is not None:
        variables["inhom"] = inhom.reshape(shape)

    return log, variables


def delta(x: np.ndarray[Any, Any], ax: int = -1) -> float:
    """
    Extract grid spacing from a 3D array.

    :param x: A 3D array.
    :param ax: The axis along which to calculate the distance.
    :return: The distance between the first two points.

    For example, consider this code::

        z, y, x = np.mgrid[0, 0:4:0.2, 0:1:5j]
        dx = pig.delta(z, ax=-1)
        dy = pig.delta(z, ax=-2)
        dz = pig.delta(z, ax=-3)
    """
    assert x.ndim == 3
    diff = np.diff(np.moveaxis(x, ax, -1)[0, 0, :2])
    return 1.0 if diff.shape[0] == 0 else float(diff[0])


def deltas(*x: np.ndarray[Any, Any]) -> list[float]:
    """
    Extract grid spacing from a 3D meshgrid.

    For example, consider this code::

        z, y, x = np.mgrid[0, 0:4:0.2, 0:1:5j]
        dz, dy, dx = pig.deltas(z, y, x)

    :param x: A 3D array.
    :return: A list with the distances between the points.
    """
    return [delta(xi, i) for i, xi in enumerate(x)]


__all__ = [
    "Models",
    "__version__",
    "delta",
    "deltas",
    "diffusivity_matrix",
    "get_upper_triangle",
    "models",
    "normalise_vector",
    "run",
    "to_ithildin",
    "weights",
]
