#ifndef __OPENCL_VERSION__
const std::string Model_marcotte2017dynamical_info = R"model(
marcotte2017dynamical:
  name: Smoothed Karma (Marcotte & Grigoriev 2017)
  description: Smoothed version of the Karma model as published by Marcotte & Grigoriev
    in 2017.
  dois:
  - https://doi.org/10.1063/1.5003259
  - https://doi.org/10.1063/1.4915143
  - https://doi.org/10.1103/PhysRevLett.71.1103
  - https://doi.org/10.1063/1.166024
  variables:
    u: 0.0
    v: 0.0
  parameters:
    diffusivity_u: 4.0062
    diffusivity_v: 0.20031
    beta: 1.389
    eps: 0.01
    ustar: 1.5415
  key: marcotte2017dynamical
)model";
#endif

static const Size Model_marcotte2017dynamical_id = UNIQUE_ID;
static const Size Model_marcotte2017dynamical_Nv = 2;
static const Size Model_marcotte2017dynamical_Np = 5;

#ifdef __OPENCL_VERSION__
void Model_marcotte2017dynamical_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_u = params[0];
  const Real diffusivity_v = params[1];
  const Real beta = params[2];
  const Real eps = params[3];
  const Real ustar = params[4];
  const Real u = _r(_v(0, states_old));
  Real* const _new_u = _pr(_v(0, states_new));
  const Real _diffuse_u = diffusivity_u * diffuse(weights, _v(0, states_old));
  const Real v = _r(_v(1, states_old));
  Real* const _new_v = _pr(_v(1, states_new));
  const Real _diffuse_v = diffusivity_v * diffuse(weights, _v(1, states_old));

  const Real e = exp(2. * (1.2571 * (u - 1.)));
  const Real V = eps * (beta * ((1. + (e - 1.) / (e + 1.)) / 2.) + (1. + (exp(2. * (1.2571 * (v - 1.))) - 1.) / (exp(2. * (1.2571 * (v - 1.))) + 1.)) / 2. * (v - 1.) - v);
  const Real U = (ustar - v * v * v * v) * (1. - (exp(2. * (u - 3.)) - 1.) / (exp(2. * (u - 3.)) + 1.)) * u * u / 2. - u;

  *_new_u = u + dt * (U + _diffuse_u);
  *_new_v = v + dt * (V + _diffuse_v);
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_marcotte2017dynamical_kernel(
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
      if (model_id == Model_marcotte2017dynamical_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_marcotte2017dynamical_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
