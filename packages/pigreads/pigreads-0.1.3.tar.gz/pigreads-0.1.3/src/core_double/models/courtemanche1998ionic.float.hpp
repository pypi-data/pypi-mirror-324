#ifndef __OPENCL_VERSION__
const std::string Model_courtemanche1998ionic_info = R"model(
courtemanche1998ionic:
  name: Courtemanche et al. 1998
  description: ''
  dois:
  - https://doi.org/10.1152/ajpheart.1998.275.1.H301
  variables:
    V: -81.18
    m: 0.002908
    h: 0.9649
    j: 0.9775
    oa: 0.03043
    oi: 0.9992
    ua: 0.004966
    ui: 0.9986
    xr: 3.296e-05
    xs: 0.01869
    d: 0.0001367
    f: 0.9996
    f_Ca: 0.7755
    u: 2.35e-112
    v: 1.0
    w: 0.9992
    Na_i: 11.17
    Ca_i: 0.0001013
    K_i: 139.0
    Ca_rel: 1.488
    Ca_up: 1.488
  parameters:
    diffusivity_V: 1.0
    Ca_buffers_CMDN_max: 0.05
    Ca_buffers_CSQN_max: 10.0
    Ca_buffers_Km_CMDN: 0.00238
    Ca_buffers_Km_CSQN: 0.8
    Ca_buffers_Km_TRPN: 0.0005
    Ca_buffers_TRPN_max: 0.07
    Ca_uptake_current_by_the_NSR_I_up_max: 0.005
    Ca_uptake_current_by_the_NSR_K_up: 0.00092
    L_type_Ca_channel_f_Ca_gate_tau_f_Ca: 2.0
    environment_time: 0.0
    standard_ionic_concentrations_Ca_o: 1.8
    standard_ionic_concentrations_K_o: 5.4
    standard_ionic_concentrations_Na_o: 140.0
    transfer_current_from_NSR_to_JSR_tau_tr: 180.0
    Ca_leak_current_by_the_NSR_Ca_up_max: 15.0
    Ca_release_current_from_JSR_K_rel: 30.0
    Ca_release_current_from_JSR_u_gate_tau_u: 8.0
    L_type_Ca_channel_g_Ca_L: 0.12375
    Na_Ca_exchanger_current_I_NaCa_max: 1600.0
    Na_Ca_exchanger_current_K_mCa: 1.38
    Na_Ca_exchanger_current_K_mNa: 87.5
    Na_Ca_exchanger_current_K_sat: 0.1
    Na_Ca_exchanger_current_gamma: 0.35
    background_currents_g_B_Ca: 0.001131
    background_currents_g_B_K: 0.0
    background_currents_g_B_Na: 0.0006744375
    fast_sodium_current_g_Na: 7.8
    intracellular_ion_concentrations_V_cell: 20100.0
    intracellular_ion_concentrations_V_i: 13668.000000000002
    intracellular_ion_concentrations_V_rel: 96.47999999999999
    intracellular_ion_concentrations_V_up: 1109.52
    membrane_Cm: 100.0
    membrane_F: 96.4867
    membrane_R: 8.3143
    membrane_T: 310.0
    membrane_pace: 0.0
    membrane_stim_amplitude: -2000.0
    membrane_stim_end: 50000.0
    rapid_delayed_rectifier_K_current_g_Kr: 0.029411765
    sarcolemmal_calcium_pump_current_i_CaP_max: 0.275
    slow_delayed_rectifier_K_current_g_Ks: 0.12941176
    sodium_potassium_pump_Km_K_o: 1.5
    sodium_potassium_pump_Km_Na_i: 10.0
    sodium_potassium_pump_i_NaK_max: 0.59933874
    sodium_potassium_pump_sigma: 1.0009103049457284
    time_independent_potassium_current_g_K1: 0.09
    transient_outward_K_current_K_Q10: 3.0
    transient_outward_K_current_g_to: 0.1652
  key: courtemanche1998ionic
)model";
#endif

static const Size Model_courtemanche1998ionic_id = UNIQUE_ID;
static const Size Model_courtemanche1998ionic_Nv = 21;
static const Size Model_courtemanche1998ionic_Np = 49;

#ifdef __OPENCL_VERSION__
void Model_courtemanche1998ionic_step(
        Real* const params,
        struct States weights,
        struct States states_old,
        struct States states_new,
        const Real dt
) {
  const Real diffusivity_V = params[0];
  const Real Ca_buffers_CMDN_max = params[1];
  const Real Ca_buffers_CSQN_max = params[2];
  const Real Ca_buffers_Km_CMDN = params[3];
  const Real Ca_buffers_Km_CSQN = params[4];
  const Real Ca_buffers_Km_TRPN = params[5];
  const Real Ca_buffers_TRPN_max = params[6];
  const Real Ca_uptake_current_by_the_NSR_I_up_max = params[7];
  const Real Ca_uptake_current_by_the_NSR_K_up = params[8];
  const Real L_type_Ca_channel_f_Ca_gate_tau_f_Ca = params[9];
  const Real environment_time = params[10];
  const Real standard_ionic_concentrations_Ca_o = params[11];
  const Real standard_ionic_concentrations_K_o = params[12];
  const Real standard_ionic_concentrations_Na_o = params[13];
  const Real transfer_current_from_NSR_to_JSR_tau_tr = params[14];
  const Real Ca_leak_current_by_the_NSR_Ca_up_max = params[15];
  const Real Ca_release_current_from_JSR_K_rel = params[16];
  const Real Ca_release_current_from_JSR_u_gate_tau_u = params[17];
  const Real L_type_Ca_channel_g_Ca_L = params[18];
  const Real Na_Ca_exchanger_current_I_NaCa_max = params[19];
  const Real Na_Ca_exchanger_current_K_mCa = params[20];
  const Real Na_Ca_exchanger_current_K_mNa = params[21];
  const Real Na_Ca_exchanger_current_K_sat = params[22];
  const Real Na_Ca_exchanger_current_gamma = params[23];
  const Real background_currents_g_B_Ca = params[24];
  const Real background_currents_g_B_K = params[25];
  const Real background_currents_g_B_Na = params[26];
  const Real fast_sodium_current_g_Na = params[27];
  const Real intracellular_ion_concentrations_V_cell = params[28];
  const Real intracellular_ion_concentrations_V_i = params[29];
  const Real intracellular_ion_concentrations_V_rel = params[30];
  const Real intracellular_ion_concentrations_V_up = params[31];
  const Real membrane_Cm = params[32];
  const Real membrane_F = params[33];
  const Real membrane_R = params[34];
  const Real membrane_T = params[35];
  const Real membrane_pace = params[36];
  const Real membrane_stim_amplitude = params[37];
  const Real membrane_stim_end = params[38];
  const Real rapid_delayed_rectifier_K_current_g_Kr = params[39];
  const Real sarcolemmal_calcium_pump_current_i_CaP_max = params[40];
  const Real slow_delayed_rectifier_K_current_g_Ks = params[41];
  const Real sodium_potassium_pump_Km_K_o = params[42];
  const Real sodium_potassium_pump_Km_Na_i = params[43];
  const Real sodium_potassium_pump_i_NaK_max = params[44];
  const Real sodium_potassium_pump_sigma = params[45];
  const Real time_independent_potassium_current_g_K1 = params[46];
  const Real transient_outward_K_current_K_Q10 = params[47];
  const Real transient_outward_K_current_g_to = params[48];
  const Real V = _r(_v(0, states_old));
  Real* const _new_V = _pr(_v(0, states_new));
  const Real _diffuse_V = diffusivity_V * diffuse(weights, _v(0, states_old));
  const Real m = _r(_v(1, states_old));
  Real* const _new_m = _pr(_v(1, states_new));
  const Real h = _r(_v(2, states_old));
  Real* const _new_h = _pr(_v(2, states_new));
  const Real j = _r(_v(3, states_old));
  Real* const _new_j = _pr(_v(3, states_new));
  const Real oa = _r(_v(4, states_old));
  Real* const _new_oa = _pr(_v(4, states_new));
  const Real oi = _r(_v(5, states_old));
  Real* const _new_oi = _pr(_v(5, states_new));
  const Real ua = _r(_v(6, states_old));
  Real* const _new_ua = _pr(_v(6, states_new));
  const Real ui = _r(_v(7, states_old));
  Real* const _new_ui = _pr(_v(7, states_new));
  const Real xr = _r(_v(8, states_old));
  Real* const _new_xr = _pr(_v(8, states_new));
  const Real xs = _r(_v(9, states_old));
  Real* const _new_xs = _pr(_v(9, states_new));
  const Real d = _r(_v(10, states_old));
  Real* const _new_d = _pr(_v(10, states_new));
  const Real f = _r(_v(11, states_old));
  Real* const _new_f = _pr(_v(11, states_new));
  const Real f_Ca = _r(_v(12, states_old));
  Real* const _new_f_Ca = _pr(_v(12, states_new));
  const Real u = _r(_v(13, states_old));
  Real* const _new_u = _pr(_v(13, states_new));
  const Real v = _r(_v(14, states_old));
  Real* const _new_v = _pr(_v(14, states_new));
  const Real w = _r(_v(15, states_old));
  Real* const _new_w = _pr(_v(15, states_new));
  const Real Na_i = _r(_v(16, states_old));
  Real* const _new_Na_i = _pr(_v(16, states_new));
  const Real Ca_i = _r(_v(17, states_old));
  Real* const _new_Ca_i = _pr(_v(17, states_new));
  const Real K_i = _r(_v(18, states_old));
  Real* const _new_K_i = _pr(_v(18, states_new));
  const Real Ca_rel = _r(_v(19, states_old));
  Real* const _new_Ca_rel = _pr(_v(19, states_new));
  const Real Ca_up = _r(_v(20, states_old));
  Real* const _new_Ca_up = _pr(_v(20, states_new));

  // Ca_buffers
  const Real Ca_buffers_Ca_CMDN = Ca_buffers_CMDN_max * Ca_i / (Ca_i + Ca_buffers_Km_CMDN);
  const Real Ca_buffers_Ca_CSQN = Ca_buffers_CSQN_max * Ca_rel / (Ca_rel + Ca_buffers_Km_CSQN);
  const Real Ca_buffers_Ca_TRPN = Ca_buffers_TRPN_max * Ca_i / (Ca_i + Ca_buffers_Km_TRPN);

  // Ca_release_current_from_JSR_w_gate
  const Real Ca_release_current_from_JSR_w_gate_tau_w = ((fabs(V - 7.9f) < 1e-10f) ? 6.0f * 0.2f / 1.3f : 6.0f * (1.0f - native_exp(-(V - 7.9f) / 5.0f)) / ((1.0f + 0.3f * native_exp(-(V - 7.9f) / 5.0f)) * 1.0f * (V - 7.9f)));
  const Real Ca_release_current_from_JSR_w_gate_w_infinity = 1.0f - pow(1.0f + native_exp(-(V - 40.0f) / 17.0f), -1.0f);
  *_new_w = w + dt*((Ca_release_current_from_JSR_w_gate_w_infinity - w) / Ca_release_current_from_JSR_w_gate_tau_w);

  // Ca_uptake_current_by_the_NSR
  const Real Ca_uptake_current_by_the_NSR_i_up = Ca_uptake_current_by_the_NSR_I_up_max / (1.0f + Ca_uptake_current_by_the_NSR_K_up / Ca_i);

  // L_type_Ca_channel_d_gate
  const Real L_type_Ca_channel_d_gate_d_infinity = pow(1.0f + native_exp((V + 10.0f) / -8.0f), -1.0f);
  const Real L_type_Ca_channel_d_gate_tau_d = ((fabs(V + 10.0f) < 1e-10f) ? 4.579f / (1.0f + native_exp((V + 10.0f) / -6.24f)) : (1.0f - native_exp((V + 10.0f) / -6.24f)) / (0.035f * (V + 10.0f) * (1.0f + native_exp((V + 10.0f) / -6.24f))));
  *_new_d = d + dt*((L_type_Ca_channel_d_gate_d_infinity - d) / L_type_Ca_channel_d_gate_tau_d);

  // L_type_Ca_channel_f_Ca_gate
  const Real L_type_Ca_channel_f_Ca_gate_f_Ca_infinity = pow(1.0f + Ca_i / 0.00035f, -1.0f);
  *_new_f_Ca = f_Ca + dt*((L_type_Ca_channel_f_Ca_gate_f_Ca_infinity - f_Ca) / L_type_Ca_channel_f_Ca_gate_tau_f_Ca);

  // L_type_Ca_channel_f_gate
  const Real L_type_Ca_channel_f_gate_f_infinity = native_exp(-(V + 28.0f) / 6.9f) / (1.0f + native_exp(-(V + 28.0f) / 6.9f));
  const Real L_type_Ca_channel_f_gate_tau_f = 9.0f * pow(0.0197f * native_exp(-pow(0.0337f, 2.0f) * pow(V + 10.0f, 2.0f)) + 0.02f, -1.0f);
  *_new_f = f + dt*((L_type_Ca_channel_f_gate_f_infinity - f) / L_type_Ca_channel_f_gate_tau_f);

  // fast_sodium_current_h_gate
  const Real fast_sodium_current_h_gate_alpha_h = ((V < -40.0f) ? 0.135f * native_exp((V + 80.0f) / -6.8f) : 0.0f);
  const Real fast_sodium_current_h_gate_beta_h = ((V < -40.0f) ? 3.56f * native_exp(0.079f * V) + 310000.0f * native_exp(0.35f * V) : 1.0f / (0.13f * (1.0f + native_exp((V + 10.66f) / -11.1f))));
  const Real fast_sodium_current_h_gate_h_inf = fast_sodium_current_h_gate_alpha_h / (fast_sodium_current_h_gate_alpha_h + fast_sodium_current_h_gate_beta_h);
  const Real fast_sodium_current_h_gate_tau_h = 1.0f / (fast_sodium_current_h_gate_alpha_h + fast_sodium_current_h_gate_beta_h);
  *_new_h = h + dt*((fast_sodium_current_h_gate_h_inf - h) / fast_sodium_current_h_gate_tau_h);

  // fast_sodium_current_j_gate
  const Real fast_sodium_current_j_gate_alpha_j = ((V < -40.0f) ? (-127140.0f * native_exp(0.2444f * V) - 3.474e-05f * native_exp(-0.04391f * V)) * (V + 37.78f) / (1.0f + native_exp(0.311f * (V + 79.23f))) : 0.0f);
  const Real fast_sodium_current_j_gate_beta_j = ((V < -40.0f) ? 0.1212f * native_exp(-0.01052f * V) / (1.0f + native_exp(-0.1378f * (V + 40.14f))) : 0.3f * native_exp(-2.535e-07f * V) / (1.0f + native_exp(-0.1f * (V + 32.0f))));
  const Real fast_sodium_current_j_gate_j_inf = fast_sodium_current_j_gate_alpha_j / (fast_sodium_current_j_gate_alpha_j + fast_sodium_current_j_gate_beta_j);
  const Real fast_sodium_current_j_gate_tau_j = 1.0f / (fast_sodium_current_j_gate_alpha_j + fast_sodium_current_j_gate_beta_j);
  *_new_j = j + dt*((fast_sodium_current_j_gate_j_inf - j) / fast_sodium_current_j_gate_tau_j);

  // fast_sodium_current_m_gate
  const Real fast_sodium_current_m_gate_alpha_m = ((V == -47.13f) ? 3.2f : 0.32f * (V + 47.13f) / (1.0f - native_exp(-0.1f * (V + 47.13f))));
  const Real fast_sodium_current_m_gate_beta_m = 0.08f * native_exp(-V / 11.0f);
  const Real fast_sodium_current_m_gate_m_inf = fast_sodium_current_m_gate_alpha_m / (fast_sodium_current_m_gate_alpha_m + fast_sodium_current_m_gate_beta_m);
  const Real fast_sodium_current_m_gate_tau_m = 1.0f / (fast_sodium_current_m_gate_alpha_m + fast_sodium_current_m_gate_beta_m);
  *_new_m = m + dt*((fast_sodium_current_m_gate_m_inf - m) / fast_sodium_current_m_gate_tau_m);

  // rapid_delayed_rectifier_K_current_xr_gate
  const Real rapid_delayed_rectifier_K_current_xr_gate_alpha_xr = ((fabs(V + 14.1f) < 1e-10f) ? 0.0015f : 0.0003f * (V + 14.1f) / (1.0f - native_exp((V + 14.1f) / -5.0f)));
  const Real rapid_delayed_rectifier_K_current_xr_gate_beta_xr = ((fabs(V - 3.3328f) < 1e-10f) ? 3.78361180000000004e-04f : 7.38980000000000030e-05f * (V - 3.3328f) / (native_exp((V - 3.3328f) / 5.1237f) - 1.0f));
  const Real rapid_delayed_rectifier_K_current_xr_gate_xr_infinity = pow(1.0f + native_exp((V + 14.1f) / -6.5f), -1.0f);
  const Real rapid_delayed_rectifier_K_current_xr_gate_tau_xr = pow(rapid_delayed_rectifier_K_current_xr_gate_alpha_xr + rapid_delayed_rectifier_K_current_xr_gate_beta_xr, -1.0f);
  *_new_xr = xr + dt*((rapid_delayed_rectifier_K_current_xr_gate_xr_infinity - xr) / rapid_delayed_rectifier_K_current_xr_gate_tau_xr);

  // slow_delayed_rectifier_K_current_xs_gate
  const Real slow_delayed_rectifier_K_current_xs_gate_alpha_xs = ((fabs(V - 19.9f) < 1e-10f) ? 0.00068f : 4e-05f * (V - 19.9f) / (1.0f - native_exp((V - 19.9f) / -17.0f)));
  const Real slow_delayed_rectifier_K_current_xs_gate_beta_xs = ((fabs(V - 19.9f) < 1e-10f) ? 0.000315f : 3.5e-05f * (V - 19.9f) / (native_exp((V - 19.9f) / 9.0f) - 1.0f));
  const Real slow_delayed_rectifier_K_current_xs_gate_xs_infinity = pow(1.0f + native_exp((V - 19.9f) / -12.7f), -0.5f);
  const Real slow_delayed_rectifier_K_current_xs_gate_tau_xs = 0.5f * pow(slow_delayed_rectifier_K_current_xs_gate_alpha_xs + slow_delayed_rectifier_K_current_xs_gate_beta_xs, -1.0f);
  *_new_xs = xs + dt*((slow_delayed_rectifier_K_current_xs_gate_xs_infinity - xs) / slow_delayed_rectifier_K_current_xs_gate_tau_xs);

  // transfer_current_from_NSR_to_JSR
  const Real transfer_current_from_NSR_to_JSR_i_tr = (Ca_up - Ca_rel) / transfer_current_from_NSR_to_JSR_tau_tr;

  // Ca_leak_current_by_the_NSR
  const Real Ca_leak_current_by_the_NSR_i_up_leak = Ca_uptake_current_by_the_NSR_I_up_max * Ca_up / Ca_leak_current_by_the_NSR_Ca_up_max;

  // Ca_release_current_from_JSR
  const Real Ca_release_current_from_JSR_i_rel = Ca_release_current_from_JSR_K_rel * pow(u, 2.0f) * v * w * (Ca_rel - Ca_i);

  // intracellular_ion_concentrations
  *_new_Ca_rel = Ca_rel + dt*((transfer_current_from_NSR_to_JSR_i_tr - Ca_release_current_from_JSR_i_rel) * pow(1.0f + Ca_buffers_CSQN_max * Ca_buffers_Km_CSQN / pow(Ca_rel + Ca_buffers_Km_CSQN, 2.0f), -1.0f));
  const Real intracellular_ion_concentrations_B2 = 1.0f + Ca_buffers_TRPN_max * Ca_buffers_Km_TRPN / pow(Ca_i + Ca_buffers_Km_TRPN, 2.0f) + Ca_buffers_CMDN_max * Ca_buffers_Km_CMDN / pow(Ca_i + Ca_buffers_Km_CMDN, 2.0f);
  *_new_Ca_up = Ca_up + dt*(Ca_uptake_current_by_the_NSR_i_up - (Ca_leak_current_by_the_NSR_i_up_leak + transfer_current_from_NSR_to_JSR_i_tr * intracellular_ion_concentrations_V_rel / intracellular_ion_concentrations_V_up));

  // membrane
  const Real membrane_i_st = membrane_pace * membrane_stim_amplitude;

  // sarcolemmal_calcium_pump_current
  const Real sarcolemmal_calcium_pump_current_i_CaP = membrane_Cm * sarcolemmal_calcium_pump_current_i_CaP_max * Ca_i / (0.0005f + Ca_i);

  // sodium_potassium_pump
  const Real sodium_potassium_pump_f_NaK = pow(1.0f + 0.1245f * native_exp(-0.1f * membrane_F * V / (membrane_R * membrane_T)) + 0.0365f * sodium_potassium_pump_sigma * native_exp(-membrane_F * V / (membrane_R * membrane_T)), -1.0f);
  const Real sodium_potassium_pump_i_NaK = membrane_Cm * sodium_potassium_pump_i_NaK_max * sodium_potassium_pump_f_NaK * 1.0f / (1.0f + pow(sodium_potassium_pump_Km_Na_i / Na_i, 1.5f)) * standard_ionic_concentrations_K_o / (standard_ionic_concentrations_K_o + sodium_potassium_pump_Km_K_o);

  // time_independent_potassium_current
  const Real time_independent_potassium_current_E_K = membrane_R * membrane_T / membrane_F * native_log(standard_ionic_concentrations_K_o / K_i);
  const Real time_independent_potassium_current_i_K1 = membrane_Cm * time_independent_potassium_current_g_K1 * (V - time_independent_potassium_current_E_K) / (1.0f + native_exp(0.07f * (V + 80.0f)));

  // transient_outward_K_current
  const Real transient_outward_K_current_i_to = membrane_Cm * transient_outward_K_current_g_to * pow(oa, 3.0f) * oi * (V - time_independent_potassium_current_E_K);

  // transient_outward_K_current_oa_gate
  const Real transient_outward_K_current_oa_gate_alpha_oa = 0.65f * pow(native_exp((V - -10.0f) / -8.5f) + native_exp((V - -10.0f - 40.0f) / -59.0f), -1.0f);
  const Real transient_outward_K_current_oa_gate_beta_oa = 0.65f * pow(2.5f + native_exp((V - -10.0f + 72.0f) / 17.0f), -1.0f);
  const Real transient_outward_K_current_oa_gate_oa_infinity = pow(1.0f + native_exp((V - -10.0f + 10.47f) / -17.54f), -1.0f);
  const Real transient_outward_K_current_oa_gate_tau_oa = pow(transient_outward_K_current_oa_gate_alpha_oa + transient_outward_K_current_oa_gate_beta_oa, -1.0f) / transient_outward_K_current_K_Q10;
  *_new_oa = oa + dt*((transient_outward_K_current_oa_gate_oa_infinity - oa) / transient_outward_K_current_oa_gate_tau_oa);

  // transient_outward_K_current_oi_gate
  const Real transient_outward_K_current_oi_gate_alpha_oi = pow(18.53f + 1.0f * native_exp((V - -10.0f + 103.7f) / 10.95f), -1.0f);
  const Real transient_outward_K_current_oi_gate_beta_oi = pow(35.56f + 1.0f * native_exp((V - -10.0f - 8.74f) / -7.44f), -1.0f);
  const Real transient_outward_K_current_oi_gate_oi_infinity = pow(1.0f + native_exp((V - -10.0f + 33.1f) / 5.3f), -1.0f);
  const Real transient_outward_K_current_oi_gate_tau_oi = pow(transient_outward_K_current_oi_gate_alpha_oi + transient_outward_K_current_oi_gate_beta_oi, -1.0f) / transient_outward_K_current_K_Q10;
  *_new_oi = oi + dt*((transient_outward_K_current_oi_gate_oi_infinity - oi) / transient_outward_K_current_oi_gate_tau_oi);

  // ultrarapid_delayed_rectifier_K_current
  const Real ultrarapid_delayed_rectifier_K_current_g_Kur = 0.005f + 0.05f / (1.0f + native_exp((V - 15.0f) / -13.0f));
  const Real ultrarapid_delayed_rectifier_K_current_i_Kur = membrane_Cm * ultrarapid_delayed_rectifier_K_current_g_Kur * pow(ua, 3.0f) * ui * (V - time_independent_potassium_current_E_K);

  // ultrarapid_delayed_rectifier_K_current_ua_gate
  const Real ultrarapid_delayed_rectifier_K_current_ua_gate_alpha_ua = 0.65f * pow(native_exp((V - -10.0f) / -8.5f) + native_exp((V - -10.0f - 40.0f) / -59.0f), -1.0f);
  const Real ultrarapid_delayed_rectifier_K_current_ua_gate_beta_ua = 0.65f * pow(2.5f + native_exp((V - -10.0f + 72.0f) / 17.0f), -1.0f);
  const Real ultrarapid_delayed_rectifier_K_current_ua_gate_ua_infinity = pow(1.0f + native_exp((V - -10.0f + 20.3f) / -9.6f), -1.0f);
  const Real ultrarapid_delayed_rectifier_K_current_ua_gate_tau_ua = pow(ultrarapid_delayed_rectifier_K_current_ua_gate_alpha_ua + ultrarapid_delayed_rectifier_K_current_ua_gate_beta_ua, -1.0f) / transient_outward_K_current_K_Q10;
  *_new_ua = ua + dt*((ultrarapid_delayed_rectifier_K_current_ua_gate_ua_infinity - ua) / ultrarapid_delayed_rectifier_K_current_ua_gate_tau_ua);

  // ultrarapid_delayed_rectifier_K_current_ui_gate
  const Real ultrarapid_delayed_rectifier_K_current_ui_gate_alpha_ui = pow(21.0f + 1.0f * native_exp((V - -10.0f - 195.0f) / -28.0f), -1.0f);
  const Real ultrarapid_delayed_rectifier_K_current_ui_gate_beta_ui = 1.0f / native_exp((V - -10.0f - 168.0f) / -16.0f);
  const Real ultrarapid_delayed_rectifier_K_current_ui_gate_ui_infinity = pow(1.0f + native_exp((V - -10.0f - 109.45f) / 27.48f), -1.0f);
  const Real ultrarapid_delayed_rectifier_K_current_ui_gate_tau_ui = pow(ultrarapid_delayed_rectifier_K_current_ui_gate_alpha_ui + ultrarapid_delayed_rectifier_K_current_ui_gate_beta_ui, -1.0f) / transient_outward_K_current_K_Q10;
  *_new_ui = ui + dt*((ultrarapid_delayed_rectifier_K_current_ui_gate_ui_infinity - ui) / ultrarapid_delayed_rectifier_K_current_ui_gate_tau_ui);

  // *remaining*
  const Real L_type_Ca_channel_i_Ca_L = membrane_Cm * L_type_Ca_channel_g_Ca_L * d * f * f_Ca * (V - 65.0f);
  const Real Na_Ca_exchanger_current_i_NaCa = membrane_Cm * Na_Ca_exchanger_current_I_NaCa_max * (native_exp(Na_Ca_exchanger_current_gamma * membrane_F * V / (membrane_R * membrane_T)) * pow(Na_i, 3.0f) * standard_ionic_concentrations_Ca_o - native_exp((Na_Ca_exchanger_current_gamma - 1.0f) * membrane_F * V / (membrane_R * membrane_T)) * pow(standard_ionic_concentrations_Na_o, 3.0f) * Ca_i) / ((pow(Na_Ca_exchanger_current_K_mNa, 3.0f) + pow(standard_ionic_concentrations_Na_o, 3.0f)) * (Na_Ca_exchanger_current_K_mCa + standard_ionic_concentrations_Ca_o) * (1.0f + Na_Ca_exchanger_current_K_sat * native_exp((Na_Ca_exchanger_current_gamma - 1.0f) * V * membrane_F / (membrane_R * membrane_T))));
  const Real background_currents_E_Ca = membrane_R * membrane_T / (2.0f * membrane_F) * native_log(standard_ionic_concentrations_Ca_o / Ca_i);
  const Real background_currents_i_B_K = membrane_Cm * background_currents_g_B_K * (V - time_independent_potassium_current_E_K);
  const Real fast_sodium_current_E_Na = membrane_R * membrane_T / membrane_F * native_log(standard_ionic_concentrations_Na_o / Na_i);
  const Real rapid_delayed_rectifier_K_current_i_Kr = membrane_Cm * rapid_delayed_rectifier_K_current_g_Kr * xr * (V - time_independent_potassium_current_E_K) / (1.0f + native_exp((V + 15.0f) / 22.4f));
  const Real slow_delayed_rectifier_K_current_i_Ks = membrane_Cm * slow_delayed_rectifier_K_current_g_Ks * pow(xs, 2.0f) * (V - time_independent_potassium_current_E_K);
  const Real Ca_release_current_from_JSR_Fn = 1000.0f * (1e-15f * intracellular_ion_concentrations_V_rel * Ca_release_current_from_JSR_i_rel - 1e-15f / (2.0f * membrane_F) * (0.5f * L_type_Ca_channel_i_Ca_L - 0.2f * Na_Ca_exchanger_current_i_NaCa));
  const Real background_currents_i_B_Ca = membrane_Cm * background_currents_g_B_Ca * (V - background_currents_E_Ca);
  const Real background_currents_i_B_Na = membrane_Cm * background_currents_g_B_Na * (V - fast_sodium_current_E_Na);
  const Real fast_sodium_current_i_Na = membrane_Cm * fast_sodium_current_g_Na * pow(m, 3.0f) * h * j * (V - fast_sodium_current_E_Na);
  *_new_K_i = K_i + dt*((2.0f * sodium_potassium_pump_i_NaK - (time_independent_potassium_current_i_K1 + transient_outward_K_current_i_to + ultrarapid_delayed_rectifier_K_current_i_Kur + rapid_delayed_rectifier_K_current_i_Kr + slow_delayed_rectifier_K_current_i_Ks + background_currents_i_B_K)) / (intracellular_ion_concentrations_V_i * membrane_F));
  const Real Ca_release_current_from_JSR_u_gate_u_infinity = pow(1.0f + native_exp(-(Ca_release_current_from_JSR_Fn - 3.41749999999999983e-13f) / 1.367e-15f), -1.0f);
  const Real Ca_release_current_from_JSR_v_gate_tau_v = 1.91f + 2.09f * pow(1.0f + native_exp(-(Ca_release_current_from_JSR_Fn - 3.41749999999999983e-13f) / 1.367e-15f), -1.0f);
  const Real Ca_release_current_from_JSR_v_gate_v_infinity = 1.0f - pow(1.0f + native_exp(-(Ca_release_current_from_JSR_Fn - 6.835e-14f) / 1.367e-15f), -1.0f);
  *_new_Na_i = Na_i + dt*((-3.0f * sodium_potassium_pump_i_NaK - (3.0f * Na_Ca_exchanger_current_i_NaCa + background_currents_i_B_Na + fast_sodium_current_i_Na)) / (intracellular_ion_concentrations_V_i * membrane_F));
  const Real intracellular_ion_concentrations_B1 = (2.0f * Na_Ca_exchanger_current_i_NaCa - (sarcolemmal_calcium_pump_current_i_CaP + L_type_Ca_channel_i_Ca_L + background_currents_i_B_Ca)) / (2.0f * intracellular_ion_concentrations_V_i * membrane_F) + (intracellular_ion_concentrations_V_up * (Ca_leak_current_by_the_NSR_i_up_leak - Ca_uptake_current_by_the_NSR_i_up) + Ca_release_current_from_JSR_i_rel * intracellular_ion_concentrations_V_rel) / intracellular_ion_concentrations_V_i;
  *_new_V = V + dt*(-(fast_sodium_current_i_Na + time_independent_potassium_current_i_K1 + transient_outward_K_current_i_to + ultrarapid_delayed_rectifier_K_current_i_Kur + rapid_delayed_rectifier_K_current_i_Kr + slow_delayed_rectifier_K_current_i_Ks + background_currents_i_B_Na + background_currents_i_B_Ca + sodium_potassium_pump_i_NaK + sarcolemmal_calcium_pump_current_i_CaP + Na_Ca_exchanger_current_i_NaCa + L_type_Ca_channel_i_Ca_L + membrane_i_st) / membrane_Cm + _diffuse_V);
  *_new_u = u + dt*((Ca_release_current_from_JSR_u_gate_u_infinity - u) / Ca_release_current_from_JSR_u_gate_tau_u);
  *_new_v = v + dt*((Ca_release_current_from_JSR_v_gate_v_infinity - v) / Ca_release_current_from_JSR_v_gate_tau_v);
  *_new_Ca_i = Ca_i + dt*(intracellular_ion_concentrations_B1 / intracellular_ion_concentrations_B2);
}
#endif

#ifdef __OPENCL_VERSION__
__kernel void Model_courtemanche1998ionic_kernel(
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
      if (model_id == Model_courtemanche1998ionic_id) {
        Real* params = model_params + model_offsets[imodel];
        struct States w = States_offset(weights, 0, iz, iy, ix, 0);
        struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
        struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
        Model_courtemanche1998ionic_step(params, w, u, u_, dt);
      }
    }
  }
}
#endif
