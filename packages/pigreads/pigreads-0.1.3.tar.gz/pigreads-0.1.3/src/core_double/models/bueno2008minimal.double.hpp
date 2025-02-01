#ifndef __OPENCL_VERSION__
const std::string Model_bueno2008minimal_info = R"model(
bueno2008minimal:
  name: Bueno-Orovio, Cherry, and Fenton (2008)
  description: Minimal model for human ventricular action potentials in tissue.
  dois:
  - https://doi.org/10.1016/j.jtbi.2008.03.029
  variables:
    u: 0.0
    v: 1.0
    w: 1.0
    s: 0.0
  parameters:
    diffusivity_u: 0.1171
    u0: 0
    u_u: 1.55
    theta_v: 0.3
    theta_w: 0.13
    theta_vm: 0.006
    theta_0: 0.006
    tau_v1m: 60
    tau_v2m: 1150
    tau_vp: 1.4506
    tau_w1m: 60
    tau_w2m: 15
    k_wm: 65
    u_wm: 0.03
    tau_wp: 200
    tau_fi: 0.11
    tau_o1: 400
    tau_o2: 6
    tau_so1: 30.0181
    tau_so2: 0.9957
    k_so: 2.0458
    u_so: 0.65
    tau_s1: 2.7342
    tau_s2: 16
    k_s: 2.0994
    u_s: 0.9087
    tau_si: 1.8875
    tau_winf: 0.07
    w_infstar: 0.94
  parameter sets:
    EPI:
      u0: 0
      u_u: 1.55
      theta_v: 0.3
      theta_w: 0.13
      theta_vm: 0.006
      theta_0: 0.006
      tau_v1m: 60
      tau_v2m: 1150
      tau_vp: 1.4506
      tau_w1m: 60
      tau_w2m: 15
      k_wm: 65
      u_wm: 0.03
      tau_wp: 200
      tau_fi: 0.11
      tau_o1: 400
      tau_o2: 6
      tau_so1: 30.0181
      tau_so2: 0.9957
      k_so: 2.0458
      u_so: 0.65
      tau_s1: 2.7342
      tau_s2: 16
      k_s: 2.0994
      u_s: 0.9087
      tau_si: 1.8875
      tau_winf: 0.07
      w_infstar: 0.94
    ENDO:
      u0: 0
      u_u: 1.56
      theta_v: 0.3
      theta_w: 0.13
      theta_vm: 0.2
      theta_0: 0.006
      tau_v1m: 75
      tau_v2m: 10
      tau_vp: 1.4506
      tau_w1m: 6
      tau_w2m: 140
      k_wm: 200
      u_wm: 0.016
      tau_wp: 280
      tau_fi: 0.1
      tau_o1: 470
      tau_o2: 6
      tau_so1: 40
      tau_so2: 1.2
      k_so: 2
      u_so: 0.65
      tau_s1: 2.7342
      tau_s2: 2
      k_s: 2.0994
      u_s: 0.9087
      tau_si: 2.9013
      tau_winf: 0.0273
      w_infstar: 0.78
    Midwall:
      u0: 0
      u_u: 1.61
      theta_v: 0.3
      theta_w: 0.13
      theta_vm: 0.1
      theta_0: 0.005
      tau_v1m: 80
      tau_v2m: 1.4506
      tau_vp: 1.4506
      tau_w1m: 70
      tau_w2m: 8
      k_wm: 200
      u_wm: 0.016
      tau_wp: 280
      tau_fi: 0.078
      tau_o1: 410
      tau_o2: 7
      tau_so1: 91
      tau_so2: 0.8
      k_so: 2.1
      u_so: 0.6
      tau_s1: 2.7342
      tau_s2: 4
      k_s: 2.0994
      u_s: 0.9087
      tau_si: 3.3849
      tau_winf: 0.01
      w_infstar: 0.5
    PB:
      u0: 0
      u_u: 1.45
      theta_v: 0.35
      theta_w: 0.13
      theta_vm: 0.175
      theta_0: 0.006
      tau_v1m: 10
      tau_v2m: 1150
      tau_vp: 1.4506
      tau_w1m: 140
      tau_w2m: 6.25
      k_wm: 65
      u_wm: 0.015
      tau_wp: 326
      tau_fi: 0.105
      tau_o1: 400
      tau_o2: 6
      tau_so1: 30.0181
      tau_so2: 0.9957
      k_so: 2.0458
      u_so: 0.65
      tau_s1: 2.7342
      tau_s2: 16
      k_s: 2.0994
      u_s: 0.9087
      tau_si: 1.8875
      tau_winf: 0.175
      w_infstar: 0.9
    TNNP:
      u0: 0
      u_u: 1.58
      theta_v: 0.3
      theta_w: 0.015
      theta_vm: 0.015
      theta_0: 0.006
      tau_v1m: 60
      tau_v2m: 1150
      tau_vp: 1.4506
      tau_w1m: 70
      tau_w2m: 20
      k_wm: 65
      u_wm: 0.03
      tau_wp: 280
      tau_fi: 0.11
      tau_o1: 6
      tau_o2: 6
      tau_so1: 43
      tau_so2: 0.2
      k_so: 2
      u_so: 0.65
      tau_s1: 2.7342
      tau_s2: 3
      k_s: 2.0994
      u_s: 0.9087
      tau_si: 2.8723
      tau_winf: 0.07
      w_infstar: 0.94
  key: bueno2008minimal
)model";
#endif

static const Size Model_bueno2008minimal_id = UNIQUE_ID;
static const Size Model_bueno2008minimal_Nv = 4;
static const Size Model_bueno2008minimal_Np = 29;

#ifdef __OPENCL_VERSION__
void Model_bueno2008minimal_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_u = params[0];
  const Real u0 = params[1];
  const Real u_u = params[2];
  const Real theta_v = params[3];
  const Real theta_w = params[4];
  const Real theta_vm = params[5];
  const Real theta_0 = params[6];
  const Real tau_v1m = params[7];
  const Real tau_v2m = params[8];
  const Real tau_vp = params[9];
  const Real tau_w1m = params[10];
  const Real tau_w2m = params[11];
  const Real k_wm = params[12];
  const Real u_wm = params[13];
  const Real tau_wp = params[14];
  const Real tau_fi = params[15];
  const Real tau_o1 = params[16];
  const Real tau_o2 = params[17];
  const Real tau_so1 = params[18];
  const Real tau_so2 = params[19];
  const Real k_so = params[20];
  const Real u_so = params[21];
  const Real tau_s1 = params[22];
  const Real tau_s2 = params[23];
  const Real k_s = params[24];
  const Real u_s = params[25];
  const Real tau_si = params[26];
  const Real tau_winf = params[27];
  const Real w_infstar = params[28];
  const Real u = _r(_v(0, states_old));
  Real* const _new_u = _pr(_v(0, states_new));
  const Real _diffuse_u = diffusivity_u * diffuse(weights, _v(0, states_old));
  const Real v = _r(_v(1, states_old));
  Real* const _new_v = _pr(_v(1, states_new));
  const Real w = _r(_v(2, states_old));
  Real* const _new_w = _pr(_v(2, states_new));
  const Real s = _r(_v(3, states_old));
  Real* const _new_s = _pr(_v(3, states_new));

  const Real Hthvm = (u - theta_vm > 0) ? 1 : 0;
  const Real Hthw = (u - theta_w > 0) ? 1 : 0;
  const Real Hth0 = (u - theta_0 > 0) ? 1 : 0;
  const Real Hthv = (u - theta_v > 0) ? 1 : 0;

  const Real Hkm = (1 + tanh(k_wm * (u-u_wm))) / 2;
  const Real Hko = (1 + tanh(k_so * (u-u_so))) / 2;
  const Real Hks = (1 + tanh(k_s * (u-u_s))) / 2;

  const Real tau_vm = tau_v1m + Hthvm*(tau_v2m-tau_v1m);
  const Real tau_wm = tau_w1m + (tau_w2m-tau_w1m)*Hkm;
  const Real tau_so = tau_so1 + (tau_so2-tau_so1)*Hko;
  const Real tau_s = tau_s1 + Hthw*(tau_s2-tau_s1);
  const Real tau_o = tau_o1 + Hth0*(tau_o2-tau_o1);

  const Real vinf = 1 - Hthvm;
  const Real winf = (1-Hth0)*(1-u/tau_winf) + Hth0*w_infstar;

  const Real Jfi = -v*Hthv*(u-theta_v)*(u_u-u)/tau_fi;
  const Real Jso = (theta_w>u) ? (u-u0)/tau_o : 1.0/tau_so;
  const Real Jsi = -Hthw*w*s/tau_si;

  const Real U = -(Jfi + Jso + Jsi);
  const Real V = (theta_v>u) ? (vinf-v)/tau_vm : - v/tau_vp;
  const Real W = (theta_w>u) ? (winf-w)/tau_wm : - w/tau_wp;
  const Real S = (Hks-s)/tau_s;

  *_new_u = u + dt * (U + _diffuse_u);
  *_new_v = v + dt * V;
  *_new_w = w + dt * W;
  *_new_s = s + dt * S;
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_bueno2008minimal_kernel(
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
      if (model_id == Model_bueno2008minimal_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_bueno2008minimal_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
