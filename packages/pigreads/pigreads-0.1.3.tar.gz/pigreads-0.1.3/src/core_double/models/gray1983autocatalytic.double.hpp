#ifndef __OPENCL_VERSION__
const std::string Model_gray1983autocatalytic_info = R"model(
gray1983autocatalytic:
  name: Gray & Scott 1982
  description: |-
    One of the two variable reaction-diffusion model presented in the article
    "Autocatalytic reactions in the isothermal, continuous stirred tank
    reactor: isolas and other forms of multistability".

    It describes the chemical reactions:
    U + 2V -> 3V
    V -> P

    u, v: concentrations of U, V.
    k: rate of conversion of V to P.
    f: rate of the process that feeds U and drains U, V, and P.
  dois:
  - https://doi.org/10.1016/0009-2509(83)80132-8
  variables:
    u: 1.0
    v: 0.0
  parameters:
    diffusivity_u: 1
    diffusivity_v: 0.5
    f: 0.055
    k: 0.062
  key: gray1983autocatalytic
)model";
#endif

static const Size Model_gray1983autocatalytic_id = UNIQUE_ID;
static const Size Model_gray1983autocatalytic_Nv = 2;
static const Size Model_gray1983autocatalytic_Np = 4;

#ifdef __OPENCL_VERSION__
void Model_gray1983autocatalytic_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_u = params[0];
  const Real diffusivity_v = params[1];
  const Real f = params[2];
  const Real k = params[3];
  const Real u = _r(_v(0, states_old));
  Real* const _new_u = _pr(_v(0, states_new));
  const Real _diffuse_u = diffusivity_u * diffuse(weights, _v(0, states_old));
  const Real v = _r(_v(1, states_old));
  Real* const _new_v = _pr(_v(1, states_new));
  const Real _diffuse_v = diffusivity_v * diffuse(weights, _v(1, states_old));

  const Real uvv = u * v * v;
  const Real U = -uvv + f * (1 - u);
  const Real V = uvv - (f + k) * v;

  *_new_u = u + dt * (U + _diffuse_u);
  *_new_v = v + dt * (V + _diffuse_v);
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_gray1983autocatalytic_kernel(
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
      if (model_id == Model_gray1983autocatalytic_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_gray1983autocatalytic_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
