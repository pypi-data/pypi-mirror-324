#ifndef __OPENCL_VERSION__
const std::string Model_trivial_info = R"model(
trivial:
  name: Trivial model
  description: This model encodes only diffusion, with a zero reaction term.
  dois: []
  variables:
    u: 0.0
  key: trivial
  parameters:
    diffusivity_u: 1.0
)model";
#endif

static const Size Model_trivial_id = UNIQUE_ID;
static const Size Model_trivial_Nv = 1;
static const Size Model_trivial_Np = 1;

#ifdef __OPENCL_VERSION__
void Model_trivial_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_u = params[0];
  const Real u = _r(_v(0, states_old));
  Real* const _new_u = _pr(_v(0, states_new));
  const Real _diffuse_u = diffusivity_u * diffuse(weights, _v(0, states_old));

  *_new_u = u + dt * _diffuse_u;
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_trivial_kernel(
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
      if (model_id == Model_trivial_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_trivial_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
