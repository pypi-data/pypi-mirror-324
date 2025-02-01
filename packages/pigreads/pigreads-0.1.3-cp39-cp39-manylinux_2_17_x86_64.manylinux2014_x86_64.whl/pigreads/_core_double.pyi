"""
Type annotations for low-level implementation
---------------------------------------------
"""

from __future__ import annotations

from typing import Any

import numpy as np

# pylint: disable=unused-argument
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class OpenCLWrapper_double: ...  # pylint: disable=invalid-name

def setup() -> OpenCLWrapper_double: ...
def models() -> str: ...
def weights(
    cl: OpenCLWrapper_double,
    dz: Any,
    dy: Any,
    dx: Any,
    py_mask: np.ndarray[Any, Any],
    py_diffusivity: np.ndarray[Any, Any],
) -> np.ndarray[Any, Any]: ...
def run(
    cl: OpenCLWrapper_double,
    py_models: np.ndarray[Any, Any],
    py_inhom: np.ndarray[Any, Any],
    py_weights: np.ndarray[Any, Any],
    py_states: np.ndarray[Any, Any],
    py_stim_signal: np.ndarray[Any, Any],
    py_stim_shape: np.ndarray[Any, Any],
    Nt: Any,  # pylint: disable=invalid-name
    dt: Any,
) -> np.ndarray[Any, Any]: ...
