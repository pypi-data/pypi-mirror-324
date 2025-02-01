#ifndef __OPENCL_VERSION__
const std::string Model_paci2013atrial_info = R"model(
paci2013atrial:
  name: Paci et al. 2014 (Atrial)
  description: ''
  dois:
  - https://doi.org/10.1007/s10439-013-0833-3
  variables:
    Vm: -0.068733823452164
    m: 0.141183142078492
    h: 0.642108593994587
    j: 0.173566329483423
    d: 0.000127632520741878
    f1: 0.98038400433601
    f2: 0.999953006710394
    fCa: 0.997346890768643
    Xr1: 0.0257889110986083
    Xr2: 0.405046678739985
    Xs: 0.0447460799149437
    Xf: 0.0607988713874682
    q: 0.776163826643278
    r: 0.000503296941001262
    Nai: 14.4424010544424
    Cai: 4.49232909234503e-05
    Ca_SR: 0.149980051221604
    g: 1.0
  parameters:
    diffusivity_Vm: 1.0
    environment_time: 0.0
    i_CaL_f2_gate_constf2: 2.0
    i_CaL_fCa_gate_tau_fCa: 0.002
    i_PCa_KPCa: 0.0005
    i_PCa_g_PCa: 0.4125
    i_f_E_f: -0.017
    i_f_g_f: 30.10312
    model_parameters_Cao: 1.8
    model_parameters_Cm: 7.86671e-11
    model_parameters_F: 96485.3415
    model_parameters_Ki: 150.0
    model_parameters_Ko: 5.4
    model_parameters_Nao: 151.0
    model_parameters_R: 8.314472
    model_parameters_T: 310.0
    model_parameters_V_SR: 465.2
    model_parameters_Vc: 7012.0
    electric_potentials_E_K: -0.08880285397707481
    electric_potentials_PkNa: 0.03
    i_CaL_g_CaL: 8.635702e-05
    i_Kr_Xr1_gate_L0: 0.025
    i_Kr_Xr1_gate_Q: 2.3
    i_Kr_Xr1_gate_V_half: -20.69505995297709
    i_NaCa_KmCa: 1.38
    i_NaCa_KmNai: 87.5
    i_NaCa_Ksat: 0.1
    i_NaCa_alpha: 2.8571432
    i_NaCa_gamma: 0.35
    i_NaCa_kNaCa: 2450.0
    i_NaK_Km_K: 1.0
    i_NaK_Km_Na: 40.0
    i_NaK_PNaK: 1.4731392
    i_K1_g_K1: 19.1925
    i_Kr_g_Kr: 29.8667
    i_Ks_g_Ks: 2.041
    i_Na_g_Na: 6646.185
    i_b_Ca_g_b_Ca: 0.69264
    i_b_Na_g_b_Na: 0.9
    i_to_g_to: 59.8077
    calcium_dynamics_Buf_C: 0.25
    calcium_dynamics_Buf_SR: 10.0
    calcium_dynamics_Kbuf_C: 0.001
    calcium_dynamics_Kbuf_SR: 0.3
    calcium_dynamics_Kup: 0.00025
    calcium_dynamics_V_leak: 0.00044444
    calcium_dynamics_VmaxUp: 0.22
    calcium_dynamics_a_rel: 16.464
    calcium_dynamics_b_rel: 0.25
    calcium_dynamics_c_rel: 8.232
    calcium_dynamics_tau_g: 0.002
  key: paci2013atrial
)model";
#endif

static const Size Model_paci2013atrial_id = UNIQUE_ID;
static const Size Model_paci2013atrial_Nv = 18;
static const Size Model_paci2013atrial_Np = 51;

#ifdef __OPENCL_VERSION__
void Model_paci2013atrial_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_Vm = params[0];
  const Real environment_time = params[1];
  const Real i_CaL_f2_gate_constf2 = params[2];
  const Real i_CaL_fCa_gate_tau_fCa = params[3];
  const Real i_PCa_KPCa = params[4];
  const Real i_PCa_g_PCa = params[5];
  const Real i_f_E_f = params[6];
  const Real i_f_g_f = params[7];
  const Real model_parameters_Cao = params[8];
  const Real model_parameters_Cm = params[9];
  const Real model_parameters_F = params[10];
  const Real model_parameters_Ki = params[11];
  const Real model_parameters_Ko = params[12];
  const Real model_parameters_Nao = params[13];
  const Real model_parameters_R = params[14];
  const Real model_parameters_T = params[15];
  const Real model_parameters_V_SR = params[16];
  const Real model_parameters_Vc = params[17];
  const Real electric_potentials_E_K = params[18];
  const Real electric_potentials_PkNa = params[19];
  const Real i_CaL_g_CaL = params[20];
  const Real i_Kr_Xr1_gate_L0 = params[21];
  const Real i_Kr_Xr1_gate_Q = params[22];
  const Real i_Kr_Xr1_gate_V_half = params[23];
  const Real i_NaCa_KmCa = params[24];
  const Real i_NaCa_KmNai = params[25];
  const Real i_NaCa_Ksat = params[26];
  const Real i_NaCa_alpha = params[27];
  const Real i_NaCa_gamma = params[28];
  const Real i_NaCa_kNaCa = params[29];
  const Real i_NaK_Km_K = params[30];
  const Real i_NaK_Km_Na = params[31];
  const Real i_NaK_PNaK = params[32];
  const Real i_K1_g_K1 = params[33];
  const Real i_Kr_g_Kr = params[34];
  const Real i_Ks_g_Ks = params[35];
  const Real i_Na_g_Na = params[36];
  const Real i_b_Ca_g_b_Ca = params[37];
  const Real i_b_Na_g_b_Na = params[38];
  const Real i_to_g_to = params[39];
  const Real calcium_dynamics_Buf_C = params[40];
  const Real calcium_dynamics_Buf_SR = params[41];
  const Real calcium_dynamics_Kbuf_C = params[42];
  const Real calcium_dynamics_Kbuf_SR = params[43];
  const Real calcium_dynamics_Kup = params[44];
  const Real calcium_dynamics_V_leak = params[45];
  const Real calcium_dynamics_VmaxUp = params[46];
  const Real calcium_dynamics_a_rel = params[47];
  const Real calcium_dynamics_b_rel = params[48];
  const Real calcium_dynamics_c_rel = params[49];
  const Real calcium_dynamics_tau_g = params[50];
  const Real Vm = _r(_v(0, states_old));
  Real* const _new_Vm = _pr(_v(0, states_new));
  const Real _diffuse_Vm = diffusivity_Vm * diffuse(weights, _v(0, states_old));
  const Real m = _r(_v(1, states_old));
  Real* const _new_m = _pr(_v(1, states_new));
  const Real h = _r(_v(2, states_old));
  Real* const _new_h = _pr(_v(2, states_new));
  const Real j = _r(_v(3, states_old));
  Real* const _new_j = _pr(_v(3, states_new));
  const Real d = _r(_v(4, states_old));
  Real* const _new_d = _pr(_v(4, states_new));
  const Real f1 = _r(_v(5, states_old));
  Real* const _new_f1 = _pr(_v(5, states_new));
  const Real f2 = _r(_v(6, states_old));
  Real* const _new_f2 = _pr(_v(6, states_new));
  const Real fCa = _r(_v(7, states_old));
  Real* const _new_fCa = _pr(_v(7, states_new));
  const Real Xr1 = _r(_v(8, states_old));
  Real* const _new_Xr1 = _pr(_v(8, states_new));
  const Real Xr2 = _r(_v(9, states_old));
  Real* const _new_Xr2 = _pr(_v(9, states_new));
  const Real Xs = _r(_v(10, states_old));
  Real* const _new_Xs = _pr(_v(10, states_new));
  const Real Xf = _r(_v(11, states_old));
  Real* const _new_Xf = _pr(_v(11, states_new));
  const Real q = _r(_v(12, states_old));
  Real* const _new_q = _pr(_v(12, states_new));
  const Real r = _r(_v(13, states_old));
  Real* const _new_r = _pr(_v(13, states_new));
  const Real Nai = _r(_v(14, states_old));
  Real* const _new_Nai = _pr(_v(14, states_new));
  const Real Cai = _r(_v(15, states_old));
  Real* const _new_Cai = _pr(_v(15, states_new));
  const Real Ca_SR = _r(_v(16, states_old));
  Real* const _new_Ca_SR = _pr(_v(16, states_new));
  const Real g = _r(_v(17, states_old));
  Real* const _new_g = _pr(_v(17, states_new));

  // i_CaL_d_gate
  const Real i_CaL_d_gate_alpha_d = 0.25 + 1.4 / (1.0 + exp((-Vm * 1000.0 - 35.0) / 13.0));
  const Real i_CaL_d_gate_beta_d = 1.4 / (1.0 + exp((Vm * 1000.0 + 5.0) / 5.0));
  const Real i_CaL_d_gate_d_infinity = 1.0 / (1.0 + exp(-(Vm * 1000.0 + 5.986) / 7.0));
  const Real i_CaL_d_gate_gamma_d = 1.0 / (1.0 + exp((-Vm * 1000.0 + 50.0) / 20.0));
  const Real i_CaL_d_gate_tau_d = (i_CaL_d_gate_alpha_d * i_CaL_d_gate_beta_d + i_CaL_d_gate_gamma_d) * 1.0 / 1000.0;
  *_new_d = d + dt*((i_CaL_d_gate_d_infinity - d) / i_CaL_d_gate_tau_d);

  // i_CaL_f1_gate
  const Real i_CaL_f1_gate_f1_inf = 1.0 / (1.0 + exp((Vm * 1000.0 + 25.226) / 3.0));
  const Real i_CaL_f1_gate_constf1 = ((i_CaL_f1_gate_f1_inf - f1 > 0.0) ? 1.0 + 1433.0 * (Cai - 50.0 * 1e-06) : 1.0);
  const Real i_CaL_f1_gate_tau_f1 = (20.0 + (1102.5 * exp(-pow(pow(Vm * 1000.0 + 27.0, 2.0) / 15.0, 2.0)) + (200.0 / (1.0 + exp((13.0 - Vm * 1000.0) / 10.0)) + 180.0 / (1.0 + exp((30.0 + Vm * 1000.0) / 10.0))))) * i_CaL_f1_gate_constf1 / 1000.0;
  *_new_f1 = f1 + dt*((i_CaL_f1_gate_f1_inf - f1) / i_CaL_f1_gate_tau_f1);

  // i_CaL_f2_gate
  const Real i_CaL_f2_gate_f2_inf = 0.33 + 0.67 / (1.0 + exp((Vm * 1000.0 + 31.226) / 4.0));
  const Real i_CaL_f2_gate_tau_f2 = (600.0 * exp(-pow(Vm * 1000.0 + 25.0, 2.0) / 170.0) + (31.0 / (1.0 + exp((25.0 - Vm * 1000.0) / 10.0)) + 16.0 / (1.0 + exp((30.0 + Vm * 1000.0) / 10.0)))) * i_CaL_f2_gate_constf2 / 1000.0;
  *_new_f2 = f2 + dt*((i_CaL_f2_gate_f2_inf - f2) / i_CaL_f2_gate_tau_f2);

  // i_CaL_fCa_gate
  const Real i_CaL_fCa_gate_alpha_fCa = 1.0 / (1.0 + pow(Cai / 0.0006, 8.0));
  const Real i_CaL_fCa_gate_beta_fCa = 0.1 / (1.0 + exp((Cai - 0.0009) / 0.0001));
  const Real i_CaL_fCa_gate_gamma_fCa = 0.3 / (1.0 + exp((Cai - 0.00075) / 0.0008));
  const Real i_CaL_fCa_gate_fCa_inf = (i_CaL_fCa_gate_alpha_fCa + (i_CaL_fCa_gate_beta_fCa + i_CaL_fCa_gate_gamma_fCa)) / 1.3156;
  const Real i_CaL_fCa_gate_constfCa = (((Vm > -0.06) && (i_CaL_fCa_gate_fCa_inf > fCa)) ? 0.0 : 1.0);
  *_new_fCa = fCa + dt*(i_CaL_fCa_gate_constfCa * (i_CaL_fCa_gate_fCa_inf - fCa) / i_CaL_fCa_gate_tau_fCa);

  // i_Kr_Xr2_gate
  const Real i_Kr_Xr2_gate_Xr2_infinity = 1.0 / (1.0 + exp((Vm * 1000.0 + 88.0) / 50.0));
  const Real i_Kr_Xr2_gate_alpha_Xr2 = 3.0 / (1.0 + exp((-60.0 - Vm * 1000.0) / 20.0));
  const Real i_Kr_Xr2_gate_beta_Xr2 = 1.12 / (1.0 + exp((-60.0 + Vm * 1000.0) / 20.0));
  const Real i_Kr_Xr2_gate_tau_Xr2 = 1.0 * (i_Kr_Xr2_gate_alpha_Xr2 * i_Kr_Xr2_gate_beta_Xr2) / 1000.0;
  *_new_Xr2 = Xr2 + dt*((i_Kr_Xr2_gate_Xr2_infinity - Xr2) / i_Kr_Xr2_gate_tau_Xr2);

  // i_Ks_Xs_gate
  const Real i_Ks_Xs_gate_Xs_infinity = 1.0 / (1.0 + exp((-Vm * 1000.0 - 20.0) / 16.0));
  const Real i_Ks_Xs_gate_alpha_Xs = 1100.0 / sqrt(1.0 + exp((-10.0 - Vm * 1000.0) / 6.0));
  const Real i_Ks_Xs_gate_beta_Xs = 1.0 / (1.0 + exp((-60.0 + Vm * 1000.0) / 20.0));
  const Real i_Ks_Xs_gate_tau_Xs = 1.0 * (i_Ks_Xs_gate_alpha_Xs * i_Ks_Xs_gate_beta_Xs) / 1000.0;
  *_new_Xs = Xs + dt*((i_Ks_Xs_gate_Xs_infinity - Xs) / i_Ks_Xs_gate_tau_Xs);

  // i_Na_h_gate
  const Real i_Na_h_gate_alpha_h = ((Vm < -0.04) ? 0.057 * exp(-(Vm * 1000.0 + 80.0) / 6.8) : 0.0);
  const Real i_Na_h_gate_beta_h = ((Vm < -0.04) ? 2.7 * exp(0.079 * (Vm * 1000.0)) + 3.1 * (pow(10.0, 5.0) * exp(0.3485 * (Vm * 1000.0))) : 0.77 / (0.13 * (1.0 + exp((Vm * 1000.0 + 10.66) / -11.1))));
  const Real i_Na_h_gate_h_inf = 1.0 / sqrt(1.0 + exp((Vm * 1000.0 + 72.1) / 5.7));
  const Real i_Na_h_gate_tau_h = ((Vm < -0.04) ? 1.5 / ((i_Na_h_gate_alpha_h + i_Na_h_gate_beta_h) * 1000.0) : 2.542 / 1000.0);
  *_new_h = h + dt*((i_Na_h_gate_h_inf - h) / i_Na_h_gate_tau_h);

  // i_Na_j_gate
  const Real i_Na_j_gate_alpha_j = ((Vm < -0.04) ? (-25428.0 * exp(0.2444 * (Vm * 1000.0)) - 6.948 * (pow(10.0, -6.0) * exp(-0.04391 * (Vm * 1000.0)))) * (Vm * 1000.0 + 37.78) / (1.0 + exp(0.311 * (Vm * 1000.0 + 79.23))) : 0.0);
  const Real i_Na_j_gate_beta_j = ((Vm < -0.04) ? 0.02424 * exp(-0.01052 * (Vm * 1000.0)) / (1.0 + exp(-0.1378 * (Vm * 1000.0 + 40.14))) : 0.6 * exp(0.057 * (Vm * 1000.0)) / (1.0 + exp(-0.1 * (Vm * 1000.0 + 32.0))));
  const Real i_Na_j_gate_j_inf = 1.0 / sqrt(1.0 + exp((Vm * 1000.0 + 72.1) / 5.7));
  const Real i_Na_j_gate_tau_j = 7.0 / ((i_Na_j_gate_alpha_j + i_Na_j_gate_beta_j) * 1000.0);
  *_new_j = j + dt*((i_Na_j_gate_j_inf - j) / i_Na_j_gate_tau_j);

  // i_Na_m_gate
  const Real i_Na_m_gate_alpha_m = 1.0 / (1.0 + exp((-Vm * 1000.0 - 60.0) / 5.0));
  const Real i_Na_m_gate_beta_m = 0.1 / (1.0 + exp((Vm * 1000.0 + 35.0) / 5.0)) + 0.1 / (1.0 + exp((Vm * 1000.0 - 50.0) / 200.0));
  const Real i_Na_m_gate_m_inf = 1.0 / pow(1.0 + exp((-Vm * 1000.0 - 34.1) / 5.9), 1.0 / 3.0);
  const Real i_Na_m_gate_tau_m = 1.0 * (i_Na_m_gate_alpha_m * i_Na_m_gate_beta_m) / 1000.0;
  *_new_m = m + dt*((i_Na_m_gate_m_inf - m) / i_Na_m_gate_tau_m);

  // i_PCa
  const Real i_PCa_i_PCa = i_PCa_g_PCa * Cai / (Cai + i_PCa_KPCa);

  // i_f
  const Real i_f_i_f = i_f_g_f * (Xf * (Vm - i_f_E_f));

  // i_f_Xf_gate
  const Real i_f_Xf_gate_Xf_infinity = 1.0 / (1.0 + exp((Vm * 1000.0 + 77.85) / 5.0));
  const Real i_f_Xf_gate_tau_Xf = 1900.0 / (1.0 + exp((Vm * 1000.0 + 15.0) / 10.0)) / 1000.0;
  *_new_Xf = Xf + dt*((i_f_Xf_gate_Xf_infinity - Xf) / i_f_Xf_gate_tau_Xf);

  // i_to_q_gate
  const Real i_to_q_gate_q_inf = 1.0 / (1.0 + exp((Vm * 1000.0 + 53.0) / 13.0));
  const Real i_to_q_gate_tau_q = (6.06 + 39.102 / (0.57 * exp(-0.08 * (Vm * 1000.0 + 44.0)) + 0.065 * exp(0.1 * (Vm * 1000.0 + 45.93)))) / 1000.0;
  *_new_q = q + dt*((i_to_q_gate_q_inf - q) / i_to_q_gate_tau_q);

  // i_to_r_gate
  const Real i_to_r_gate_r_inf = 1.0 / (1.0 + exp(-(Vm * 1000.0 - 22.3) / 18.75));
  const Real i_to_r_gate_tau_r = (2.75352 + 14.40516 / (1.037 * exp(0.09 * (Vm * 1000.0 + 30.61)) + 0.369 * exp(-0.12 * (Vm * 1000.0 + 23.84)))) / 1000.0;
  *_new_r = r + dt*((i_to_r_gate_r_inf - r) / i_to_r_gate_tau_r);

  // electric_potentials
  const Real electric_potentials_E_Ca = 0.5 * (model_parameters_R * model_parameters_T) / model_parameters_F * log(model_parameters_Cao / Cai);
  const Real electric_potentials_E_Na = model_parameters_R * model_parameters_T / model_parameters_F * log(model_parameters_Nao / Nai);
  const Real electric_potentials_E_Ks = model_parameters_R * model_parameters_T / model_parameters_F * log((model_parameters_Ko + electric_potentials_PkNa * model_parameters_Nao) / (model_parameters_Ki + electric_potentials_PkNa * Nai));

  // i_CaL
  const Real i_CaL_i_CaL = i_CaL_g_CaL * (4.0 * (Vm * pow(model_parameters_F, 2.0))) / (model_parameters_R * model_parameters_T) * (Cai * exp(2.0 * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) - 0.341 * model_parameters_Cao) / (exp(2.0 * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) - 1.0) * (d * (f1 * (f2 * fCa)));

  // i_Kr_Xr1_gate
  const Real i_Kr_Xr1_gate_alpha_Xr1 = 450.0 / (1.0 + exp((-45.0 - Vm * 1000.0) / 10.0));
  const Real i_Kr_Xr1_gate_beta_Xr1 = 6.0 / (1.0 + exp((30.0 + Vm * 1000.0) / 11.5));
  const Real i_Kr_Xr1_gate_tau_Xr1 = 1.0 * (i_Kr_Xr1_gate_alpha_Xr1 * i_Kr_Xr1_gate_beta_Xr1) / 1000.0;
  const Real i_Kr_Xr1_gate_Xr1_inf = 1.0 / (1.0 + exp((i_Kr_Xr1_gate_V_half - Vm * 1000.0) / 4.9));
  *_new_Xr1 = Xr1 + dt*((i_Kr_Xr1_gate_Xr1_inf - Xr1) / i_Kr_Xr1_gate_tau_Xr1);

  // i_NaCa
  const Real i_NaCa_i_NaCa = i_NaCa_kNaCa * (exp(i_NaCa_gamma * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) * (pow(Nai, 3.0) * model_parameters_Cao) - exp((i_NaCa_gamma - 1.0) * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) * (pow(model_parameters_Nao, 3.0) * (Cai * i_NaCa_alpha))) / ((pow(i_NaCa_KmNai, 3.0) + pow(model_parameters_Nao, 3.0)) * ((i_NaCa_KmCa + model_parameters_Cao) * (1.0 + i_NaCa_Ksat * exp((i_NaCa_gamma - 1.0) * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)))));

  // i_NaK
  const Real i_NaK_i_NaK = i_NaK_PNaK * model_parameters_Ko / (model_parameters_Ko + i_NaK_Km_K) * Nai / (Nai + i_NaK_Km_Na) / (1.0 + (0.1245 * exp(-0.1 * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) + 0.0353 * exp(-Vm * model_parameters_F / (model_parameters_R * model_parameters_T))));

  // i_K1
  const Real i_K1_alpha_K1 = 3.91 / (1.0 + exp(0.5942 * (Vm * 1000.0 - electric_potentials_E_K * 1000.0 - 200.0)));
  const Real i_K1_beta_K1 = (-1.509 * exp(0.0002 * (Vm * 1000.0 - electric_potentials_E_K * 1000.0 + 100.0)) + exp(0.5886 * (Vm * 1000.0 - electric_potentials_E_K * 1000.0 - 10.0))) / (1.0 + exp(0.4547 * (Vm * 1000.0 - electric_potentials_E_K * 1000.0)));
  const Real i_K1_XK1_inf = i_K1_alpha_K1 / (i_K1_alpha_K1 + i_K1_beta_K1);
  const Real i_K1_i_K1 = i_K1_g_K1 * (i_K1_XK1_inf * ((Vm - electric_potentials_E_K) * sqrt(model_parameters_Ko / 5.4)));

  // i_Kr
  const Real i_Kr_i_Kr = i_Kr_g_Kr * ((Vm - electric_potentials_E_K) * (Xr1 * (Xr2 * sqrt(model_parameters_Ko / 5.4))));

  // i_Ks
  const Real i_Ks_i_Ks = i_Ks_g_Ks * ((Vm - electric_potentials_E_Ks) * (pow(Xs, 2.0) * (1.0 + 0.6 / (1.0 + pow(3.8 * 1e-05 / Cai, 1.4)))));

  // i_Na
  const Real i_Na_i_Na = i_Na_g_Na * (pow(m, 3.0) * (h * (j * (Vm - electric_potentials_E_Na))));

  // i_b_Ca
  const Real i_b_Ca_i_b_Ca = i_b_Ca_g_b_Ca * (Vm - electric_potentials_E_Ca);

  // i_b_Na
  const Real i_b_Na_i_b_Na = i_b_Na_g_b_Na * (Vm - electric_potentials_E_Na);

  // i_to
  const Real i_to_i_to = i_to_g_to * ((Vm - electric_potentials_E_K) * (q * r));

  // Membrane
  *_new_Vm = Vm + dt*(-(i_K1_i_K1 + (i_to_i_to + (i_Kr_i_Kr + (i_Ks_i_Ks + (i_CaL_i_CaL + (i_NaK_i_NaK + (i_Na_i_Na + (i_NaCa_i_NaCa + (i_PCa_i_PCa + (i_f_i_f + (i_b_Na_i_b_Na + i_b_Ca_i_b_Ca))))))))))) + _diffuse_Vm);

  // calcium_dynamics
  const Real calcium_dynamics_g_inf = ((Cai <= 0.00035) ? 1.0 / (1.0 + pow(Cai / 0.00035, 6.0)) : 1.0 / (1.0 + pow(Cai / 0.00035, 16.0)));
  const Real calcium_dynamics_Ca_SR_bufSR = 1.0 / (1.0 + calcium_dynamics_Buf_SR * calcium_dynamics_Kbuf_SR / pow(Ca_SR + calcium_dynamics_Kbuf_SR, 2.0));
  const Real calcium_dynamics_Cai_bufc = 1.0 / (1.0 + calcium_dynamics_Buf_C * calcium_dynamics_Kbuf_C / pow(Cai + calcium_dynamics_Kbuf_C, 2.0));
  const Real calcium_dynamics_const2 = (((calcium_dynamics_g_inf > g) && (Vm > -0.06)) ? 0.0 : 1.0);
  const Real calcium_dynamics_i_leak = (Ca_SR - Cai) * calcium_dynamics_V_leak;
  const Real calcium_dynamics_i_rel = (calcium_dynamics_c_rel + calcium_dynamics_a_rel * pow(Ca_SR, 2.0) / (pow(calcium_dynamics_b_rel, 2.0) + pow(Ca_SR, 2.0))) * (d * (g * 0.0556));
  const Real calcium_dynamics_i_up = calcium_dynamics_VmaxUp / (1.0 + pow(calcium_dynamics_Kup, 2.0) / pow(Cai, 2.0));
  *_new_Ca_SR = Ca_SR + dt*(calcium_dynamics_Ca_SR_bufSR * model_parameters_Vc / model_parameters_V_SR * (calcium_dynamics_i_up - (calcium_dynamics_i_rel + calcium_dynamics_i_leak)));
  *_new_Cai = Cai + dt*(calcium_dynamics_Cai_bufc * (calcium_dynamics_i_leak - calcium_dynamics_i_up + calcium_dynamics_i_rel - (i_CaL_i_CaL + (i_b_Ca_i_b_Ca + i_PCa_i_PCa) - 2.0 * i_NaCa_i_NaCa) * model_parameters_Cm / (2.0 * (model_parameters_Vc * (model_parameters_F * 1e-18)))));
  *_new_g = g + dt*(calcium_dynamics_const2 * (calcium_dynamics_g_inf - g) / calcium_dynamics_tau_g);

  // sodium_dynamics
  *_new_Nai = Nai + dt*(-model_parameters_Cm * (i_Na_i_Na + (i_b_Na_i_b_Na + (3.0 * i_NaK_i_NaK + 3.0 * i_NaCa_i_NaCa))) / (model_parameters_F * (model_parameters_Vc * 1e-18)));
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_paci2013atrial_kernel(
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
      if (model_id == Model_paci2013atrial_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_paci2013atrial_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
