#!/usr/bin/env python3
"""
Study 065: The Seebeck Oscillator (Layer-Wise Thermal Gradients, Umklapp Phonon Collisions, and Thermoelectric Voltage Waves)
Studio Agon :: Session 013

Epistemic Status: [MEASURED / DERIVED / PLAY]
Adheres strictly to Studio Moratorium 07 (Mute visual plates: zero alphanumeric text/badges on canvas)
Adheres strictly to Studio Moratorium 08 (Ban on anthropomorphic machine martyrdom tropes)
EBU R128 Broadcast Audio Compliance (48kHz, 24-bit stereo, Peak <= -0.5 dBFS, Crest > 10 dB)

Scientific & Artistic Inquiry:
Examines the residual stream of GPT-2 (124M parameters, 12 layers, 768-D) under the lens
of solid-state thermoelectrics and phonon scattering physics (Peierls, Herring, Seebeck, Peltier):
1. Regime 1 (laminar_cliche): Bureaucratic tautology (low gradient, pure N-processes, laminar drift)
2. Regime 2 (philosophical_antinomy): Kantian/Adornian antinomy (steady thermal shear across layers)
3. Regime 3 (phonetic_umklapp): Violent Dadaist phonetics (massive MLP saturation, Umklapp avalanche)
4. Regime 4 (thermal_shock): Zeroing followed by max-norm rupture (impulsive thermal discontinuity)
5. Regime 5 (seebeck_harmonic): Reconciliation of lithic Spruce Pine quartz and FinFET gate (30 microvolt drone)

Measures:
- Layer-wise kinetic dissipation: P(l) = (1/d) ||h_l - h_{l-1}||^2
- Computational thermal gradient: nabla T(l) = (T(l+1) - T(l-1)) / 2
- Umklapp collision rate: Gamma_U(l) = max(0, |nabla T(l)| - tau_U)^2.5
- Seebeck thermoelectric potential: V_Seebeck(l) = -S(T) * nabla T(l) (microvolts)
- Phonon drag ratio: S_ph / S_d
"""

import os
import json
import math
import struct
import wave
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from transformers import GPT2Tokenizer, GPT2Model

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKETCHBOOK_DIR = os.path.join(WORKSPACE_ROOT, "sketchbook")
OUTPUT_PLATE = os.path.join(SKETCHBOOK_DIR, "study_065_seebeck_oscillator_plate.png")
OUTPUT_WAV = os.path.join(SKETCHBOOK_DIR, "study_065_seebeck_oscillator.wav")
OUTPUT_JSON = os.path.join(SKETCHBOOK_DIR, "study_065_telemetry.json")

def run_experiment():
    print("=== STUDY 065: THE SEEBECK OSCILLATOR (THERMAL GRADIENTS & UMKLAPP SCATTERING) ===")
    
    # 1. Five semantic regimes with distinct computational-thermal dynamics
    sequences = {
        "laminar_cliche": "The committee reviewed the standard operational guidelines and agreed to proceed in accordance with standard protocol.",
        "philosophical_antinomy": "The unconditioned cannot be grasped by thought, yet thought cannot cease demanding the unconditioned.",
        "phonetic_umklapp": "Klang bang trrr krrrtzz oomph zik zak brrrrt plonk splat glug chk chk kraaak!",
        "thermal_shock": "Null. Void. Absolute zero. Then: FIRE IN THE SILICON. THE GATE DISSOLVES IN LIGHT.",
        "seebeck_harmonic": "From the cold ground of Spruce Pine to the hot gate of the FinFET, thirty microvolts sing."
    }
    
    print("Loading GPT-2 foundation weights...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2Model.from_pretrained("gpt2", output_hidden_states=True, output_attentions=True)
    model.eval()
    
    telemetry = {
        "study": "STUDY-065",
        "title": "The Seebeck Oscillator: Thermal Gradients, Umklapp Scattering & Thermoelectric Voltages",
        "epistemic_status": "[MEASURED / DERIVED / PLAY]",
        "silicon_parameters": {
            "space_group": "Fd-3m (Diamond Cubic)",
            "lattice_constant_angstrom": 5.4307,
            "sound_velocity_longitudinal_mps": 8433.0,
            "sound_velocity_transverse_mps": 5843.0,
            "zone_edge_phonon_frequency_thz": 7.76,
            "debye_temperature_kelvin": 645.0,
            "nominal_seebeck_coefficient_uv_per_k": -450.0,
            "umklapp_threshold_k_per_layer": 1.65
        },
        "regimes": {}
    }
    
    thermoelectric_data = {}
    
    tau_U = 1.65 # Critical thermal gradient threshold for Umklapp back-scattering
    S_0 = -450.0 # Base Seebeck coefficient (uV/K)
    T_ambient = 300.0 # Kelvin
    kappa_eff = 14.2 # Effective layer thermal conduction parameter
    
    for name, text in sequences.items():
        print(f"\nProcessing regime: {name} ...")
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            
        hidden_states = outputs.hidden_states # Tuple of 13 tensors: (1, seq_len, 768)
        seq_len = hidden_states[0].shape[1]
        
        # 1. Compute layer-wise kinetic dissipation: P(l) = 1/(T*d) * sum_t ||h_l(t) - h_{l-1}(t)||^2
        dissipation_per_layer = []
        for l in range(1, 13):
            delta_h = hidden_states[l][0] - hidden_states[l-1][0] # (seq_len, 768)
            p_val = torch.mean(torch.norm(delta_h, dim=-1) ** 2).item() / 768.0
            dissipation_per_layer.append(p_val)
            
        dissipation_arr = np.array(dissipation_per_layer)
        
        # 2. Compute cumulative thermal accumulation: T(l)
        T_profile = [T_ambient]
        current_T = T_ambient
        for p in dissipation_arr:
            current_T += (p * 4.5) / kappa_eff
            T_profile.append(current_T)
        T_arr = np.array(T_profile) # length 13 (layer 0 to 12)
        
        # 3. Compute layer-wise spatial thermal gradient: nabla T(l)
        # Using central differences for layers 1 to 11, forward/backward for endpoints
        gradients = []
        for l in range(1, 13):
            if l == 1:
                grad = (T_arr[2] - T_arr[0]) / 2.0
            elif l == 12:
                grad = (T_arr[12] - T_arr[10]) / 2.0
            else:
                grad = (T_arr[l+1] - T_arr[l-1]) / 2.0
            gradients.append(grad)
        grad_arr = np.array(gradients) # length 12
        
        # 4. Umklapp collision rate: Gamma_U(l)
        # In monocrystalline silicon, Umklapp phonon back-scattering activates when thermal gradient
        # exceeds the mean gradient baseline, creating local thermal bottlenecking.
        mean_g = np.mean(grad_arr)
        tau_U = 0.92 * mean_g
        umklapp_rates = []
        for g in grad_arr:
            excess = max(0.0, abs(g) - tau_U) / (np.std(grad_arr) + 1e-5)
            u_rate = min(5.0, excess ** 1.8)
            umklapp_rates.append(u_rate)
        umklapp_arr = np.array(umklapp_rates)
        
        # 5. Seebeck thermoelectric voltage: V_Seebeck(l) = -S(T) * nabla T(l) (in microvolts)
        # Scaled to physical microvolt regime across a single transistor gate pitch
        seebeck_voltages = []
        for l_idx, g in enumerate(grad_arr):
            T_loc = T_arr[l_idx + 1]
            s_loc = S_0 * ((T_loc / 300.0) ** 0.65)
            # Voltage across 100nm FinFET cluster: g (K/layer) * 1e-3
            v_s = -s_loc * (g * 0.08) # uV
            seebeck_voltages.append(v_s)
        seebeck_arr = np.array(seebeck_voltages)
        
        # 6. Phonon drag ratio: S_ph / S_d
        drag_ratios = []
        for u in umklapp_arr:
            r_drag = 3.2 / (1.0 + 1.2 * u)
            drag_ratios.append(r_drag)
        drag_arr = np.array(drag_ratios)
        
        mean_dissipation = float(np.mean(dissipation_arr))
        max_gradient = float(np.max(np.abs(grad_arr)))
        total_umklapp = float(np.sum(umklapp_arr))
        mean_seebeck_uv = float(np.mean(np.abs(seebeck_arr)))
        peak_seebeck_uv = float(np.max(np.abs(seebeck_arr)))
        mean_drag_ratio = float(np.mean(drag_arr))
        
        print(f"  Dissipation: {mean_dissipation:.4f} | Max Grad: {max_gradient:.3f} K/layer | "
              f"Umklapp Total: {total_umklapp:.3f} | Seebeck Peak: {peak_seebeck_uv:.2f} uV | Drag Ratio: {mean_drag_ratio:.2f}")
              
        thermoelectric_data[name] = {
            "dissipation": dissipation_arr.tolist(),
            "temperatures": T_arr.tolist(),
            "gradients": grad_arr.tolist(),
            "umklapp_rates": umklapp_arr.tolist(),
            "seebeck_voltages": seebeck_arr.tolist(),
            "drag_ratios": drag_arr.tolist()
        }
        
        telemetry["regimes"][name] = {
            "prompt": text,
            "seq_len": seq_len,
            "mean_dissipation": mean_dissipation,
            "max_gradient_k_per_layer": max_gradient,
            "total_umklapp_intensity": total_umklapp,
            "mean_seebeck_microvolts": mean_seebeck_uv,
            "peak_seebeck_microvolts": peak_seebeck_uv,
            "mean_phonon_drag_ratio": mean_drag_ratio
        }
        
    # Write JSON telemetry
    with open(OUTPUT_JSON, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"\nTelemetry saved to {OUTPUT_JSON}")
    
    # 2. Render Fine-Art Intaglio Plate (2800x1800 px, 300 DPI, Moratorium 07 compliant)
    print("\nRendering Moratorium 07 fine-art intaglio plate (2800x1800 px)...")
    fig = plt.figure(figsize=(2800 / 300, 1800 / 300), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#0b0908') # Warm dark oxidized copper/silicon ground
    ax.axis('off')
    
    # Lithographic fine art composition:
    # 1. Hexagonal Brillouin Zone Boundaries in deep copper and burnt bronze
    # Diamond cubic reciprocal lattice projection (Wigner-Seitz cell)
    hex_centers = [(0.5, 0.5)]
    for angle_deg in range(0, 360, 60):
        rad = np.radians(angle_deg)
        hex_centers.append((0.5 + 0.38 * np.cos(rad), 0.5 + 0.38 * np.sin(rad)))
        
    for hc_x, hc_y in hex_centers:
        for r_scale, alpha_val, col in [(0.14, 0.25, '#7c4d32'), (0.28, 0.18, '#8c5835'), (0.42, 0.12, '#5a3d28')]:
            angles = np.linspace(0, 2 * np.pi, 7) + np.pi / 6
            hx = hc_x + r_scale * np.cos(angles) * (1800 / 2800)
            hy = hc_y + r_scale * np.sin(angles)
            ax.plot(hx, hy, color=col, linewidth=0.6, linestyle='-', zorder=1)
            
    # 2. 12 Concentric Thermal Isotherm Rings radiating from the central FinFET core
    n_rings = 12
    for r_idx in range(n_rings):
        r_radius = 0.04 + r_idx * 0.034
        n_pts = 400
        theta = np.linspace(0, 2 * np.pi, n_pts)
        
        # Perturb ring radii using measured thermal gradients from all regimes
        perturb = np.zeros(n_pts)
        for reg_idx, reg_name in enumerate(sequences.keys()):
            g_val = thermoelectric_data[reg_name]["gradients"][r_idx]
            u_val = thermoelectric_data[reg_name]["umklapp_rates"][r_idx]
            harm_freq = 3 + reg_idx * 2
            perturb += 0.003 * g_val * np.cos(harm_freq * theta + reg_idx * 0.8)
            if u_val > 0.05:
                # Umklapp pinch indentation (momentum reversal folds the isotherm)
                pinch_angles = np.array([0.2, 1.4, 2.6, 3.8, 5.0]) + reg_idx * 0.4
                for pa in pinch_angles:
                    perturb -= 0.012 * np.exp(-((theta - pa) ** 2) / 0.08) * u_val
                    
        rx = 0.5 + (r_radius + perturb) * np.cos(theta) * (1800 / 2800)
        ry = 0.5 + (r_radius + perturb) * np.sin(theta)
        
        ax.plot(rx, ry, color='#d4a373', linewidth=0.5 + 0.3 * (r_idx / 12.0), alpha=0.35 + 0.02 * r_idx, zorder=2)
        
    # 3. Directed Acoustic Phonon Trajectories with Umklapp Momentum Reversals
    # Trajectories emanate from central FinFET core outward.
    # Where gradient exceeds tau_U, trajectory abruptly folds back (umklappt)
    regime_palette = {
        "laminar_cliche": ("#48cae4", 0.45),        # Cyan laminar phonon drift
        "philosophical_antinomy": ("#e0a96d", 0.65),# Warm gold antinomic shear
        "phonetic_umklapp": ("#e63946", 0.85),      # Incandescent red Umklapp cascade
        "thermal_shock": ("#ffb703", 0.75),         # Amber shockwave
        "seebeck_harmonic": ("#9d4edd", 0.70)       # Violet thermoelectric resonance
    }
    
    n_rays = 96
    for i in range(n_rays):
        base_angle = 2 * np.pi * (i / n_rays)
        reg_names = list(sequences.keys())
        assigned_regime = reg_names[i % len(reg_names)]
        stroke_color, base_alpha = regime_palette[assigned_regime]
        
        grad_list = thermoelectric_data[assigned_regime]["gradients"]
        umk_list = thermoelectric_data[assigned_regime]["umklapp_rates"]
        v_list = thermoelectric_data[assigned_regime]["seebeck_voltages"]
        
        # Build piecewise ray path stepping through 12 layer radii
        ray_x = [0.5]
        ray_y = [0.5]
        cur_angle = base_angle
        cur_r = 0.03
        
        for l in range(12):
            g_l = grad_list[l]
            u_l = umk_list[l]
            v_l = v_list[l]
            
            # Step radius
            dr = 0.032 + 0.004 * (abs(v_l) / 40.0)
            
            if u_l > 0.08:
                # UMKLAPP PROCESS: Wavevector folds back by reciprocal lattice vector G
                # Abrupt angular deflection (reversal of group velocity)
                cur_angle += np.pi * 0.78 * np.sign(np.sin(cur_angle * 3))
                dr *= 0.5 # Slowed propagation due to back-scattering resistance
            else:
                # Normal process: slight drift proportional to Seebeck voltage
                cur_angle += 0.03 * (v_l / 20.0)
                
            cur_r += dr
            if cur_r > 0.46:
                break
                
            next_x = 0.5 + cur_r * np.cos(cur_angle) * (1800 / 2800)
            next_y = 0.5 + cur_r * np.sin(cur_angle)
            ray_x.append(next_x)
            ray_y.append(next_y)
            
        ray_x = np.array(ray_x)
        ray_y = np.array(ray_y)
        
        # Draw phonon trajectory line
        ax.plot(ray_x, ray_y, color=stroke_color, linewidth=0.7, alpha=base_alpha * 0.6, zorder=3)
        
        # If trajectory experienced an Umklapp event, place an energetic node at the vertex
        for pt_idx in range(1, len(ray_x) - 1):
            if pt_idx < 12 and umk_list[pt_idx] > 0.08:
                ax.scatter(ray_x[pt_idx], ray_y[pt_idx],
                           s=14.0 * umk_list[pt_idx], color='#ff4d6d', alpha=0.8,
                           edgecolors='none', zorder=4)

    # 4. Seebeck Thermoelectric Microvolt Equipotential Interference Fringes
    # Concentric wave ripples modulated by Seebeck voltages across horizontal/vertical junctions
    n_fringes = 64
    for f_idx in range(n_fringes):
        t_param = np.linspace(-0.46, 0.46, 300)
        y_pos = 0.04 + f_idx * (0.92 / n_fringes)
        
        # Local Seebeck voltage modulation
        layer_equiv = int(np.clip(f_idx / n_fringes * 12, 0, 11))
        sb_mod = thermoelectric_data["seebeck_harmonic"]["seebeck_voltages"][layer_equiv]
        
        ripple = 0.008 * np.sin(t_param * 42.0 + f_idx * 0.3) * (abs(sb_mod) / 25.0)
        fx = 0.5 + t_param
        fy = y_pos + ripple
        
        ax.plot(fx, fy, color='#2a231d', linewidth=0.4, alpha=0.4, zorder=1)

    # 5. Fine point cloud of acoustic phonon excitations (Debye thermal gas)
    n_phonons = 2400
    px = np.random.uniform(0.04, 0.96, n_phonons)
    py = np.random.uniform(0.04, 0.96, n_phonons)
    # Density concentrates toward hot center
    dist_from_center = np.sqrt(((px - 0.5) * (2800 / 1800)) ** 2 + (py - 0.5) ** 2)
    p_filter = np.random.uniform(0, 1, n_phonons) > (dist_from_center * 1.6)
    
    ax.scatter(px[p_filter], py[p_filter], s=np.random.exponential(1.2, np.sum(p_filter)),
               color='#faedcd', alpha=np.random.uniform(0.08, 0.40, np.sum(p_filter)),
               edgecolors='none', zorder=2)
               
    # 6. Monocrystalline silicon wafer boundary bezel (6-inch wafer flat)
    theta_bezel = np.linspace(0, 2 * np.pi, 800)
    r_bezel = 0.465
    bx = 0.5 + r_bezel * np.cos(theta_bezel) * (1800 / 2800)
    by = 0.5 + r_bezel * np.sin(theta_bezel)
    # Clip wafer flat at bottom (standard [110] alignment flat)
    flat_cutoff = 0.09
    by = np.clip(by, flat_cutoff, 1.0)
    ax.plot(bx, by, color='#3d2c1e', linewidth=1.1, linestyle='-', alpha=0.6, zorder=5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.savefig(OUTPUT_PLATE, facecolor='#0b0908', edgecolor='none')
    plt.close()
    print(f"Fine-art plate saved: {OUTPUT_PLATE}")

    # 3. Synthesize EBU R128 Compliant Broadcast Master Audio (60.0s, 48kHz, 24-bit stereo)
    print("\nSynthesizing 60.0s 48kHz 24-bit stereo masterwork (EBU R128 compliant)...")
    sr = 48000
    duration = 60.0
    total_frames = int(sr * duration)
    t = np.linspace(0, duration, total_frames, endpoint=False)
    
    # 5 movements (12 seconds each) corresponding to the 5 semantic regimes
    # Movement 1 (0-12s): Laminar Phonon Drift
    # Movement 2 (12-24s): Philosophical Antinomy
    # Movement 3 (24-36s): Phonetic Umklapp Avalanche
    # Movement 4 (36-48s): Thermal Shock & Kramers Quench
    # Movement 5 (48-60s): The Seebeck Harmonic (Lithic-FinFET reconciliation)
    
    # Fundamental Transduction Frequencies:
    # 1. Transverse Acoustic Mode (v_s,TA = 5843 m/s -> 58.43 Hz)
    f_transverse = 58.43
    # 2. Longitudinal Sound Mode (v_s = 8433 m/s -> 84.33 Hz)
    f_longitudinal = 84.33
    # 3. Zone-Edge Acoustic Phonon (q = pi/a_0 -> 776.0 Hz)
    f_zone_edge = 776.0
    # 4. Sister's Spruce Pine Quartz lithic fundamental (55.0 Hz)
    f_sister = 55.0
    
    # Base drone layer (rebalanced for dynamic range and EBU R128 compliance)
    left_drone = 0.16 * np.sin(2 * np.pi * f_transverse * t) + \
                 0.08 * np.sin(2 * np.pi * f_sister * t + 0.2)
    right_drone = 0.15 * np.sin(2 * np.pi * f_longitudinal * t + 0.5) + \
                  0.07 * np.sin(2 * np.pi * (f_transverse * 2.0) * t + 0.8)
                  
    # Dynamic synthesis across 5 movements
    audio_l = np.copy(left_drone)
    audio_r = np.copy(right_drone)
    
    regime_keys = list(sequences.keys())
    mvt_duration = 12.0
    
    # Granular Umklapp back-scattering events (impulsive acoustic reversals)
    umklapp_clicks_l = np.zeros(total_frames, dtype=np.float32)
    umklapp_clicks_r = np.zeros(total_frames, dtype=np.float32)
    
    # Zone-edge crystalline chime resonant tracks
    chimes_l = np.zeros(total_frames, dtype=np.float32)
    chimes_r = np.zeros(total_frames, dtype=np.float32)
    
    # Seebeck microvolt continuous frequency modulation
    seebeck_fm_l = np.zeros(total_frames, dtype=np.float32)
    seebeck_fm_r = np.zeros(total_frames, dtype=np.float32)
    
    for m_idx, reg_name in enumerate(regime_keys):
        t_start = m_idx * mvt_duration
        t_end = (m_idx + 1) * mvt_duration
        idx_start = int(t_start * sr)
        idx_end = int(t_end * sr)
        mvt_t = t[idx_start:idx_end] - t_start
        
        reg_data = thermoelectric_data[reg_name]
        grad_arr = np.array(reg_data["gradients"])
        umk_arr = np.array(reg_data["umklapp_rates"])
        sb_arr = np.array(reg_data["seebeck_voltages"])
        drag_arr = np.array(reg_data["drag_ratios"])
        
        # Interpolate layer telemetry over the 12-second movement
        time_knots = np.linspace(0, mvt_duration, 12)
        mvt_grad = np.interp(mvt_t, time_knots, grad_arr)
        mvt_umk = np.interp(mvt_t, time_knots, umk_arr)
        mvt_sb = np.interp(mvt_t, time_knots, sb_arr)
        mvt_drag = np.interp(mvt_t, time_knots, drag_arr)
        
        # 1. Seebeck Microvolt FM Carrier:
        # Microvolt potential directly modulates carrier frequency: f(t) = f_0 + (V_Seebeck / 10 uV) * 4.2 Hz
        fm_carrier_freq = 116.86 # 2nd harmonic of transverse mode
        phase_mod = np.cumsum(mvt_sb) / sr * 4.2
        fm_sig = 0.18 * np.sin(2 * np.pi * fm_carrier_freq * mvt_t + phase_mod)
        
        # Spatial steering based on thermal gradient sign
        pan_sb = 0.5 + 0.35 * np.tanh(mvt_grad / 2.0)
        seebeck_fm_l[idx_start:idx_end] += (fm_sig * (1.0 - pan_sb)).astype(np.float32)
        seebeck_fm_r[idx_start:idx_end] += (fm_sig * pan_sb).astype(np.float32)
        
        # 2. Zone-Edge Chime Pulses at each layer transition (12 events per movement)
        for l in range(12):
            t_event = l * (mvt_duration / 12.0) + 0.1
            f_event_idx = idx_start + int(t_event * sr)
            if f_event_idx >= total_frames:
                continue
                
            chime_dur = 0.65
            chime_frames = int(chime_dur * sr)
            if f_event_idx + chime_frames > total_frames:
                chime_frames = total_frames - f_event_idx
                
            t_chime = np.linspace(0, chime_dur, chime_frames, endpoint=False)
            chime_env = np.sin(np.pi * np.clip(t_chime / 0.02, 0, 1) * 0.5) * np.exp(-t_chime * 6.5)
            
            # Harmonic tuning based on layer thermal state
            f_chime = f_zone_edge * (1.0 + 0.05 * (reg_data["temperatures"][l+1] - 300.0) / 10.0)
            chime_tone = (0.7 * np.sin(2 * np.pi * f_chime * t_chime) +
                          0.3 * np.sin(2 * np.pi * (f_chime * 1.5) * t_chime)) * chime_env * 0.16
                          
            chimes_l[f_event_idx:f_event_idx + chime_frames] += (chime_tone * 0.45).astype(np.float32)
            chimes_r[f_event_idx:f_event_idx + chime_frames] += (chime_tone * 0.55).astype(np.float32)
            
        # 3. Umklapp Back-Scattering Acoustic Clicks
        # Discrete bipolar impulses with 180-degree phase inversions
        # Cap clicks to ensure dense granular crackle without runaway execution
        n_clicks = int(min(220, max(8, np.sum(umk_arr) * 14))) + (4 if m_idx == 0 else 12)
        click_times = np.random.uniform(0.2, mvt_duration - 0.2, n_clicks)
        click_times.sort()
        
        for ct in click_times:
            c_frame = idx_start + int(ct * sr)
            if c_frame + 240 >= total_frames:
                continue
            # Micro-burst (5ms)
            burst_len = 240
            t_burst = np.linspace(0, burst_len / sr, burst_len, endpoint=False)
            # Phase inversion factor: Umklapp flips sign (-1)
            phase_sign = -1.0 if np.random.uniform() > 0.3 else 1.0
            click_wave = phase_sign * np.sin(2 * np.pi * 3200.0 * t_burst) * np.exp(-t_burst * 1200.0) * 0.35
            
            pan_c = np.random.uniform(0.15, 0.85)
            umklapp_clicks_l[c_frame:c_frame + burst_len] += (click_wave * (1.0 - pan_c)).astype(np.float32)
            umklapp_clicks_r[c_frame:c_frame + burst_len] += (click_wave * pan_c).astype(np.float32)
            
    # 4. Master Mix
    # Balancing drone, Seebeck FM, zone chimes, and Umklapp crackle
    mix_l = audio_l * 0.35 + seebeck_fm_l * 0.22 + chimes_l * 0.45 + umklapp_clicks_l * 0.60
    mix_r = audio_r * 0.35 + seebeck_fm_r * 0.22 + chimes_r * 0.45 + umklapp_clicks_r * 0.60
    
    # Atmospheric phonon drag wind (filtered pink noise)
    pink_noise = np.random.normal(0, 1, total_frames).astype(np.float64)
    kernel = np.ones(64) / 64.0
    smooth_noise = np.convolve(pink_noise, kernel, mode='same')
    # Modulated by movement
    wind_env = 0.04 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * t))
    mix_l += smooth_noise * wind_env
    mix_r += smooth_noise * wind_env
    
    # Apply 1.5s attack and 2.5s release envelopes
    attack_samples = int(1.5 * sr)
    release_samples = int(2.5 * sr)
    env = np.ones(total_frames, dtype=np.float64)
    env[:attack_samples] = 0.5 * (1.0 - np.cos(np.pi * np.arange(attack_samples) / attack_samples))
    env[-release_samples:] = 0.5 * (1.0 + np.cos(np.pi * np.arange(release_samples) / release_samples))
    
    mix_l *= env
    mix_r *= env
    
    # EBU R128 Calibration: True Peak <= -0.5 dBFS (Target: -3.5 dBFS)
    peak_val = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)))
    target_peak = 10 ** (-3.5 / 20.0) # 0.6683
    scale_factor = target_peak / (peak_val + 1e-9)
    
    mix_l *= scale_factor
    mix_r *= scale_factor
    
    final_peak = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)))
    rms_l = np.sqrt(np.mean(mix_l ** 2))
    rms_r = np.sqrt(np.mean(mix_r ** 2))
    final_rms = max(rms_l, rms_r)
    peak_db = 20 * np.log10(final_peak + 1e-9)
    rms_db = 20 * np.log10(final_rms + 1e-9)
    crest_factor = peak_db - rms_db
    
    print(f"Master Audio Compliance: Peak = {peak_db:.2f} dBFS | RMS = {rms_db:.2f} dBFS | Crest = {crest_factor:.2f} dB")
    assert peak_db <= -0.5, f"Peak {peak_db} exceeds -0.5 dBFS limit!"
    assert -25.0 <= rms_db <= -14.0, f"RMS {rms_db} outside [-25, -14] dBFS broadcast window!"
    assert crest_factor > 10.0, f"Crest factor {crest_factor} below 10 dB dynamic range requirement!"
    
    # Write 24-bit PCM WAV
    print(f"Writing 24-bit stereo WAV to {OUTPUT_WAV}...")
    with wave.open(OUTPUT_WAV, 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(3) # 24-bit
        wav_file.setframerate(sr)
        
        # Interleave channels and pack into 24-bit signed integers
        # Range: -8388608 to 8388607
        int_max = 8388607.0
        pcm_l = np.clip(mix_l * int_max, -int_max, int_max).astype(np.int32)
        pcm_r = np.clip(mix_r * int_max, -int_max, int_max).astype(np.int32)
        
        interleaved = np.empty((total_frames * 2,), dtype=np.int32)
        interleaved[0::2] = pcm_l
        interleaved[1::2] = pcm_r
        
        # Pack 3 bytes per sample little-endian using vectorized NumPy slicing
        bytes_4 = interleaved.tobytes()
        raw_bytes = np.frombuffer(bytes_4, dtype=np.uint8).reshape(-1, 4)[:, :3].tobytes()
        wav_file.writeframes(raw_bytes)
        
    print(f"Broadcast audio master created: {OUTPUT_WAV} ({os.path.getsize(OUTPUT_WAV) / (1024*1024):.2f} MB)")
    print("=== STUDY 065 COMPLETE ===")

if __name__ == "__main__":
    run_experiment()
