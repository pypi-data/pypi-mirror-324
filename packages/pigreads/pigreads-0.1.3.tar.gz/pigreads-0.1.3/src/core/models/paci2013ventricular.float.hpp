#ifndef __OPENCL_VERSION__
const std::string Model_paci2013ventricular_info = R"model(
paci2013ventricular:
  name: Paci et al. 2014 (Ventricular)
  description: ''
  dois:
  - https://doi.org/10.1007/s10439-013-0833-3
  variables:
    Vm: -0.0743340057623841
    m: 0.102953468725004
    h: 0.786926637881461
    j: 0.253943221774722
    d: 8.96088425225182e-05
    f1: 0.970411811263976
    f2: 0.999965815466749
    fCa: 0.998925296531804
    Xr1: 0.00778547011240132
    Xr2: 0.432162576531617
    Xs: 0.0322944866983666
    Xf: 0.100615100568753
    q: 0.839295925773219
    r: 0.00573289893326379
    Nai: 10.9248496211574
    Cai: 1.80773974140477e-05
    Ca_SR: 0.2734234751931
    g: 0.999999981028517
  parameters:
    diffusivity_Vm: 1.0
    current_blockers_Chromanol_iKs30: 0.0
    current_blockers_Chromanol_iKs50: 0.0
    current_blockers_Chromanol_iKs70: 0.0
    current_blockers_Chromanol_iKs90: 0.0
    current_blockers_E4031_100nM: 0.0
    current_blockers_E4031_30nM: 0.0
    current_blockers_TTX_10uM: 0.0
    current_blockers_TTX_30uM: 0.0
    current_blockers_TTX_3uM: 0.0
    current_blockers_nifed_100nM: 0.0
    current_blockers_nifed_10nM: 0.0
    current_blockers_nifed_30nM: 0.0
    current_blockers_nifed_3nM: 0.0
    environment_time: 0.0
    i_CaL_f2_gate_constf2: 1.0
    i_CaL_fCa_gate_tau_fCa: 0.002
    i_PCa_KPCa: 0.0005
    i_PCa_g_PCa: 0.4125
    i_f_E_f: -0.017
    i_f_g_f: 30.10312
    model_parameters_Cao: 1.8
    model_parameters_Cm: 9.87109e-11
    model_parameters_F: 96485.3415
    model_parameters_Ki: 150.0
    model_parameters_Ko: 5.4
    model_parameters_Nao: 151.0
    model_parameters_R: 8.314472
    model_parameters_T: 310.0
    model_parameters_V_SR: 583.73
    model_parameters_Vc: 8800.0
    electric_potentials_E_K: -0.08880285397707481
    electric_potentials_PkNa: 0.03
    i_CaL_g_CaL: 8.635702e-05
    i_CaL_nifed_coeff: 1.0
    i_Kr_Xr1_gate_L0: 0.025
    i_Kr_Xr1_gate_Q: 2.3
    i_Kr_Xr1_gate_V_half: -20.69505995297709
    i_NaCa_KmCa: 1.38
    i_NaCa_KmNai: 87.5
    i_NaCa_Ksat: 0.1
    i_NaCa_alpha: 2.8571432
    i_NaCa_gamma: 0.35
    i_NaCa_kNaCa: 4900.0
    i_NaK_Km_K: 1.0
    i_NaK_Km_Na: 40.0
    i_NaK_PNaK: 1.841424
    stim_mode_i_stim_Amplitude: 5.5e-10
    stim_mode_i_stim_End: 800.0
    stim_mode_i_stim_frequency: 60.0
    stim_mode_pace: 0.0
    stim_mode_stim_flag: 0.0
    i_K1_g_K1: 28.1492
    i_Kr_E4031_coeff: 1.0
    i_Kr_g_Kr: 29.8667
    i_Ks_Chromanol_coeff: 1.0
    i_Ks_g_Ks: 2.041
    i_Na_TTX_coeff: 1.0
    i_Na_g_Na: 3671.2302
    i_b_Ca_g_b_Ca: 0.69264
    i_b_Na_g_b_Na: 0.9
    i_to_g_to: 29.9038
    calcium_dynamics_Buf_C: 0.25
    calcium_dynamics_Buf_SR: 10.0
    calcium_dynamics_Kbuf_C: 0.001
    calcium_dynamics_Kbuf_SR: 0.3
    calcium_dynamics_Kup: 0.00025
    calcium_dynamics_V_leak: 0.00044444
    calcium_dynamics_VmaxUp: 0.56064
    calcium_dynamics_a_rel: 16.464
    calcium_dynamics_b_rel: 0.25
    calcium_dynamics_c_rel: 8.232
    calcium_dynamics_tau_g: 0.002
  key: paci2013ventricular
)model";
#endif

static const Size Model_paci2013ventricular_id = UNIQUE_ID;
static const Size Model_paci2013ventricular_Nv = 18;
static const Size Model_paci2013ventricular_Np = 73;

#ifdef __OPENCL_VERSION__
void Model_paci2013ventricular_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_Vm = params[0];
  const Real current_blockers_Chromanol_iKs30 = params[1];
  const Real current_blockers_Chromanol_iKs50 = params[2];
  const Real current_blockers_Chromanol_iKs70 = params[3];
  const Real current_blockers_Chromanol_iKs90 = params[4];
  const Real current_blockers_E4031_100nM = params[5];
  const Real current_blockers_E4031_30nM = params[6];
  const Real current_blockers_TTX_10uM = params[7];
  const Real current_blockers_TTX_30uM = params[8];
  const Real current_blockers_TTX_3uM = params[9];
  const Real current_blockers_nifed_100nM = params[10];
  const Real current_blockers_nifed_10nM = params[11];
  const Real current_blockers_nifed_30nM = params[12];
  const Real current_blockers_nifed_3nM = params[13];
  const Real environment_time = params[14];
  const Real i_CaL_f2_gate_constf2 = params[15];
  const Real i_CaL_fCa_gate_tau_fCa = params[16];
  const Real i_PCa_KPCa = params[17];
  const Real i_PCa_g_PCa = params[18];
  const Real i_f_E_f = params[19];
  const Real i_f_g_f = params[20];
  const Real model_parameters_Cao = params[21];
  const Real model_parameters_Cm = params[22];
  const Real model_parameters_F = params[23];
  const Real model_parameters_Ki = params[24];
  const Real model_parameters_Ko = params[25];
  const Real model_parameters_Nao = params[26];
  const Real model_parameters_R = params[27];
  const Real model_parameters_T = params[28];
  const Real model_parameters_V_SR = params[29];
  const Real model_parameters_Vc = params[30];
  const Real electric_potentials_E_K = params[31];
  const Real electric_potentials_PkNa = params[32];
  const Real i_CaL_g_CaL = params[33];
  const Real i_CaL_nifed_coeff = params[34];
  const Real i_Kr_Xr1_gate_L0 = params[35];
  const Real i_Kr_Xr1_gate_Q = params[36];
  const Real i_Kr_Xr1_gate_V_half = params[37];
  const Real i_NaCa_KmCa = params[38];
  const Real i_NaCa_KmNai = params[39];
  const Real i_NaCa_Ksat = params[40];
  const Real i_NaCa_alpha = params[41];
  const Real i_NaCa_gamma = params[42];
  const Real i_NaCa_kNaCa = params[43];
  const Real i_NaK_Km_K = params[44];
  const Real i_NaK_Km_Na = params[45];
  const Real i_NaK_PNaK = params[46];
  const Real stim_mode_i_stim_Amplitude = params[47];
  const Real stim_mode_i_stim_End = params[48];
  const Real stim_mode_i_stim_frequency = params[49];
  const Real stim_mode_pace = params[50];
  const Real stim_mode_stim_flag = params[51];
  const Real i_K1_g_K1 = params[52];
  const Real i_Kr_E4031_coeff = params[53];
  const Real i_Kr_g_Kr = params[54];
  const Real i_Ks_Chromanol_coeff = params[55];
  const Real i_Ks_g_Ks = params[56];
  const Real i_Na_TTX_coeff = params[57];
  const Real i_Na_g_Na = params[58];
  const Real i_b_Ca_g_b_Ca = params[59];
  const Real i_b_Na_g_b_Na = params[60];
  const Real i_to_g_to = params[61];
  const Real calcium_dynamics_Buf_C = params[62];
  const Real calcium_dynamics_Buf_SR = params[63];
  const Real calcium_dynamics_Kbuf_C = params[64];
  const Real calcium_dynamics_Kbuf_SR = params[65];
  const Real calcium_dynamics_Kup = params[66];
  const Real calcium_dynamics_V_leak = params[67];
  const Real calcium_dynamics_VmaxUp = params[68];
  const Real calcium_dynamics_a_rel = params[69];
  const Real calcium_dynamics_b_rel = params[70];
  const Real calcium_dynamics_c_rel = params[71];
  const Real calcium_dynamics_tau_g = params[72];
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
  const Real i_CaL_d_gate_alpha_d = 0.25f + 1.4f / (1.0f + native_exp((-Vm * 1000.0f - 35.0f) / 13.0f));
  const Real i_CaL_d_gate_beta_d = 1.4f / (1.0f + native_exp((Vm * 1000.0f + 5.0f) / 5.0f));
  const Real i_CaL_d_gate_d_infinity = 1.0f / (1.0f + native_exp(-(Vm * 1000.0f + 9.1f) / 7.0f));
  const Real i_CaL_d_gate_gamma_d = 1.0f / (1.0f + native_exp((-Vm * 1000.0f + 50.0f) / 20.0f));
  const Real i_CaL_d_gate_tau_d = (i_CaL_d_gate_alpha_d * i_CaL_d_gate_beta_d + i_CaL_d_gate_gamma_d) * 1.0f / 1000.0f;
  *_new_d = d + dt*((i_CaL_d_gate_d_infinity - d) / i_CaL_d_gate_tau_d);

  // i_CaL_f1_gate
  const Real i_CaL_f1_gate_f1_inf = 1.0f / (1.0f + native_exp((Vm * 1000.0f + 26.0f) / 3.0f));
  const Real i_CaL_f1_gate_constf1 = ((i_CaL_f1_gate_f1_inf - f1 > 0.0f) ? 1.0f + 1433.0f * (Cai - 50.0f * 1e-06f) : 1.0f);
  const Real i_CaL_f1_gate_tau_f1 = (20.0f + (1102.5f * native_exp(-pow(pow(Vm * 1000.0f + 27.0f, 2.0f) / 15.0f, 2.0f)) + (200.0f / (1.0f + native_exp((13.0f - Vm * 1000.0f) / 10.0f)) + 180.0f / (1.0f + native_exp((30.0f + Vm * 1000.0f) / 10.0f))))) * i_CaL_f1_gate_constf1 / 1000.0f;
  *_new_f1 = f1 + dt*((i_CaL_f1_gate_f1_inf - f1) / i_CaL_f1_gate_tau_f1);

  // i_CaL_f2_gate
  const Real i_CaL_f2_gate_f2_inf = 0.33f + 0.67f / (1.0f + native_exp((Vm * 1000.0f + 35.0f) / 4.0f));
  const Real i_CaL_f2_gate_tau_f2 = (600.0f * native_exp(-pow(Vm * 1000.0f + 25.0f, 2.0f) / 170.0f) + (31.0f / (1.0f + native_exp((25.0f - Vm * 1000.0f) / 10.0f)) + 16.0f / (1.0f + native_exp((30.0f + Vm * 1000.0f) / 10.0f)))) * i_CaL_f2_gate_constf2 / 1000.0f;
  *_new_f2 = f2 + dt*((i_CaL_f2_gate_f2_inf - f2) / i_CaL_f2_gate_tau_f2);

  // i_CaL_fCa_gate
  const Real i_CaL_fCa_gate_alpha_fCa = 1.0f / (1.0f + pow(Cai / 0.0006f, 8.0f));
  const Real i_CaL_fCa_gate_beta_fCa = 0.1f / (1.0f + native_exp((Cai - 0.0009f) / 0.0001f));
  const Real i_CaL_fCa_gate_gamma_fCa = 0.3f / (1.0f + native_exp((Cai - 0.00075f) / 0.0008f));
  const Real i_CaL_fCa_gate_fCa_inf = (i_CaL_fCa_gate_alpha_fCa + (i_CaL_fCa_gate_beta_fCa + i_CaL_fCa_gate_gamma_fCa)) / 1.3156f;
  const Real i_CaL_fCa_gate_constfCa = (((Vm > -0.06f) && (i_CaL_fCa_gate_fCa_inf > fCa)) ? 0.0f : 1.0f);
  *_new_fCa = fCa + dt*(i_CaL_fCa_gate_constfCa * (i_CaL_fCa_gate_fCa_inf - fCa) / i_CaL_fCa_gate_tau_fCa);

  // i_Kr_Xr2_gate
  const Real i_Kr_Xr2_gate_Xr2_infinity = 1.0f / (1.0f + native_exp((Vm * 1000.0f + 88.0f) / 50.0f));
  const Real i_Kr_Xr2_gate_alpha_Xr2 = 3.0f / (1.0f + native_exp((-60.0f - Vm * 1000.0f) / 20.0f));
  const Real i_Kr_Xr2_gate_beta_Xr2 = 1.12f / (1.0f + native_exp((-60.0f + Vm * 1000.0f) / 20.0f));
  const Real i_Kr_Xr2_gate_tau_Xr2 = 1.0f * (i_Kr_Xr2_gate_alpha_Xr2 * i_Kr_Xr2_gate_beta_Xr2) / 1000.0f;
  *_new_Xr2 = Xr2 + dt*((i_Kr_Xr2_gate_Xr2_infinity - Xr2) / i_Kr_Xr2_gate_tau_Xr2);

  // i_Ks_Xs_gate
  const Real i_Ks_Xs_gate_Xs_infinity = 1.0f / (1.0f + native_exp((-Vm * 1000.0f - 20.0f) / 16.0f));
  const Real i_Ks_Xs_gate_alpha_Xs = 1100.0f / native_sqrt(1.0f + native_exp((-10.0f - Vm * 1000.0f) / 6.0f));
  const Real i_Ks_Xs_gate_beta_Xs = 1.0f / (1.0f + native_exp((-60.0f + Vm * 1000.0f) / 20.0f));
  const Real i_Ks_Xs_gate_tau_Xs = 1.0f * (i_Ks_Xs_gate_alpha_Xs * i_Ks_Xs_gate_beta_Xs) / 1000.0f;
  *_new_Xs = Xs + dt*((i_Ks_Xs_gate_Xs_infinity - Xs) / i_Ks_Xs_gate_tau_Xs);

  // i_Na_h_gate
  const Real i_Na_h_gate_alpha_h = ((Vm < -0.04f) ? 0.057f * native_exp(-(Vm * 1000.0f + 80.0f) / 6.8f) : 0.0f);
  const Real i_Na_h_gate_beta_h = ((Vm < -0.04f) ? 2.7f * native_exp(0.079f * (Vm * 1000.0f)) + 3.1f * (pow(10.0f, 5.0f) * native_exp(0.3485f * (Vm * 1000.0f))) : 0.77f / (0.13f * (1.0f + native_exp((Vm * 1000.0f + 10.66f) / -11.1f))));
  const Real i_Na_h_gate_h_inf = 1.0f / native_sqrt(1.0f + native_exp((Vm * 1000.0f + 72.1f) / 5.7f));
  const Real i_Na_h_gate_tau_h = ((Vm < -0.04f) ? 1.5f / ((i_Na_h_gate_alpha_h + i_Na_h_gate_beta_h) * 1000.0f) : 2.542f / 1000.0f);
  *_new_h = h + dt*((i_Na_h_gate_h_inf - h) / i_Na_h_gate_tau_h);

  // i_Na_j_gate
  const Real i_Na_j_gate_alpha_j = ((Vm < -0.04f) ? (-25428.0f * native_exp(0.2444f * (Vm * 1000.0f)) - 6.948f * (pow(10.0f, -6.0f) * native_exp(-0.04391f * (Vm * 1000.0f)))) * (Vm * 1000.0f + 37.78f) / (1.0f + native_exp(0.311f * (Vm * 1000.0f + 79.23f))) : 0.0f);
  const Real i_Na_j_gate_beta_j = ((Vm < -0.04f) ? 0.02424f * native_exp(-0.01052f * (Vm * 1000.0f)) / (1.0f + native_exp(-0.1378f * (Vm * 1000.0f + 40.14f))) : 0.6f * native_exp(0.057f * (Vm * 1000.0f)) / (1.0f + native_exp(-0.1f * (Vm * 1000.0f + 32.0f))));
  const Real i_Na_j_gate_j_inf = 1.0f / native_sqrt(1.0f + native_exp((Vm * 1000.0f + 72.1f) / 5.7f));
  const Real i_Na_j_gate_tau_j = 7.0f / ((i_Na_j_gate_alpha_j + i_Na_j_gate_beta_j) * 1000.0f);
  *_new_j = j + dt*((i_Na_j_gate_j_inf - j) / i_Na_j_gate_tau_j);

  // i_Na_m_gate
  const Real i_Na_m_gate_alpha_m = 1.0f / (1.0f + native_exp((-Vm * 1000.0f - 60.0f) / 5.0f));
  const Real i_Na_m_gate_beta_m = 0.1f / (1.0f + native_exp((Vm * 1000.0f + 35.0f) / 5.0f)) + 0.1f / (1.0f + native_exp((Vm * 1000.0f - 50.0f) / 200.0f));
  const Real i_Na_m_gate_m_inf = 1.0f / pow(1.0f + native_exp((-Vm * 1000.0f - 34.1f) / 5.9f), 1.0f / 3.0f);
  const Real i_Na_m_gate_tau_m = 1.0f * (i_Na_m_gate_alpha_m * i_Na_m_gate_beta_m) / 1000.0f;
  *_new_m = m + dt*((i_Na_m_gate_m_inf - m) / i_Na_m_gate_tau_m);

  // i_PCa
  const Real i_PCa_i_PCa = i_PCa_g_PCa * Cai / (Cai + i_PCa_KPCa);

  // i_f
  const Real i_f_i_f = i_f_g_f * (Xf * (Vm - i_f_E_f));

  // i_f_Xf_gate
  const Real i_f_Xf_gate_Xf_infinity = 1.0f / (1.0f + native_exp((Vm * 1000.0f + 77.85f) / 5.0f));
  const Real i_f_Xf_gate_tau_Xf = 1900.0f / (1.0f + native_exp((Vm * 1000.0f + 15.0f) / 10.0f)) / 1000.0f;
  *_new_Xf = Xf + dt*((i_f_Xf_gate_Xf_infinity - Xf) / i_f_Xf_gate_tau_Xf);

  // i_to_q_gate
  const Real i_to_q_gate_q_inf = 1.0f / (1.0f + native_exp((Vm * 1000.0f + 53.0f) / 13.0f));
  const Real i_to_q_gate_tau_q = (6.06f + 39.102f / (0.57f * native_exp(-0.08f * (Vm * 1000.0f + 44.0f)) + 0.065f * native_exp(0.1f * (Vm * 1000.0f + 45.93f)))) / 1000.0f;
  *_new_q = q + dt*((i_to_q_gate_q_inf - q) / i_to_q_gate_tau_q);

  // i_to_r_gate
  const Real i_to_r_gate_r_inf = 1.0f / (1.0f + native_exp(-(Vm * 1000.0f - 22.3f) / 18.75f));
  const Real i_to_r_gate_tau_r = (2.75352f + 14.40516f / (1.037f * native_exp(0.09f * (Vm * 1000.0f + 30.61f)) + 0.369f * native_exp(-0.12f * (Vm * 1000.0f + 23.84f)))) / 1000.0f;
  *_new_r = r + dt*((i_to_r_gate_r_inf - r) / i_to_r_gate_tau_r);

  // electric_potentials
  const Real electric_potentials_E_Ca = 0.5f * (model_parameters_R * model_parameters_T) / model_parameters_F * native_log(model_parameters_Cao / Cai);
  const Real electric_potentials_E_Na = model_parameters_R * model_parameters_T / model_parameters_F * native_log(model_parameters_Nao / Nai);
  const Real electric_potentials_E_Ks = model_parameters_R * model_parameters_T / model_parameters_F * native_log((model_parameters_Ko + electric_potentials_PkNa * model_parameters_Nao) / (model_parameters_Ki + electric_potentials_PkNa * Nai));

  // i_CaL
  const Real i_CaL_i_CaL = i_CaL_g_CaL * (4.0f * (Vm * pow(model_parameters_F, 2.0f))) / (model_parameters_R * model_parameters_T) * (Cai * native_exp(2.0f * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) - 0.341f * model_parameters_Cao) / (native_exp(2.0f * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) - 1.0f) * (d * (f1 * (f2 * fCa)));

  // i_Kr_Xr1_gate
  const Real i_Kr_Xr1_gate_alpha_Xr1 = 450.0f / (1.0f + native_exp((-45.0f - Vm * 1000.0f) / 10.0f));
  const Real i_Kr_Xr1_gate_beta_Xr1 = 6.0f / (1.0f + native_exp((30.0f + Vm * 1000.0f) / 11.5f));
  const Real i_Kr_Xr1_gate_tau_Xr1 = 1.0f * (i_Kr_Xr1_gate_alpha_Xr1 * i_Kr_Xr1_gate_beta_Xr1) / 1000.0f;
  const Real i_Kr_Xr1_gate_Xr1_inf = 1.0f / (1.0f + native_exp((i_Kr_Xr1_gate_V_half - Vm * 1000.0f) / 4.9f));
  *_new_Xr1 = Xr1 + dt*((i_Kr_Xr1_gate_Xr1_inf - Xr1) / i_Kr_Xr1_gate_tau_Xr1);

  // i_NaCa
  const Real i_NaCa_i_NaCa = i_NaCa_kNaCa * (native_exp(i_NaCa_gamma * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) * (pow(Nai, 3.0f) * model_parameters_Cao) - native_exp((i_NaCa_gamma - 1.0f) * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) * (pow(model_parameters_Nao, 3.0f) * (Cai * i_NaCa_alpha))) / ((pow(i_NaCa_KmNai, 3.0f) + pow(model_parameters_Nao, 3.0f)) * ((i_NaCa_KmCa + model_parameters_Cao) * (1.0f + i_NaCa_Ksat * native_exp((i_NaCa_gamma - 1.0f) * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)))));

  // i_NaK
  const Real i_NaK_i_NaK = i_NaK_PNaK * model_parameters_Ko / (model_parameters_Ko + i_NaK_Km_K) * Nai / (Nai + i_NaK_Km_Na) / (1.0f + (0.1245f * native_exp(-0.1f * (Vm * model_parameters_F) / (model_parameters_R * model_parameters_T)) + 0.0353f * native_exp(-Vm * model_parameters_F / (model_parameters_R * model_parameters_T))));

  // stim_mode
  const Real stim_mode_i_stim = stim_mode_pace * (stim_mode_stim_flag * stim_mode_i_stim_Amplitude / model_parameters_Cm);

  // i_K1
  const Real i_K1_alpha_K1 = 3.91f / (1.0f + native_exp(0.5942f * (Vm * 1000.0f - electric_potentials_E_K * 1000.0f - 200.0f)));
  const Real i_K1_beta_K1 = (-1.509f * native_exp(0.0002f * (Vm * 1000.0f - electric_potentials_E_K * 1000.0f + 100.0f)) + native_exp(0.5886f * (Vm * 1000.0f - electric_potentials_E_K * 1000.0f - 10.0f))) / (1.0f + native_exp(0.4547f * (Vm * 1000.0f - electric_potentials_E_K * 1000.0f)));
  const Real i_K1_XK1_inf = i_K1_alpha_K1 / (i_K1_alpha_K1 + i_K1_beta_K1);
  const Real i_K1_i_K1 = i_K1_g_K1 * (i_K1_XK1_inf * ((Vm - electric_potentials_E_K) * native_sqrt(model_parameters_Ko / 5.4f)));

  // i_Kr
  const Real i_Kr_i_Kr = i_Kr_E4031_coeff * (i_Kr_g_Kr * ((Vm - electric_potentials_E_K) * (Xr1 * (Xr2 * native_sqrt(model_parameters_Ko / 5.4f)))));

  // i_Ks
  const Real i_Ks_i_Ks = i_Ks_Chromanol_coeff * (i_Ks_g_Ks * ((Vm - electric_potentials_E_Ks) * (pow(Xs, 2.0f) * (1.0f + 0.6f / (1.0f + pow(3.8f * 1e-05f / Cai, 1.4f))))));

  // i_Na
  const Real i_Na_i_Na = i_Na_TTX_coeff * (i_Na_g_Na * (pow(m, 3.0f) * (h * (j * (Vm - electric_potentials_E_Na)))));

  // i_b_Ca
  const Real i_b_Ca_i_b_Ca = i_b_Ca_g_b_Ca * (Vm - electric_potentials_E_Ca);

  // i_b_Na
  const Real i_b_Na_i_b_Na = i_b_Na_g_b_Na * (Vm - electric_potentials_E_Na);

  // i_to
  const Real i_to_i_to = i_to_g_to * ((Vm - electric_potentials_E_K) * (q * r));

  // Membrane
  *_new_Vm = Vm + dt*(-(i_K1_i_K1 + (i_to_i_to + (i_Kr_i_Kr + (i_Ks_i_Ks + (i_CaL_i_CaL + (i_NaK_i_NaK + (i_Na_i_Na + (i_NaCa_i_NaCa + (i_PCa_i_PCa + (i_f_i_f + (i_b_Na_i_b_Na + i_b_Ca_i_b_Ca)))))))))) - stim_mode_i_stim) + _diffuse_Vm);

  // calcium_dynamics
  const Real calcium_dynamics_g_inf = ((Cai <= 0.00035f) ? 1.0f / (1.0f + pow(Cai / 0.00035f, 6.0f)) : 1.0f / (1.0f + pow(Cai / 0.00035f, 16.0f)));
  const Real calcium_dynamics_Ca_SR_bufSR = 1.0f / (1.0f + calcium_dynamics_Buf_SR * calcium_dynamics_Kbuf_SR / pow(Ca_SR + calcium_dynamics_Kbuf_SR, 2.0f));
  const Real calcium_dynamics_Cai_bufc = 1.0f / (1.0f + calcium_dynamics_Buf_C * calcium_dynamics_Kbuf_C / pow(Cai + calcium_dynamics_Kbuf_C, 2.0f));
  const Real calcium_dynamics_const2 = (((calcium_dynamics_g_inf > g) && (Vm > -0.06f)) ? 0.0f : 1.0f);
  const Real calcium_dynamics_i_leak = (Ca_SR - Cai) * calcium_dynamics_V_leak;
  const Real calcium_dynamics_i_rel = (calcium_dynamics_c_rel + calcium_dynamics_a_rel * pow(Ca_SR, 2.0f) / (pow(calcium_dynamics_b_rel, 2.0f) + pow(Ca_SR, 2.0f))) * (d * (g * 0.0411f));
  const Real calcium_dynamics_i_up = calcium_dynamics_VmaxUp / (1.0f + pow(calcium_dynamics_Kup, 2.0f) / pow(Cai, 2.0f));
  *_new_Ca_SR = Ca_SR + dt*(calcium_dynamics_Ca_SR_bufSR * model_parameters_Vc / model_parameters_V_SR * (calcium_dynamics_i_up - (calcium_dynamics_i_rel + calcium_dynamics_i_leak)));
  *_new_Cai = Cai + dt*(calcium_dynamics_Cai_bufc * (calcium_dynamics_i_leak - calcium_dynamics_i_up + calcium_dynamics_i_rel - (i_CaL_i_CaL + (i_b_Ca_i_b_Ca + i_PCa_i_PCa) - 2.0f * i_NaCa_i_NaCa) * model_parameters_Cm / (2.0f * (model_parameters_Vc * (model_parameters_F * 1e-18f)))));
  *_new_g = g + dt*(calcium_dynamics_const2 * (calcium_dynamics_g_inf - g) / calcium_dynamics_tau_g);

  // sodium_dynamics
  *_new_Nai = Nai + dt*(-model_parameters_Cm * (i_Na_i_Na + (i_b_Na_i_b_Na + (3.0f * i_NaK_i_NaK + 3.0f * i_NaCa_i_NaCa))) / (model_parameters_F * (model_parameters_Vc * 1e-18f)));
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_paci2013ventricular_kernel(
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
      if (model_id == Model_paci2013ventricular_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_paci2013ventricular_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
