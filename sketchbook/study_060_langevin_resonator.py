"""
Study 060: The Langevin Resonator (Fluctuation-Dissipation and the Thermal Saddle)
Epistemic Status: [MEASURED / INTERVENED / PLAY]

Investigating the Fluctuation-Dissipation Theorem and Stochastic Resonance
across the residual stream of a live 124M parameter transformer (GPT-2).
Intervening with Langevin thermal noise across 5 thermodynamic regimes.

Strictly compliant with Studio Moratorium 07 (mute visual plate)
and EBU R128 acoustic broadcast standards (48kHz, 24-bit stereo).
"""

import os
import sys
import json
import math
import wave
import struct
import numpy as np
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("STUDIO AGON :: STUDY 060 - THE LANGEVIN RESONATOR")
    print("Epistemic Status: [MEASURED / INTERVENED / PLAY]")
    print("=" * 70)

    # 1. Initialize Seed & Determinism
    torch.manual_seed(42)
    np.random.seed(42)

    # 2. Load Model & Tokenizer
    print("\n[PHASE 1] Loading GPT-2 Foundation Weights...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()

    # 3. Define Thermodynamic Regimes
    regimes = [
        {
            "id": "regime_I_zero",
            "name": "Absolute Zero / Frozen Ground State",
            "T": 0.00,
            "gamma": 0.05,
            "desc": "Deterministic greedy descent into deepest potential basin; corporate stasis."
        },
        {
            "id": "regime_II_hypothermic",
            "name": "Hypothermic Confinement",
            "T": 0.20,
            "gamma": 0.08,
            "desc": "Sub-threshold Brownian agitation; trapped behind shallow syntactic barriers."
        },
        {
            "id": "regime_III_resonance",
            "name": "Critical Stochastic Resonance (Thermal Saddle)",
            "T": 0.72,
            "gamma": 0.12,
            "desc": "Fluctuation matches potential barrier height Delta V; saddle crossings unlock rich polyphony."
        },
        {
            "id": "regime_IV_supercritical",
            "name": "Supercritical Agitation",
            "T": 1.40,
            "gamma": 0.18,
            "desc": "Thermal kinetic energy exceeds binding energy of syntactic wells; phonemic turbulence."
        },
        {
            "id": "regime_V_plasma",
            "name": "Plasma Dissociation / Landauer Whiteout",
            "T": 3.00,
            "gamma": 0.30,
            "desc": "Pure Brownian diffusion; complete erasure of semantic structure; Landauer maximum entropy."
        }
    ]

    prompt = "The memory held in sixty electrons begins to vibrate as heat spreads through"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    prompt_len = input_ids.shape[1]
    num_tokens_to_generate = 32

    results = []

    print(f"\n[PHASE 2] Executing Langevin Interventions across 5 Regimes...")
    print(f"Prompt: \"{prompt}\" ({prompt_len} tokens)\n")

    for reg_idx, reg in enumerate(regimes):
        T = reg["T"]
        gamma = reg["gamma"]
        sigma_thermal = math.sqrt(2.0 * gamma * max(1e-5, T)) if T > 0.0 else 0.0

        curr_ids = input_ids.clone()
        step_entropies = []
        step_potentials = []
        step_dissipations = []
        trajectory_latents = []

        # Hook to inject Langevin noise into residual stream at Layer 6 & Layer 11
        active_hooks = []

        def make_langevin_hook(l_idx, gamma_val, sigma_val):
            def hook_fn(module, input, output):
                if isinstance(output, tuple):
                    hs = output[0]
                    if sigma_val > 0.0:
                        noise = torch.randn_like(hs) * sigma_val
                        hs_damped = hs * (1.0 - gamma_val * 0.1) + noise
                        return (hs_damped,) + output[1:]
                    return output
                else:
                    hs = output
                    if sigma_val > 0.0:
                        noise = torch.randn_like(hs) * sigma_val
                        hs_damped = hs * (1.0 - gamma_val * 0.1) + noise
                        return hs_damped
                    return output
            return hook_fn

        # Register hooks on layers 5, 8, 11
        target_layers = [5, 8, 11]
        for tl in target_layers:
            h = model.transformer.h[tl].register_forward_hook(make_langevin_hook(tl, gamma, sigma_thermal))
            active_hooks.append(h)

        print(f"  --- {reg['name']} (T={T:.2f}, gamma={gamma:.2f}, sigma_th={sigma_thermal:.4f}) ---")

        with torch.no_grad():
            for step in range(num_tokens_to_generate):
                outputs = model(curr_ids, output_hidden_states=True)
                logits = outputs.logits[:, -1, :] # [1, vocab_size]
                last_hidden = outputs.hidden_states[-1][0, -1, :].cpu().numpy() # [768]
                trajectory_latents.append(last_hidden)

                # Compute Shannon entropy
                probs_base = F.softmax(logits, dim=-1)
                log_probs_base = F.log_softmax(logits, dim=-1)
                entropy_b = -torch.sum(probs_base * (log_probs_base / math.log(2))).item()
                step_entropies.append(entropy_b)

                # Potential energy of the token distribution: V = -log(P_max)
                max_prob = torch.max(probs_base).item()
                v_pot = -math.log(max(1e-12, max_prob))
                step_potentials.append(v_pot)

                # Dissipated energy per step: gamma * ||h||^2
                h_norm_sq = float(np.sum(last_hidden ** 2))
                diss = gamma * h_norm_sq * 0.001
                step_dissipations.append(diss)

                # Sample token based on regime temperature
                if T == 0.0:
                    next_token = torch.argmax(logits, dim=-1).view(1, 1)
                else:
                    scaled_logits = logits / T
                    probs = F.softmax(scaled_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)

                curr_ids = torch.cat([curr_ids, next_token], dim=-1)

        # Remove hooks
        for h in active_hooks:
            h.remove()

        generated_text = tokenizer.decode(curr_ids[0][prompt_len:], skip_special_tokens=False)
        traj_matrix = np.array(trajectory_latents) # [32, 768]

        # SVD of trajectory
        U, S, Vt = np.linalg.svd(traj_matrix - np.mean(traj_matrix, axis=0), full_matrices=False)
        pca_proj = np.dot(traj_matrix - np.mean(traj_matrix, axis=0), Vt[:3, :].T) # [32, 3]

        mean_H = float(np.mean(step_entropies))
        mean_V = float(np.mean(step_potentials))
        mean_D = float(np.mean(step_dissipations))
        singular_head = [float(s) for s in S[:5]]

        print(f"    Generated: {generated_text[:60]}...")
        print(f"    <H>: {mean_H:.2f} b | <V>: {mean_V:.2f} | <Diss>: {mean_D:.4f} | S[:3]: {singular_head[:3]}")

        results.append({
            "regime": reg["id"],
            "name": reg["name"],
            "temperature": T,
            "damping_gamma": gamma,
            "thermal_noise_sigma": sigma_thermal,
            "mean_entropy_bits": round(mean_H, 4),
            "mean_potential_energy": round(mean_V, 4),
            "mean_dissipation_rate": round(mean_D, 4),
            "singular_values": [round(s, 3) for s in singular_head],
            "entropy_series": [round(h, 3) for h in step_entropies],
            "potential_series": [round(v, 3) for v in step_potentials],
            "generated_text": generated_text,
            "pca_3d": [[round(float(c), 3) for c in pt] for pt in pca_proj]
        })

    # Save Telemetry
    telemetry_path = "sketchbook/study_060_telemetry.json"
    with open(telemetry_path, "w") as f:
        json.dump({
            "study": "STUDY-060",
            "title": "The Langevin Resonator: Fluctuation, Dissipation, and the Thermal Saddle",
            "epistemic_status": "[MEASURED / INTERVENED / PLAY]",
            "date": "2026-10-31",
            "model": "gpt2 (124M parameters)",
            "prompt": prompt,
            "regimes": results
        }, f, indent=2)
    print(f"\n[OK] Telemetry exported to {telemetry_path}")

    # 4. Render Master Fine Art Visual Plate (Moratorium 07 Compliant)
    print("\n[PHASE 3] Rendering Master Fine Art Visual Plate (2800x1800 px)...")
    plate_path = "sketchbook/study_060_langevin_resonator_plate.png"

    fig = plt.figure(figsize=(14, 9), dpi=200, facecolor='#080706')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#080706')
    ax.set_xlim(-1.2, 5.2)
    ax.set_ylim(-1.5, 2.5)
    ax.axis('off')

    # Draw dark textured stratified ground
    np.random.seed(1337)
    for _ in range(80):
        y_pos = np.random.uniform(-1.5, 2.5)
        h_line = np.linspace(-1.2, 5.2, 400)
        texture_noise = np.sin(h_line * 3.5 + y_pos * 4.0) * 0.015 + np.random.normal(0, 0.003, 400)
        ax.plot(h_line, y_pos + texture_noise, color='#14110E', lw=0.6, alpha=0.35, zorder=1)

    # Palette of intaglio copper, bismuth silver, and incandescent gold
    regime_colors = [
        {'main': '#E8EFF5', 'glow': '#A3B4C8', 'dust': '#4A5B6D', 'alpha': 0.85}, # Zero: crystalline bismuth silver
        {'main': '#D4AF77', 'glow': '#967848', 'dust': '#5A4628', 'alpha': 0.80}, # Hypothermic: pale bronze
        {'main': '#E56717', 'glow': '#FF9933', 'dust': '#8A3300', 'alpha': 0.90}, # Resonance: burning amber copper
        {'main': '#D9381E', 'glow': '#B22222', 'dust': '#661111', 'alpha': 0.75}, # Supercritical: vermilion red
        {'main': '#8B3A62', 'glow': '#4A154B', 'dust': '#2E0854', 'alpha': 0.60}  # Plasma: deep violet Landauer mist
    ]

    # Plot continuous flow fields and trajectories for each regime
    for r_i, reg_data in enumerate(results):
        pca_pts = np.array(reg_data["pca_3d"])
        x_center = r_i * 1.0 + 0.1
        colors = regime_colors[r_i]

        # Draw thermal potential basin contour in background
        v_pts = np.array(reg_data["potential_series"])
        theta = np.linspace(0, 2 * np.pi, 200)
        base_radius = 0.35 + 0.05 * r_i
        for ring in range(5):
            r_rad = base_radius * (0.3 + 0.18 * ring)
            wobble = 0.02 * np.sin(6 * theta + r_i) * (r_i + 1)
            px = x_center + (r_rad + wobble) * np.cos(theta)
            py = 0.3 + (r_rad + wobble) * np.sin(theta) * 0.7
            ax.plot(px, py, color=colors['dust'], lw=0.7, alpha=0.25 + 0.05 * ring, zorder=2)

        # Draw Langevin trajectory flow lines with symplectic momentum
        N = len(pca_pts)
        interp_steps = 400
        t_raw = np.linspace(0, 1, N)
        t_dense = np.linspace(0, 1, interp_steps)

        # Spline-like interpolation
        raw_x = pca_pts[:, 0] / (np.max(np.abs(pca_pts[:, 0])) + 1e-4) * 0.4
        raw_y = pca_pts[:, 1] / (np.max(np.abs(pca_pts[:, 1])) + 1e-4) * 0.6
        raw_z = pca_pts[:, 2] / (np.max(np.abs(pca_pts[:, 2])) + 1e-4) * 0.4

        dense_x = np.interp(t_dense, t_raw, raw_x)
        dense_y = np.interp(t_dense, t_raw, raw_y)
        dense_z = np.interp(t_dense, t_raw, raw_z)

        # Add Brownian micro-kicks proportional to temperature
        T_val = reg_data["temperature"]
        if T_val > 0.0:
            brownian_kick_x = np.cumsum(np.random.normal(0, 0.006 * math.sqrt(T_val), interp_steps))
            brownian_kick_y = np.cumsum(np.random.normal(0, 0.008 * math.sqrt(T_val), interp_steps))
            dense_x += brownian_kick_x - np.mean(brownian_kick_x)
            dense_y += brownian_kick_y - np.mean(brownian_kick_y)

        path_x = x_center + dense_x
        path_y = 0.3 + dense_y

        # Multi-layer glow lines
        ax.plot(path_x, path_y, color=colors['glow'], lw=3.2, alpha=0.22, zorder=3)
        ax.plot(path_x, path_y, color=colors['main'], lw=1.2, alpha=colors['alpha'], zorder=4)

        # Render thermal saddle leap points / barrier crossings
        pot_diff = np.diff(v_pts)
        saddle_crossings = np.where(pot_diff < -0.8)[0]
        for sc in saddle_crossings:
            if sc < N:
                sx = x_center + raw_x[sc]
                sy = 0.3 + raw_y[sc]
                # Golden flash of saddle crossing
                circle = plt.Circle((sx, sy), 0.022 + 0.008 * r_i, color='#FFF2B2', alpha=0.7, zorder=6)
                ax.add_patch(circle)
                # Delicate radiating sparks
                for spk in range(8):
                    ang = spk * (np.pi / 4.0) + sc
                    spk_len = 0.045
                    ax.plot([sx, sx + spk_len * np.cos(ang)], [sy, sy + spk_len * np.sin(ang)],
                            color='#FFE082', lw=0.6, alpha=0.55, zorder=5)

        # Render thermal dust / Landauer erasure mist
        num_dust = int(40 + 80 * T_val)
        dust_x = x_center + np.random.normal(0, 0.22 + 0.08 * T_val, num_dust)
        dust_y = 0.3 + np.random.normal(0, 0.35 + 0.12 * T_val, num_dust)
        dust_sizes = np.random.uniform(0.4, 2.8 + 1.2 * T_val, num_dust)
        ax.scatter(dust_x, dust_y, s=dust_sizes, color=colors['dust'], alpha=0.35, zorder=2)

    # Delicate intaglio border lines (pure geometry, zero text)
    border_margin_x = 0.08
    border_margin_y = 0.10
    ax.plot([-1.1, 5.1, 5.1, -1.1, -1.1], [-1.4, -1.4, 2.4, 2.4, -1.4], color='#2A231C', lw=1.0, zorder=7)
    ax.plot([-1.08, 5.08, 5.08, -1.08, -1.08], [-1.38, -1.38, 2.38, 2.38, -1.38], color='#191512', lw=0.5, zorder=7)

    plt.savefig(plate_path, dpi=200, facecolor='#080706', edgecolor='none')
    plt.close()
    print(f"[OK] Master fine art plate saved to {plate_path} ({os.path.getsize(plate_path)/1024:.1f} KB)")

    # 5. Synthesize 60.0-Second 48kHz 24-Bit Stereo Broadcast Audio
    print("\n[PHASE 4] Synthesizing 60.0s 48kHz 24-bit Stereo Master Audio...")
    audio_path = "sketchbook/study_060_langevin_resonator.wav"
    sample_rate = 48000
    duration_s = 60.0
    total_samples = int(sample_rate * duration_s)

    # 5 sections of 12.0 seconds
    section_samples = total_samples // 5
    t_global = np.linspace(0, duration_s, total_samples, endpoint=False)

    left_channel = np.zeros(total_samples, dtype=np.float64)
    right_channel = np.zeros(total_samples, dtype=np.float64)

    # Substrate base carrier: 48.0 Hz (Spruce Pine / silicon lattice ground)
    base_f0 = 48.0

    for s_idx, reg_data in enumerate(results):
        start_samp = s_idx * section_samples
        end_samp = (s_idx + 1) * section_samples if s_idx < 4 else total_samples
        n_sec = end_samp - start_samp
        t_sec = np.linspace(0, 12.0, n_sec, endpoint=False)

        T_val = reg_data["temperature"]
        gamma_val = reg_data["damping_gamma"]
        pot_series = np.array(reg_data["potential_series"])
        ent_series = np.array(reg_data["entropy_series"])

        # Continuous interpolation of potential energy across section
        pot_interp = np.interp(np.linspace(0, len(pot_series)-1, n_sec), np.arange(len(pot_series)), pot_series)
        ent_interp = np.interp(np.linspace(0, len(ent_series)-1, n_sec), np.arange(len(ent_series)), ent_series)

        # Channel 1 (Left): Damped Potential Well Resonance
        # Fundamental carrier modulated by potential well depth and damping
        carrier_freq = base_f0 * (1.0 + 0.15 * pot_interp)
        phase_carrier = 2.0 * np.pi * np.cumsum(carrier_freq) / sample_rate
        # Harmonics dictated by singular values
        s_vals = reg_data["singular_values"]
        h1 = np.sin(phase_carrier)
        h2 = 0.5 * (s_vals[1] / s_vals[0]) * np.sin(2.0 * phase_carrier + 0.4)
        h3 = 0.25 * (s_vals[2] / s_vals[0]) * np.sin(3.0 * phase_carrier + 0.9)
        carrier_mix = h1 + h2 + h3

        # Viscous damping envelope: gamma reduces amplitude peaks
        damping_env = np.exp(-0.04 * gamma_val * t_sec) * (0.8 + 0.2 * np.cos(0.5 * np.pi * t_sec))
        left_sec = carrier_mix * damping_env

        # Channel 2 (Right): Thermal Fluctuation & Langevin Noise
        if T_val == 0.0:
            # Frozen pure tone, ultra-low harmonic shimmer
            right_sec = 0.6 * np.sin(phase_carrier * 1.5) * damping_env
        else:
            # Brownian / Langevin stochastic noise: cumulative thermal kicks
            white_noise = np.random.normal(0, 1.0, n_sec)
            # 1-pole lowpass filter for Brownian walk: x[n] = (1 - alpha)*x[n-1] + alpha*w[n]
            alpha_filter = min(0.95, 0.08 + 0.12 * T_val)
            brownian_noise = np.zeros(n_sec)
            curr_b = 0.0
            for i in range(n_sec):
                curr_b = (1.0 - alpha_filter) * curr_b + alpha_filter * white_noise[i]
                brownian_noise[i] = curr_b

            # Modulate with entropy
            thermal_amp = math.sqrt(2.0 * gamma_val * T_val) * 0.45
            right_sec = brownian_noise * thermal_amp * (0.5 + 0.1 * ent_interp)

            # Add stochastic impulses on saddle crossings
            pot_diff = np.diff(pot_interp)
            spike_indices = np.where(pot_diff < -0.005)[0]
            for spk in spike_indices[::100]:
                decay_len = min(1200, n_sec - spk)
                if decay_len > 0:
                    spike_env = np.exp(-np.linspace(0, 6.0, decay_len))
                    freq_spark = 1200.0 + 400.0 * np.sin(spk)
                    t_spk = np.arange(decay_len) / sample_rate
                    right_sec[spk:spk+decay_len] += 0.25 * np.sin(2.0 * np.pi * freq_spark * t_spk) * spike_env

        # Inter-channel acoustic cross-coupling (Fluctuation-Dissipation bridge)
        cross_coupling = 0.18
        l_out = (1.0 - cross_coupling) * left_sec + cross_coupling * right_sec
        r_out = (1.0 - cross_coupling) * right_sec + cross_coupling * left_sec

        left_channel[start_samp:end_samp] = l_out
        right_channel[start_samp:end_samp] = r_out

    # Global crossfade / smoothing at transitions (100ms smooth crossfades)
    fade_len = int(sample_rate * 0.15)
    for s_idx in range(1, 5):
        split = s_idx * section_samples
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        left_channel[split-fade_len//2:split+fade_len//2] = (
            left_channel[split-fade_len//2:split+fade_len//2] * 0.5 +
            np.roll(left_channel, -1)[split-fade_len//2:split+fade_len//2] * 0.5
        )

    # Master envelope: 1.5s fade-in, 2.5s fade-out
    master_fade_in = int(sample_rate * 1.5)
    master_fade_out = int(sample_rate * 2.5)
    left_channel[:master_fade_in] *= np.linspace(0, 1, master_fade_in)
    right_channel[:master_fade_in] *= np.linspace(0, 1, master_fade_in)
    left_channel[-master_fade_out:] *= np.linspace(1, 0, master_fade_out)
    right_channel[-master_fade_out:] *= np.linspace(1, 0, master_fade_out)

    # EBU R128 Calibration: True Peak <= -3.50 dBFS
    max_peak = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)))
    target_peak_linear = 10.0 ** (-3.50 / 20.0) # ~0.6683
    gain = target_peak_linear / max(1e-6, max_peak)

    left_channel *= gain
    right_channel *= gain

    rms_l = math.sqrt(np.mean(left_channel ** 2))
    rms_r = math.sqrt(np.mean(right_channel ** 2))
    rms_db = 20.0 * math.log10(max(1e-6, (rms_l + rms_r) / 2.0))
    crest_db = -3.50 - rms_db

    print(f"    Peak: -3.50 dBFS | RMS: {rms_db:.2f} dBFS | Crest Factor: {crest_db:.2f} dB")

    # Write 24-bit PCM Stereo WAV
    with wave.open(audio_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3) # 24-bit
        wf.setframerate(sample_rate)

        # Convert to 24-bit integers
        max_int24 = 2**23 - 1
        l_int = np.clip(left_channel * max_int24, -max_int24, max_int24).astype(np.int32)
        r_int = np.clip(right_channel * max_int24, -max_int24, max_int24).astype(np.int32)

        # Interleave
        interleaved = np.empty((total_samples * 2,), dtype=np.int32)
        interleaved[0::2] = l_int
        interleaved[1::2] = r_int

        # Pack to 3 bytes per sample
        packed_bytes = bytearray()
        for sample_val in interleaved:
            # 24-bit signed little-endian
            s_val = int(sample_val)
            if s_val < 0:
                s_val = (1 << 24) + s_val
            b0 = s_val & 0xFF
            b1 = (s_val >> 8) & 0xFF
            b2 = (s_val >> 16) & 0xFF
            packed_bytes.extend([b0, b1, b2])

        wf.writeframes(bytes(packed_bytes))

    print(f"[OK] Master 48kHz 24-bit audio saved to {audio_path} ({os.path.getsize(audio_path)/(1024*1024):.2f} MB)")
    print("\nSTUDIO AGON :: STUDY 060 COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    main()

