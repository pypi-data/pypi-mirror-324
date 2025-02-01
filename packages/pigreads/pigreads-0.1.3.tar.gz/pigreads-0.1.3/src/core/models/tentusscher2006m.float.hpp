#ifndef __OPENCL_VERSION__
const std::string Model_tentusscher2006m_info = R"model(
tentusscher2006m:
  name: Ten Tusscher et al. 2004 (M)
  description: ''
  dois:
  - https://doi.org/10.1152/ajpheart.00794.2003
  variables:
    V: -85.423
    Xr1: 0.0165
    Xr2: 0.473
    Xs: 0.0174
    m: 0.00165
    h: 0.749
    j: 0.6788
    d: 3.288e-05
    f: 0.7026
    f2: 0.9526
    fCass: 0.9942
    s: 0.999998
    r: 2.347e-08
    Ca_i: 0.000153
    Ca_SR: 4.272
    Ca_ss: 0.00042
    R_prime: 0.8978
    Na_i: 10.132
    K_i: 138.52
  parameters:
    diffusivity_V: 1.0
    calcium_pump_current_K_pCa: 0.0005
    calcium_pump_current_g_pCa: 0.1238
    environment_time: 0.0
    L_type_Ca_current_g_CaL: 0.0398
    calcium_background_current_g_bca: 0.000592
    calcium_dynamics_Buf_c: 0.2
    calcium_dynamics_Buf_sr: 10.0
    calcium_dynamics_Buf_ss: 0.4
    calcium_dynamics_Ca_o: 2.0
    calcium_dynamics_EC: 1.5
    calcium_dynamics_K_buf_c: 0.001
    calcium_dynamics_K_buf_sr: 0.3
    calcium_dynamics_K_buf_ss: 0.00025
    calcium_dynamics_K_up: 0.00025
    calcium_dynamics_V_leak: 0.00036
    calcium_dynamics_V_rel: 0.102
    calcium_dynamics_V_sr: 1094.0
    calcium_dynamics_V_ss: 54.68
    calcium_dynamics_V_xfer: 0.0038
    calcium_dynamics_Vmax_up: 0.006375
    calcium_dynamics_k1_prime: 0.15
    calcium_dynamics_k2_prime: 0.045
    calcium_dynamics_k3: 0.06
    calcium_dynamics_k4: 0.005
    calcium_dynamics_max_sr: 2.5
    calcium_dynamics_min_sr: 1.0
    fast_sodium_current_g_Na: 14.838
    inward_rectifier_potassium_current_g_K1: 5.405
    membrane_Cm: 185.0
    membrane_F: 96.485
    membrane_R: 8.314
    membrane_T: 310.0
    membrane_V_c: 16404.0
    membrane_pace: 0.0
    membrane_stim_amplitude: -52.0
    potassium_dynamics_K_o: 5.4
    potassium_pump_current_g_pK: 0.0146
    rapid_time_dependent_potassium_current_g_Kr: 0.153
    reversal_potentials_P_kna: 0.03
    slow_time_dependent_potassium_current_g_Ks: 0.098
    sodium_background_current_g_bna: 0.00029
    sodium_calcium_exchanger_current_K_NaCa: 1000.0
    sodium_calcium_exchanger_current_K_sat: 0.1
    sodium_calcium_exchanger_current_Km_Ca: 1.38
    sodium_calcium_exchanger_current_Km_Nai: 87.5
    sodium_calcium_exchanger_current_alpha: 2.5
    sodium_calcium_exchanger_current_gamma: 0.35
    sodium_dynamics_Na_o: 140.0
    sodium_potassium_pump_current_K_mNa: 40.0
    sodium_potassium_pump_current_K_mk: 1.0
    sodium_potassium_pump_current_P_NaK: 2.724
    transient_outward_current_g_to: 0.294
  key: tentusscher2006m
)model";
#endif

static const Size Model_tentusscher2006m_id = UNIQUE_ID;
static const Size Model_tentusscher2006m_Nv = 19;
static const Size Model_tentusscher2006m_Np = 53;

#ifdef __OPENCL_VERSION__
void Model_tentusscher2006m_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_V = params[0];
  const Real calcium_pump_current_K_pCa = params[1];
  const Real calcium_pump_current_g_pCa = params[2];
  const Real environment_time = params[3];
  const Real L_type_Ca_current_g_CaL = params[4];
  const Real calcium_background_current_g_bca = params[5];
  const Real calcium_dynamics_Buf_c = params[6];
  const Real calcium_dynamics_Buf_sr = params[7];
  const Real calcium_dynamics_Buf_ss = params[8];
  const Real calcium_dynamics_Ca_o = params[9];
  const Real calcium_dynamics_EC = params[10];
  const Real calcium_dynamics_K_buf_c = params[11];
  const Real calcium_dynamics_K_buf_sr = params[12];
  const Real calcium_dynamics_K_buf_ss = params[13];
  const Real calcium_dynamics_K_up = params[14];
  const Real calcium_dynamics_V_leak = params[15];
  const Real calcium_dynamics_V_rel = params[16];
  const Real calcium_dynamics_V_sr = params[17];
  const Real calcium_dynamics_V_ss = params[18];
  const Real calcium_dynamics_V_xfer = params[19];
  const Real calcium_dynamics_Vmax_up = params[20];
  const Real calcium_dynamics_k1_prime = params[21];
  const Real calcium_dynamics_k2_prime = params[22];
  const Real calcium_dynamics_k3 = params[23];
  const Real calcium_dynamics_k4 = params[24];
  const Real calcium_dynamics_max_sr = params[25];
  const Real calcium_dynamics_min_sr = params[26];
  const Real fast_sodium_current_g_Na = params[27];
  const Real inward_rectifier_potassium_current_g_K1 = params[28];
  const Real membrane_Cm = params[29];
  const Real membrane_F = params[30];
  const Real membrane_R = params[31];
  const Real membrane_T = params[32];
  const Real membrane_V_c = params[33];
  const Real membrane_pace = params[34];
  const Real membrane_stim_amplitude = params[35];
  const Real potassium_dynamics_K_o = params[36];
  const Real potassium_pump_current_g_pK = params[37];
  const Real rapid_time_dependent_potassium_current_g_Kr = params[38];
  const Real reversal_potentials_P_kna = params[39];
  const Real slow_time_dependent_potassium_current_g_Ks = params[40];
  const Real sodium_background_current_g_bna = params[41];
  const Real sodium_calcium_exchanger_current_K_NaCa = params[42];
  const Real sodium_calcium_exchanger_current_K_sat = params[43];
  const Real sodium_calcium_exchanger_current_Km_Ca = params[44];
  const Real sodium_calcium_exchanger_current_Km_Nai = params[45];
  const Real sodium_calcium_exchanger_current_alpha = params[46];
  const Real sodium_calcium_exchanger_current_gamma = params[47];
  const Real sodium_dynamics_Na_o = params[48];
  const Real sodium_potassium_pump_current_K_mNa = params[49];
  const Real sodium_potassium_pump_current_K_mk = params[50];
  const Real sodium_potassium_pump_current_P_NaK = params[51];
  const Real transient_outward_current_g_to = params[52];
  const Real V = _r(_v(0, states_old));
  Real* const _new_V = _pr(_v(0, states_new));
  const Real _diffuse_V = diffusivity_V * diffuse(weights, _v(0, states_old));
  const Real Xr1 = _r(_v(1, states_old));
  Real* const _new_Xr1 = _pr(_v(1, states_new));
  const Real Xr2 = _r(_v(2, states_old));
  Real* const _new_Xr2 = _pr(_v(2, states_new));
  const Real Xs = _r(_v(3, states_old));
  Real* const _new_Xs = _pr(_v(3, states_new));
  const Real m = _r(_v(4, states_old));
  Real* const _new_m = _pr(_v(4, states_new));
  const Real h = _r(_v(5, states_old));
  Real* const _new_h = _pr(_v(5, states_new));
  const Real j = _r(_v(6, states_old));
  Real* const _new_j = _pr(_v(6, states_new));
  const Real d = _r(_v(7, states_old));
  Real* const _new_d = _pr(_v(7, states_new));
  const Real f = _r(_v(8, states_old));
  Real* const _new_f = _pr(_v(8, states_new));
  const Real f2 = _r(_v(9, states_old));
  Real* const _new_f2 = _pr(_v(9, states_new));
  const Real fCass = _r(_v(10, states_old));
  Real* const _new_fCass = _pr(_v(10, states_new));
  const Real s = _r(_v(11, states_old));
  Real* const _new_s = _pr(_v(11, states_new));
  const Real r = _r(_v(12, states_old));
  Real* const _new_r = _pr(_v(12, states_new));
  const Real Ca_i = _r(_v(13, states_old));
  Real* const _new_Ca_i = _pr(_v(13, states_new));
  const Real Ca_SR = _r(_v(14, states_old));
  Real* const _new_Ca_SR = _pr(_v(14, states_new));
  const Real Ca_ss = _r(_v(15, states_old));
  Real* const _new_Ca_ss = _pr(_v(15, states_new));
  const Real R_prime = _r(_v(16, states_old));
  Real* const _new_R_prime = _pr(_v(16, states_new));
  const Real Na_i = _r(_v(17, states_old));
  Real* const _new_Na_i = _pr(_v(17, states_new));
  const Real K_i = _r(_v(18, states_old));
  Real* const _new_K_i = _pr(_v(18, states_new));

  // L_type_Ca_current_d_gate
  const Real L_type_Ca_current_d_gate_alpha_d = 1.4f / (1.0f + native_exp((-35.0f - V) / 13.0f)) + 0.25f;
  const Real L_type_Ca_current_d_gate_beta_d = 1.4f / (1.0f + native_exp((V + 5.0f) / 5.0f));
  const Real L_type_Ca_current_d_gate_d_inf = 1.0f / (1.0f + native_exp((-8.0f - V) / 7.5f));
  const Real L_type_Ca_current_d_gate_gamma_d = 1.0f / (1.0f + native_exp((50.0f - V) / 20.0f));
  const Real L_type_Ca_current_d_gate_tau_d = 1.0f * L_type_Ca_current_d_gate_alpha_d * L_type_Ca_current_d_gate_beta_d + L_type_Ca_current_d_gate_gamma_d;
  *_new_d = d + dt*((L_type_Ca_current_d_gate_d_inf - d) / L_type_Ca_current_d_gate_tau_d);

  // L_type_Ca_current_f2_gate
  const Real L_type_Ca_current_f2_gate_f2_inf = 0.67f / (1.0f + native_exp((V + 35.0f) / 7.0f)) + 0.33f;
  const Real L_type_Ca_current_f2_gate_tau_f2 = 562.0f * native_exp(-pow(V + 27.0f, 2.0f) / 240.0f) + 31.0f / (1.0f + native_exp((25.0f - V) / 10.0f)) + 80.0f / (1.0f + native_exp((V + 30.0f) / 10.0f));
  *_new_f2 = f2 + dt*((L_type_Ca_current_f2_gate_f2_inf - f2) / L_type_Ca_current_f2_gate_tau_f2);

  // L_type_Ca_current_fCass_gate
  const Real L_type_Ca_current_fCass_gate_fCass_inf = 0.6f / (1.0f + pow(Ca_ss / 0.05f, 2.0f)) + 0.4f;
  const Real L_type_Ca_current_fCass_gate_tau_fCass = 80.0f / (1.0f + pow(Ca_ss / 0.05f, 2.0f)) + 2.0f;
  *_new_fCass = fCass + dt*((L_type_Ca_current_fCass_gate_fCass_inf - fCass) / L_type_Ca_current_fCass_gate_tau_fCass);

  // L_type_Ca_current_f_gate
  const Real L_type_Ca_current_f_gate_f_inf = 1.0f / (1.0f + native_exp((V + 20.0f) / 7.0f));
  const Real L_type_Ca_current_f_gate_tau_f = 1102.5f * native_exp(-pow(V + 27.0f, 2.0f) / 225.0f) + 200.0f / (1.0f + native_exp((13.0f - V) / 10.0f)) + 180.0f / (1.0f + native_exp((V + 30.0f) / 10.0f)) + 20.0f;
  *_new_f = f + dt*((L_type_Ca_current_f_gate_f_inf - f) / L_type_Ca_current_f_gate_tau_f);

  // calcium_pump_current
  const Real calcium_pump_current_i_p_Ca = calcium_pump_current_g_pCa * Ca_i / (Ca_i + calcium_pump_current_K_pCa);

  // fast_sodium_current_h_gate
  const Real fast_sodium_current_h_gate_alpha_h = ((V < -40.0f) ? 0.057f * native_exp(-(V + 80.0f) / 6.8f) : 0.0f);
  const Real fast_sodium_current_h_gate_beta_h = ((V < -40.0f) ? 2.7f * native_exp(0.079f * V) + 310000.0f * native_exp(0.3485f * V) : 0.77f / (0.13f * (1.0f + native_exp((V + 10.66f) / -11.1f))));
  const Real fast_sodium_current_h_gate_h_inf = 1.0f / pow(1.0f + native_exp((V + 71.55f) / 7.43f), 2.0f);
  const Real fast_sodium_current_h_gate_tau_h = 1.0f / (fast_sodium_current_h_gate_alpha_h + fast_sodium_current_h_gate_beta_h);
  *_new_h = h + dt*((fast_sodium_current_h_gate_h_inf - h) / fast_sodium_current_h_gate_tau_h);

  // fast_sodium_current_j_gate
  const Real fast_sodium_current_j_gate_alpha_j = ((V < -40.0f) ? (-25428.0f * native_exp(0.2444f * V) - 6.948e-06f * native_exp(-0.04391f * V)) * (V + 37.78f) / 1.0f / (1.0f + native_exp(0.311f * (V + 79.23f))) : 0.0f);
  const Real fast_sodium_current_j_gate_beta_j = ((V < -40.0f) ? 0.02424f * native_exp(-0.01052f * V) / (1.0f + native_exp(-0.1378f * (V + 40.14f))) : 0.6f * native_exp(0.057f * V) / (1.0f + native_exp(-0.1f * (V + 32.0f))));
  const Real fast_sodium_current_j_gate_j_inf = 1.0f / pow(1.0f + native_exp((V + 71.55f) / 7.43f), 2.0f);
  const Real fast_sodium_current_j_gate_tau_j = 1.0f / (fast_sodium_current_j_gate_alpha_j + fast_sodium_current_j_gate_beta_j);
  *_new_j = j + dt*((fast_sodium_current_j_gate_j_inf - j) / fast_sodium_current_j_gate_tau_j);

  // fast_sodium_current_m_gate
  const Real fast_sodium_current_m_gate_alpha_m = 1.0f / (1.0f + native_exp((-60.0f - V) / 5.0f));
  const Real fast_sodium_current_m_gate_beta_m = 0.1f / (1.0f + native_exp((V + 35.0f) / 5.0f)) + 0.1f / (1.0f + native_exp((V - 50.0f) / 200.0f));
  const Real fast_sodium_current_m_gate_m_inf = 1.0f / pow(1.0f + native_exp((-56.86f - V) / 9.03f), 2.0f);
  const Real fast_sodium_current_m_gate_tau_m = 1.0f * fast_sodium_current_m_gate_alpha_m * fast_sodium_current_m_gate_beta_m;
  *_new_m = m + dt*((fast_sodium_current_m_gate_m_inf - m) / fast_sodium_current_m_gate_tau_m);

  // rapid_time_dependent_potassium_current_Xr1_gate
  const Real rapid_time_dependent_potassium_current_Xr1_gate_alpha_xr1 = 450.0f / (1.0f + native_exp((-45.0f - V) / 10.0f));
  const Real rapid_time_dependent_potassium_current_Xr1_gate_beta_xr1 = 6.0f / (1.0f + native_exp((V + 30.0f) / 11.5f));
  const Real rapid_time_dependent_potassium_current_Xr1_gate_xr1_inf = 1.0f / (1.0f + native_exp((-26.0f - V) / 7.0f));
  const Real rapid_time_dependent_potassium_current_Xr1_gate_tau_xr1 = 1.0f * rapid_time_dependent_potassium_current_Xr1_gate_alpha_xr1 * rapid_time_dependent_potassium_current_Xr1_gate_beta_xr1;
  *_new_Xr1 = Xr1 + dt*((rapid_time_dependent_potassium_current_Xr1_gate_xr1_inf - Xr1) / rapid_time_dependent_potassium_current_Xr1_gate_tau_xr1);

  // rapid_time_dependent_potassium_current_Xr2_gate
  const Real rapid_time_dependent_potassium_current_Xr2_gate_alpha_xr2 = 3.0f / (1.0f + native_exp((-60.0f - V) / 20.0f));
  const Real rapid_time_dependent_potassium_current_Xr2_gate_beta_xr2 = 1.12f / (1.0f + native_exp((V - 60.0f) / 20.0f));
  const Real rapid_time_dependent_potassium_current_Xr2_gate_xr2_inf = 1.0f / (1.0f + native_exp((V + 88.0f) / 24.0f));
  const Real rapid_time_dependent_potassium_current_Xr2_gate_tau_xr2 = 1.0f * rapid_time_dependent_potassium_current_Xr2_gate_alpha_xr2 * rapid_time_dependent_potassium_current_Xr2_gate_beta_xr2;
  *_new_Xr2 = Xr2 + dt*((rapid_time_dependent_potassium_current_Xr2_gate_xr2_inf - Xr2) / rapid_time_dependent_potassium_current_Xr2_gate_tau_xr2);

  // slow_time_dependent_potassium_current_Xs_gate
  const Real slow_time_dependent_potassium_current_Xs_gate_alpha_xs = 1400.0f / native_sqrt(1.0f + native_exp((5.0f - V) / 6.0f));
  const Real slow_time_dependent_potassium_current_Xs_gate_beta_xs = 1.0f / (1.0f + native_exp((V - 35.0f) / 15.0f));
  const Real slow_time_dependent_potassium_current_Xs_gate_xs_inf = 1.0f / (1.0f + native_exp((-5.0f - V) / 14.0f));
  const Real slow_time_dependent_potassium_current_Xs_gate_tau_xs = 1.0f * slow_time_dependent_potassium_current_Xs_gate_alpha_xs * slow_time_dependent_potassium_current_Xs_gate_beta_xs + 80.0f;
  *_new_Xs = Xs + dt*((slow_time_dependent_potassium_current_Xs_gate_xs_inf - Xs) / slow_time_dependent_potassium_current_Xs_gate_tau_xs);

  // transient_outward_current_r_gate
  const Real transient_outward_current_r_gate_r_inf = 1.0f / (1.0f + native_exp((20.0f - V) / 6.0f));
  const Real transient_outward_current_r_gate_tau_r = 9.5f * native_exp(-pow(V + 40.0f, 2.0f) / 1800.0f) + 0.8f;
  *_new_r = r + dt*((transient_outward_current_r_gate_r_inf - r) / transient_outward_current_r_gate_tau_r);

  // transient_outward_current_s_gate
  const Real transient_outward_current_s_gate_s_inf = 1.0f / (1.0f + native_exp((V + 20.0f) / 5.0f));
  const Real transient_outward_current_s_gate_tau_s = 85.0f * native_exp(-pow(V + 45.0f, 2.0f) / 320.0f) + 5.0f / (1.0f + native_exp((V - 20.0f) / 5.0f)) + 3.0f;
  *_new_s = s + dt*((transient_outward_current_s_gate_s_inf - s) / transient_outward_current_s_gate_tau_s);

  // calcium_dynamics
  const Real calcium_dynamics_f_JCa_i_free = 1.0f / (1.0f + calcium_dynamics_Buf_c * calcium_dynamics_K_buf_c / pow(Ca_i + calcium_dynamics_K_buf_c, 2.0f));
  const Real calcium_dynamics_f_JCa_sr_free = 1.0f / (1.0f + calcium_dynamics_Buf_sr * calcium_dynamics_K_buf_sr / pow(Ca_SR + calcium_dynamics_K_buf_sr, 2.0f));
  const Real calcium_dynamics_f_JCa_ss_free = 1.0f / (1.0f + calcium_dynamics_Buf_ss * calcium_dynamics_K_buf_ss / pow(Ca_ss + calcium_dynamics_K_buf_ss, 2.0f));
  const Real calcium_dynamics_i_leak = calcium_dynamics_V_leak * (Ca_SR - Ca_i);
  const Real calcium_dynamics_i_up = calcium_dynamics_Vmax_up / (1.0f + pow(calcium_dynamics_K_up, 2.0f) / pow(Ca_i, 2.0f));
  const Real calcium_dynamics_i_xfer = calcium_dynamics_V_xfer * (Ca_ss - Ca_i);
  const Real calcium_dynamics_kcasr = calcium_dynamics_max_sr - (calcium_dynamics_max_sr - calcium_dynamics_min_sr) / (1.0f + pow(calcium_dynamics_EC / Ca_SR, 2.0f));
  const Real calcium_dynamics_k1 = calcium_dynamics_k1_prime / calcium_dynamics_kcasr;
  const Real calcium_dynamics_k2 = calcium_dynamics_k2_prime * calcium_dynamics_kcasr;
  const Real calcium_dynamics_O = calcium_dynamics_k1 * pow(Ca_ss, 2.0f) * R_prime / (calcium_dynamics_k3 + calcium_dynamics_k1 * pow(Ca_ss, 2.0f));
  *_new_R_prime = R_prime + dt*(-calcium_dynamics_k2 * Ca_ss * R_prime + calcium_dynamics_k4 * (1.0f - R_prime));
  const Real calcium_dynamics_i_rel = calcium_dynamics_V_rel * calcium_dynamics_O * (Ca_SR - Ca_ss);
  const Real calcium_dynamics_ddt_Ca_sr_total = calcium_dynamics_i_up - (calcium_dynamics_i_rel + calcium_dynamics_i_leak);
  *_new_Ca_SR = Ca_SR + dt*(calcium_dynamics_ddt_Ca_sr_total * calcium_dynamics_f_JCa_sr_free);

  // membrane
  const Real membrane_i_Stim = membrane_pace * membrane_stim_amplitude;

  // reversal_potentials
  const Real reversal_potentials_E_Ca = 0.5f * membrane_R * membrane_T / membrane_F * native_log(calcium_dynamics_Ca_o / Ca_i);
  const Real reversal_potentials_E_K = membrane_R * membrane_T / membrane_F * native_log(potassium_dynamics_K_o / K_i);

  // sodium_potassium_pump_current
  const Real sodium_potassium_pump_current_i_NaK = sodium_potassium_pump_current_P_NaK * potassium_dynamics_K_o / (potassium_dynamics_K_o + sodium_potassium_pump_current_K_mk) * Na_i / (Na_i + sodium_potassium_pump_current_K_mNa) / (1.0f + 0.1245f * native_exp(-0.1f * V * membrane_F / (membrane_R * membrane_T)) + 0.0353f * native_exp(-V * membrane_F / (membrane_R * membrane_T)));

  // transient_outward_current
  const Real transient_outward_current_i_to = transient_outward_current_g_to * r * s * (V - reversal_potentials_E_K);

  // *remaining*
  const Real L_type_Ca_current_i_CaL = L_type_Ca_current_g_CaL * d * f * f2 * fCass * 4.0f * (V - 15.0f) * pow(membrane_F, 2.0f) / (membrane_R * membrane_T) * (0.25f * Ca_ss * native_exp(2.0f * (V - 15.0f) * membrane_F / (membrane_R * membrane_T)) - calcium_dynamics_Ca_o) / (native_exp(2.0f * (V - 15.0f) * membrane_F / (membrane_R * membrane_T)) - 1.0f);
  const Real calcium_background_current_i_b_Ca = calcium_background_current_g_bca * (V - reversal_potentials_E_Ca);
  const Real inward_rectifier_potassium_current_alpha_K1 = 0.1f / (1.0f + native_exp(0.06f * (V - reversal_potentials_E_K - 200.0f)));
  const Real inward_rectifier_potassium_current_beta_K1 = (3.0f * native_exp(0.0002f * (V - reversal_potentials_E_K + 100.0f)) + native_exp(0.1f * (V - reversal_potentials_E_K - 10.0f))) / (1.0f + native_exp(-0.5f * (V - reversal_potentials_E_K)));
  const Real potassium_pump_current_i_p_K = potassium_pump_current_g_pK * (V - reversal_potentials_E_K) / (1.0f + native_exp((25.0f - V) / 5.98f));
  const Real rapid_time_dependent_potassium_current_i_Kr = rapid_time_dependent_potassium_current_g_Kr * native_sqrt(potassium_dynamics_K_o / 5.4f) * Xr1 * Xr2 * (V - reversal_potentials_E_K);
  const Real reversal_potentials_E_Ks = membrane_R * membrane_T / membrane_F * native_log((potassium_dynamics_K_o + reversal_potentials_P_kna * sodium_dynamics_Na_o) / (K_i + reversal_potentials_P_kna * Na_i));
  const Real reversal_potentials_E_Na = membrane_R * membrane_T / membrane_F * native_log(sodium_dynamics_Na_o / Na_i);
  const Real sodium_calcium_exchanger_current_i_NaCa = sodium_calcium_exchanger_current_K_NaCa * (native_exp(sodium_calcium_exchanger_current_gamma * V * membrane_F / (membrane_R * membrane_T)) * pow(Na_i, 3.0f) * calcium_dynamics_Ca_o - native_exp((sodium_calcium_exchanger_current_gamma - 1.0f) * V * membrane_F / (membrane_R * membrane_T)) * pow(sodium_dynamics_Na_o, 3.0f) * Ca_i * sodium_calcium_exchanger_current_alpha) / ((pow(sodium_calcium_exchanger_current_Km_Nai, 3.0f) + pow(sodium_dynamics_Na_o, 3.0f)) * (sodium_calcium_exchanger_current_Km_Ca + calcium_dynamics_Ca_o) * (1.0f + sodium_calcium_exchanger_current_K_sat * native_exp((sodium_calcium_exchanger_current_gamma - 1.0f) * V * membrane_F / (membrane_R * membrane_T))));
  const Real calcium_dynamics_ddt_Ca_i_total = -(calcium_background_current_i_b_Ca + calcium_pump_current_i_p_Ca - 2.0f * sodium_calcium_exchanger_current_i_NaCa) * membrane_Cm / (2.0f * membrane_V_c * membrane_F) + (calcium_dynamics_i_leak - calcium_dynamics_i_up) * calcium_dynamics_V_sr / membrane_V_c + calcium_dynamics_i_xfer;
  const Real calcium_dynamics_ddt_Ca_ss_total = -L_type_Ca_current_i_CaL * membrane_Cm / (2.0f * calcium_dynamics_V_ss * membrane_F) + calcium_dynamics_i_rel * calcium_dynamics_V_sr / calcium_dynamics_V_ss - calcium_dynamics_i_xfer * membrane_V_c / calcium_dynamics_V_ss;
  const Real fast_sodium_current_i_Na = fast_sodium_current_g_Na * pow(m, 3.0f) * h * j * (V - reversal_potentials_E_Na);
  const Real inward_rectifier_potassium_current_xK1_inf = inward_rectifier_potassium_current_alpha_K1 / (inward_rectifier_potassium_current_alpha_K1 + inward_rectifier_potassium_current_beta_K1);
  const Real slow_time_dependent_potassium_current_i_Ks = slow_time_dependent_potassium_current_g_Ks * pow(Xs, 2.0f) * (V - reversal_potentials_E_Ks);
  const Real sodium_background_current_i_b_Na = sodium_background_current_g_bna * (V - reversal_potentials_E_Na);
  *_new_Ca_i = Ca_i + dt*(calcium_dynamics_ddt_Ca_i_total * calcium_dynamics_f_JCa_i_free);
  *_new_Ca_ss = Ca_ss + dt*(calcium_dynamics_ddt_Ca_ss_total * calcium_dynamics_f_JCa_ss_free);
  const Real inward_rectifier_potassium_current_i_K1 = inward_rectifier_potassium_current_g_K1 * inward_rectifier_potassium_current_xK1_inf * native_sqrt(potassium_dynamics_K_o / 5.4f) * (V - reversal_potentials_E_K);
  *_new_Na_i = Na_i + dt*(-(fast_sodium_current_i_Na + sodium_background_current_i_b_Na + 3.0f * sodium_potassium_pump_current_i_NaK + 3.0f * sodium_calcium_exchanger_current_i_NaCa) / (membrane_V_c * membrane_F) * membrane_Cm);
  *_new_V = V + dt*(-(inward_rectifier_potassium_current_i_K1 + transient_outward_current_i_to + rapid_time_dependent_potassium_current_i_Kr + slow_time_dependent_potassium_current_i_Ks + L_type_Ca_current_i_CaL + sodium_potassium_pump_current_i_NaK + fast_sodium_current_i_Na + sodium_background_current_i_b_Na + sodium_calcium_exchanger_current_i_NaCa + calcium_background_current_i_b_Ca + potassium_pump_current_i_p_K + calcium_pump_current_i_p_Ca + membrane_i_Stim) + _diffuse_V);
  *_new_K_i = K_i + dt*(-(inward_rectifier_potassium_current_i_K1 + transient_outward_current_i_to + rapid_time_dependent_potassium_current_i_Kr + slow_time_dependent_potassium_current_i_Ks + potassium_pump_current_i_p_K + membrane_i_Stim - 2.0f * sodium_potassium_pump_current_i_NaK) / (membrane_V_c * membrane_F) * membrane_Cm);
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_tentusscher2006m_kernel(
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
      if (model_id == Model_tentusscher2006m_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_tentusscher2006m_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
