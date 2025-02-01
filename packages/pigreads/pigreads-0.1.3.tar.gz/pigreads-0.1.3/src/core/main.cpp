#include <cmath>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <set>
#include <stdint.h>
#include <string>

#define ASSERT(code)                                                           \
  if (not(code))                                                               \
    throw std::runtime_error(std::string(__FILE__) + ":" +                     \
                             std::to_string(__LINE__) + ":ASSERT(" +           \
                             std::string(#code) + ")");
namespace py = pybind11;

// 1. type definitions
#include "types.h"

// 2. interface to OpenCL
#include "opencl.hpp"

// 3. matrix data structure
#include "states.h"

// 4. all the models
#include "models.hpp"

// 5. kernel source code
#include "kernels.h"

std::unique_ptr<OpenCLWrapper> setup() {
  std::unique_ptr<OpenCLWrapper> cl = std::make_unique<OpenCLWrapper>();
  cl->compile(kernels_source);
  return cl;
}

std::string models() { return Models::list_all(); }

py::array_t<Real> weights(OpenCLWrapper *cl, const Real dz, const Real dy,
                          const Real dx, const py::array_t<Int> py_mask,
                          const py::array_t<Real> py_diffusivity) {

  ASSERT(cl);

  struct States mask = STATES_FROM_NPY(Int, py_mask);
  ASSERT(mask.Nt == 1);
  ASSERT(mask.Nv == 1);
  mask.data = py_mask.request().ptr;
  mask.buffer = cl->bufferR(STATES_DATA_SIZE(mask), mask.data);

  struct States diffusivity = STATES_FROM_NPY(Real, py_diffusivity);
  ASSERT(diffusivity.Nt == 1);
  ASSERT(diffusivity.Nv == 6);
  diffusivity.data = py_diffusivity.request().ptr;
  diffusivity.buffer =
      cl->bufferR(STATES_DATA_SIZE(diffusivity), diffusivity.data);

  struct States weights{NULL, sizeof(Real), 1, mask.Nz, mask.Ny, mask.Nx, 19};
  STATES_MALLOC(weights);
  weights.buffer = cl->bufferW(STATES_DATA_SIZE(weights));

  cl->execute("calculate_weights", {weights.Nz, weights.Ny, weights.Nx}, dz, dy,
              dx, mask.buffer, StatesIdx{STATES_UNPACK(mask)},
              diffusivity.buffer, StatesIdx{STATES_UNPACK(diffusivity)},
              weights.buffer, StatesIdx{STATES_UNPACK(weights)});

  cl->copyBufferData(STATES_DATA_SIZE(weights), weights.buffer, weights.data);

  cl->free(mask.buffer);
  cl->free(diffusivity.buffer);
  cl->free(weights.buffer);

  return py::array_t<Real>(STATES_SHAPE(weights), (Real *)weights.data);
}

py::array_t<Real>
run(OpenCLWrapper *cl, const py::array_t<Real> py_models,
    const py::array_t<Int> py_inhom, const py::array_t<Real> py_weights,
    const py::array_t<Real> py_states, const py::array_t<Real> py_stim_signal,
    const py::array_t<Real> py_stim_shape, const Size Nt, const Real dt) {

  ASSERT(cl);

  ASSERT(dt > 0);
  ASSERT(Nt > 0);

  Models models((Size)py_models.size(), (Real *)py_models.request().ptr);
  models.buffer(cl);

  struct States s = STATES_FROM_NPY(Real, py_states);
  ASSERT(s.Nt == 1);
  s.data = py_states.request().ptr;

  struct States states{NULL, s.Ns, 2, s.Nz, s.Ny, s.Nx, s.Nv};
  ASSERT(states.Nv == models.Nv);
  STATES_MALLOC(states);
  for (Size i = 0; i < STATES_SIZE(states); i++) {
    ((Real *)states.data)[i] = 0;
  }
  memcpy(states.data, py_states.request().ptr, states.Ns * py_states.size());
  states.buffer = cl->buffer(STATES_DATA_SIZE(states), states.data,
                             CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR);

  struct States weights = STATES_FROM_NPY(Real, py_weights);
  ASSERT(weights.Nt == 1);
  ASSERT(weights.Nv == 19);
  weights.data = py_weights.request().ptr;
  weights.buffer = cl->bufferR(STATES_DATA_SIZE(weights), weights.data);

  struct States inhom = STATES_FROM_NPY(Int, py_inhom);
  ASSERT(inhom.Nt == 1);
  ASSERT(inhom.Nv == 1);
  inhom.data = py_inhom.request().ptr;
  inhom.buffer = cl->bufferR(STATES_DATA_SIZE(inhom), inhom.data);

  struct States stim_signal = STATES_FROM_NPY(Real, py_stim_signal);
  ASSERT(stim_signal.Nz == 1);
  ASSERT(stim_signal.Ny == 1);
  ASSERT(stim_signal.Nx == 1);
  stim_signal.data = py_stim_signal.request().ptr;

  struct States stim_shape = STATES_FROM_NPY(Real, py_stim_shape);
  ASSERT(stim_shape.Nt == 1);
  ASSERT(stim_shape.Nv == 1);
  stim_shape.data = py_stim_shape.request().ptr;
  stim_shape.buffer =
      cl->bufferR(STATES_DATA_SIZE(stim_shape), stim_shape.data);

  const std::vector<Size> work_size = {states.Nz, states.Ny, states.Nx};
  const std::set<Size> set_of_model_ids = models.get_set_of_model_ids();

  cl->execute("set_outside", work_size, Real(0.0), inhom.buffer,
              StatesIdx{STATES_UNPACK(inhom)}, states.buffer,
              StatesIdx{STATES_UNPACK(states)});

  for (Size it = 0; it < Nt; it++) {
    for (Size mid : set_of_model_ids) {
      models.step(cl, mid, inhom, weights, _t(it, states), _t(it + 1, states),
                  dt);
    }

    if (STATES_SIZE(stim_signal) > 0 && STATES_SIZE(stim_shape) > 0) {
      for (Size iv = 0; iv < models.Nv; iv++) {
        const Real stim_amplitude = _r(_v(iv, _t(it, stim_signal)));
        if (fabs(stim_amplitude) > VERY_SMALL_NUMBER) {
          struct States stim_states = _v(iv, _t(it + 1, states));
          cl->execute("add_stimulus", work_size, dt * stim_amplitude,
                      stim_shape.buffer, StatesIdx{STATES_UNPACK(stim_shape)},
                      stim_states.buffer,
                      StatesIdx{STATES_UNPACK(stim_states)});
        }
      }
    }
  }

  for (Size it = 0; it < states.Nt; it++) {
    cl->execute("set_outside", work_size, Real(NAN), inhom.buffer,
                StatesIdx{STATES_UNPACK(inhom)}, states.buffer,
                StatesIdx{STATES_UNPACK(_t(it, states))});
  }

  cl->copyBufferData(STATES_DATA_SIZE(states), states.buffer, states.data);

  cl->free(weights.buffer);
  cl->free(inhom.buffer);
  cl->free(stim_shape.buffer);
  cl->free(states.buffer);

  return py::array_t<Real>(py_states.request().shape, _pr(_t(Nt - 1, states)));
}

#define BIND_FUNCTION(module, func, docstring)                                 \
  module.def(#func, &func, docstring);
#define BIND_CLASS(module, class)                                              \
  py::class_<class>(m, #class).def(py::init<>());

PYBIND11_MODULE(MODULE, m) {
  m.doc() = R"pbdoc(
        Low-level implementation
        ------------------------
        .. currentmodule:: pigreads
    )pbdoc";

  BIND_CLASS(m, OpenCLWrapper);

  BIND_FUNCTION(m, setup, R"pbdoc(
      Compile OpenCL code and return the OpenCLWrapper.
    )pbdoc");

  BIND_FUNCTION(m, models, R"pbdoc(
        List available models (in YAML format).
    )pbdoc");

  BIND_FUNCTION(m, weights, R"pbdoc(
        Calculate the weights for diffusion.
    )pbdoc");

  BIND_FUNCTION(m, run, R"pbdoc(
        Run a simulation.
    )pbdoc");
}
