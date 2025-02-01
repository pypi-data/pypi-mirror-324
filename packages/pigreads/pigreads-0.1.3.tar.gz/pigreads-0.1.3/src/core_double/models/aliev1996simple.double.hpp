#ifndef __OPENCL_VERSION__
const std::string Model_aliev1996simple_info = R"model(
aliev1996simple:
  name: Aliev & Panfilov 1996
  description: A simple two-variable model of cardiac excitation.
  dois:
  - https://doi.org/10.1016/0960-0779(95)00089-5
  variables:
    u: 0.0
    v: 0.0
  parameters:
    diffusivity_u: 1.0
    eps0: 0.002
    mu1: 0.2
    mu2: 0.3
    a: 0.15
    k: 8.0
  key: aliev1996simple
)model";
#endif

static const Size Model_aliev1996simple_id = UNIQUE_ID;
static const Size Model_aliev1996simple_Nv = 2;
static const Size Model_aliev1996simple_Np = 6;

#ifdef __OPENCL_VERSION__
void Model_aliev1996simple_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_u = params[0];
  const Real eps0 = params[1];
  const Real mu1 = params[2];
  const Real mu2 = params[3];
  const Real a = params[4];
  const Real k = params[5];
  const Real u = _r(_v(0, states_old));
  Real* const _new_u = _pr(_v(0, states_new));
  const Real _diffuse_u = diffusivity_u * diffuse(weights, _v(0, states_old));
  const Real v = _r(_v(1, states_old));
  Real* const _new_v = _pr(_v(1, states_new));

  const Real eps = eps0 + mu1 * v / (u + mu2);
  const Real _react_u = -k * u * (u - a) * (u - 1.0) - u * v;
  const Real _react_v = eps * (-v - k * u * (u - a - 1.0));
  *_new_u = u + dt * (_react_u + _diffuse_u);
  *_new_v = v + dt * _react_v;
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_aliev1996simple_kernel(
        Size model_count,
        __global Size* model_ids,
        __global Size* model_offsets,
        __global Real* model_params,
        __global void* inhom_data,      struct StatesIdx inhom_idx,
        __global void* weights_data,    struct StatesIdx weights_idx,
        __global void* states_old_data, struct StatesIdx states_old_idx,
        __global void* states_new_data, struct StatesIdx states_new_idx,
        const Real dt
) {

  struct States inhom      = {inhom_data,      STATES_UNPACK(inhom_idx)};
  struct States weights    = {weights_data,    STATES_UNPACK(weights_idx)};
  struct States states_old = {states_old_data, STATES_UNPACK(states_old_idx)};
  struct States states_new = {states_new_data, STATES_UNPACK(states_new_idx)};

  const Size iz = get_global_id(0);
  const Size iy = get_global_id(1);
  const Size ix = get_global_id(2);

  if (ix < states_old.Nx && iy < states_old.Ny && iz < states_old.Nz) {
    const Int inhom_zyx = _i(States_offset(inhom, 0, iz, iy, ix, 0));
    if (inhom_zyx > 0) {
      const Size imodel = (inhom_zyx - 1) % model_count;
      const Size model_id = model_ids[imodel];
      if (model_id == Model_aliev1996simple_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_aliev1996simple_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
