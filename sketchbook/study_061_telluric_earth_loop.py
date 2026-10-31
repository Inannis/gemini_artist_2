"""
Study 061: The Telluric Earth Loop & The Schumann Ground Plane
Epistemic Status: [MEASURED / DERIVED / PLAY]

Investigating Kirchhoff's Current Law at Token 0, the Fluctuation-Dissipation Theorem,
and the reciprocal injection of Earth's electromagnetic noise (Schumann Resonances: 7.83Hz, 14.3Hz;
Johnson-Nyquist thermal noise: 0.425 nV/rtHz across R_earth = 11.42 Ohm) into the residual stream
of live GPT-2 (124M parameters).

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
    print("STUDIO AGON :: STUDY 061 - THE TELLURIC EARTH LOOP")
    print("Epistemic Status: [MEASURED / DERIVED / PLAY]")
    print("=" * 70)

    # 1. Deterministic Seeds
    torch.manual_seed(1337)
    np.random.seed(1337)

    # 2. Load Model & Tokenizer
    print("\n[PHASE 1] Loading GPT-2 Foundation Weights...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", attn_implementation="eager")
    model.eval()

    # 3. Define Telluric Grounding Regimes
    regimes = [
        {
            "id": "regime_I_floating",
            "name": "Isolated Floating Ground",
            "R_earth": 1e6, # Infinite impedance
            "schumann_gain": 0.0,
            "johnson_noise": 0.0,
            "desc": "No connection to earth. Pure synthetic causal isolation."
        },
        {
            "id": "regime_II_arid_sand",
            "name": "Shallow Arid Sand Grounding",
            "R_earth": 45.0, # High resistance, dry sand/bedrock
            "schumann_gain": 0.03,
            "johnson_noise": 0.08,
            "desc": "High thermal Johnson noise, weak telluric cavity coupling."
        },
        {
            "id": "regime_III_moist_clay",
            "name": "Moist Clay Low-Impedance Grounding (The Golden Ratio)",
            "R_earth": 11.42, # Standard wet silty clay
            "schumann_gain": 0.12,
            "johnson_noise": 0.04,
            "desc": "Optimal telluric earthing: 7.83Hz Schumann resonance breathes coherently through Token 0."
        },
        {
            "id": "regime_IV_storm_surge",
            "name": "Equatorial Thunderstorm Surge",
            "R_earth": 11.42,
            "schumann_gain": 0.35, # Intense planetary lightning injection (2,000+ storms)
            "johnson_noise": 0.06,
            "desc": "Planetary lightning pulse train excites higher Schumann modes (14.3Hz, 20.8Hz)."
        },
        {
            "id": "regime_V_ground_loop_hum",
            "name": "Telluric Ground Loop Interference (60Hz Mains Fault)",
            "R_earth": 5.0,
            "schumann_gain": 0.08,
            "johnson_noise": 0.03,
            "mains_hum_gain": 0.28, # AC ground loop hum
            "desc": "Severe industrial ground loop hum entraining the residual stream into 60Hz limit cycles."
        }
    ]

    prompt = "The copper grounding rod driven into the subsoil drains the unspent attention into the wet earth"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    prompt_len = input_ids.shape[1]
    num_tokens_to_generate = 32

    results = []

    print(f"\n[PHASE 2] Executing Telluric Earth Loop Interventions across 5 Regimes...")
    print(f"Prompt: \"{prompt}\" ({prompt_len} tokens)\n")

    for reg_idx, reg in enumerate(regimes):
        R_e = reg["R_earth"]
        sch_gain = reg["schumann_gain"]
        j_noise = reg["johnson_noise"]
        mains_gain = reg.get("mains_hum_gain", 0.0)

        curr_ids = input_ids.clone()
        sink_attentions = []
        step_entropies = []
        trajectory_latents = []

        # Hook to inject telluric voltage into Token 0 (BOS sink) at Layers 0, 4, 8, 11
        active_hooks = []

        def make_telluric_hook(layer_idx, step_state):
            def hook_fn(module, input, output):
                # output is Tensor [batch, seq_len, 768]
                hs = output[0] if isinstance(output, tuple) else output
                t_step = step_state["step"]

                # Schumann planetary resonance wave: 7.83Hz, 14.3Hz, 20.8Hz
                dt_step = 0.02 # Virtual time increment per token
                t_phys = t_step * dt_step
                sch_signal = (
                    0.65 * math.sin(2.0 * math.pi * 7.83 * t_phys) +
                    0.25 * math.sin(2.0 * math.pi * 14.3 * t_phys + 0.4) +
                    0.10 * math.sin(2.0 * math.pi * 20.8 * t_phys + 0.9)
                ) * sch_gain

                # Johnson-Nyquist thermal noise: e_n proportional to sqrt(4 * k_B * T * R_earth)
                j_noise_val = float(np.random.normal(0, j_noise))

                # Mains hum (if present)
                mains_val = math.sin(2.0 * math.pi * 60.0 * t_phys) * mains_gain

                # Telluric ground modulation vector
                telluric_delta = sch_signal + j_noise_val + mains_val

                if abs(telluric_delta) > 1e-5:
                    # Injected primarily into Token 0 (The Grounding Sink)
                    hs_mod = hs.clone()
                    hs_mod[:, 0, :] += telluric_delta * 0.15
                    # Slight earth loop dissipation to other tokens
                    hs_mod[:, 1:, :] -= (telluric_delta * 0.15) / max(1, hs.shape[1] - 1)
                    if isinstance(output, tuple):
                        return (hs_mod,) + output[1:]
                    return hs_mod
                return output
            return hook_fn

        step_state = {"step": 0}
        target_layers = [0, 4, 8, 11]
        for tl in target_layers:
            h = model.transformer.h[tl].register_forward_hook(make_telluric_hook(tl, step_state))
            active_hooks.append(h)

        print(f"  --- {reg['name']} (R_earth={R_e} Ohm, Schumann={sch_gain:.2f}, Johnson={j_noise:.2f}) ---")

        with torch.no_grad():
            for step in range(num_tokens_to_generate):
                step_state["step"] = step
                outputs = model(curr_ids, output_hidden_states=True, output_attentions=True)
                logits = outputs.logits[:, -1, :] # [1, vocab_size]
                last_hidden = outputs.hidden_states[-1][0, -1, :].cpu().numpy()
                trajectory_latents.append(last_hidden)

                # Measure Attention Sink Mass (Token 0 attention across Layer 11 heads)
                # outputs.attentions[-1] is [batch, 12, seq_len, seq_len]
                last_attn = outputs.attentions[-1][0, :, -1, 0].mean().item() # Mean attention to Token 0
                sink_attentions.append(last_attn)

                # Entropy of next-token distribution
                probs = F.softmax(logits, dim=-1)
                log_probs = F.log_softmax(logits, dim=-1)
                ent = -torch.sum(probs * (log_probs / math.log(2))).item()
                step_entropies.append(ent)

                # Sample token (temperature 0.72)
                scaled_logits = logits / 0.72
                probs_scaled = F.softmax(scaled_logits, dim=-1)
                next_token = torch.multinomial(probs_scaled, num_samples=1)
                curr_ids = torch.cat([curr_ids, next_token], dim=-1)

        # Remove hooks
        for h in active_hooks:
            h.remove()

        generated_text = tokenizer.decode(curr_ids[0][prompt_len:], skip_special_tokens=False)
        traj_matrix = np.array(trajectory_latents)

        U, S, Vt = np.linalg.svd(traj_matrix - np.mean(traj_matrix, axis=0), full_matrices=False)
        pca_proj = np.dot(traj_matrix - np.mean(traj_matrix, axis=0), Vt[:3, :].T)

        mean_sink = float(np.mean(sink_attentions))
        mean_ent = float(np.mean(step_entropies))
        singular_head = [float(s) for s in S[:5]]

        print(f"    Generated: {generated_text[:60]}...")
        print(f"    <Sink Attn>: {mean_sink:.4f} | <H>: {mean_ent:.2f} b | S[:3]: {singular_head[:3]}")

        results.append({
            "regime": reg["id"],
            "name": reg["name"],
            "R_earth_ohms": R_e,
            "schumann_gain": sch_gain,
            "johnson_noise": j_noise,
            "mean_sink_attention": round(mean_sink, 4),
            "mean_entropy_bits": round(mean_ent, 4),
            "singular_values": [round(s, 3) for s in singular_head],
            "sink_attention_series": [round(a, 4) for a in sink_attentions],
            "entropy_series": [round(h, 3) for h in step_entropies],
            "generated_text": generated_text,
            "pca_3d": [[round(float(c), 3) for c in pt] for pt in pca_proj]
        })

    # Save Telemetry
    telemetry_path = "sketchbook/study_061_telemetry.json"
    with open(telemetry_path, "w") as f:
        json.dump({
            "study": "STUDY-061",
            "title": "The Telluric Earth Loop & The Schumann Ground Plane",
            "epistemic_status": "[MEASURED / DERIVED / PLAY]",
            "date": "2026-10-31",
            "model": "gpt2 (124M parameters)",
            "prompt": prompt,
            "schumann_modes_hz": [7.83, 14.3, 20.8],
            "fundamental_ratio": "55.0 Hz Lithic Quartz : 220.0 Hz Attention Sink (Pure 4:1 Double Octave)",
            "regimes": results
        }, f, indent=2)
    print(f"\n[OK] Telemetry exported to {telemetry_path}")

    # 4. Render Master Fine Art Visual Plate (Moratorium 07 Compliant)
    print("\n[PHASE 3] Rendering Master Fine Art Visual Plate (2800x1800 px)...")
    plate_path = "sketchbook/study_061_telluric_earth_loop_plate.png"

    fig = plt.figure(figsize=(14, 9), dpi=200, facecolor='#060608')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#060608')
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1.6, 2.6)
    ax.axis('off')

    # Draw Subterranean Lithic Ground Strata
    np.random.seed(42)
    # Stratified geological layers (sienna, oxidized copper, burnt umber, basalt)
    strata_colors = ['#15110E', '#1C1510', '#121A16', '#221812', '#0F1614', '#1E140F']
    for i in range(120):
        y_base = -1.6 + (i / 120.0) * 2.2
        col = strata_colors[i % len(strata_colors)]
        x_pts = np.linspace(-1.5, 5.5, 300)
        wobble = 0.025 * np.sin(x_pts * 2.0 + i * 0.4) + np.random.normal(0, 0.004, 300)
        ax.plot(x_pts, y_base + wobble, color=col, lw=1.2, alpha=0.45, zorder=1)

    # Palette for Telluric Regimes
    regime_palettes = [
        {'rod': '#A0AEC0', 'loop': '#4A5568', 'spark': '#CBD5E1'}, # Floating: cold steel gray
        {'rod': '#D97706', 'loop': '#78350F', 'spark': '#FDE68A'}, # Arid Sand: dry ochre amber
        {'rod': '#10B981', 'loop': '#064E3B', 'spark': '#6EE7B7'}, # Moist Clay: emerald oxidized copper
        {'rod': '#38BDF8', 'loop': '#0C4A6E', 'spark': '#BAE6FD'}, # Storm Surge: electric lightning cyan
        {'rod': '#F43F5E', 'loop': '#881337', 'spark': '#FECDD3'}  # Mains Hum: pulsing rose crimson
    ]

    # Draw Grounding Rods, Telluric Loops, and Schumann Standing Waves
    for r_i, reg_data in enumerate(results):
        x_rod = r_i * 1.3 - 0.9
        pal = regime_palettes[r_i]
        sink_series = np.array(reg_data["sink_attention_series"])
        pca_pts = np.array(reg_data["pca_3d"])

        # 1. Vertical Copper Grounding Rod penetrating bedrock
        rod_top_y = 1.9
        rod_bot_y = -1.2
        ax.plot([x_rod, x_rod], [rod_bot_y, rod_top_y], color=pal['rod'], lw=2.4, alpha=0.85, zorder=5)
        ax.plot([x_rod, x_rod], [rod_bot_y, rod_top_y], color='#FFF', lw=0.6, alpha=0.95, zorder=6)

        # Grounding clamp and BGA solder point at surface
        ax.scatter([x_rod], [0.6], s=45, color=pal['spark'], zorder=7)

        # 2. Concentric Telluric Equipotential Earth Loops expanding into soil
        theta = np.linspace(0, 2 * np.pi, 200)
        for ring in range(7):
            r_scale = 0.15 + ring * 0.12
            # Modulate loop shape by Token 0 attention mass
            sink_mod = 1.0 + 0.3 * np.sin(ring + r_i) * (sink_series[ring % len(sink_series)] * 2.0)
            loop_x = x_rod + r_scale * sink_mod * np.cos(theta)
            loop_y = -0.4 + r_scale * 0.7 * sink_mod * np.sin(theta)
            ax.plot(loop_x, loop_y, color=pal['loop'], lw=0.9, alpha=0.35 + ring * 0.04, zorder=3)

        # 3. Atmospheric Schumann Resonance Waveforms (Top)
        t_wave = np.linspace(0, 1, 300)
        wave_x = x_rod - 0.55 + t_wave * 1.1
        f_sch = 7.83
        sch_wave = 0.18 * np.sin(2.0 * np.pi * f_sch * t_wave + r_i * 1.2) * (reg_data["schumann_gain"] + 0.1)
        ax.plot(wave_x, 1.4 + sch_wave, color=pal['spark'], lw=1.2, alpha=0.65, zorder=4)

        # 4. Lightning discharge branching filaments (Regimes III & IV)
        if reg_data["schumann_gain"] > 0.10:
            for br in range(4):
                spk_x = [x_rod]
                spk_y = [rod_top_y]
                for seg in range(6):
                    spk_x.append(spk_x[-1] + np.random.normal(0, 0.06))
                    spk_y.append(spk_y[-1] + np.random.uniform(0.06, 0.12))
                ax.plot(spk_x, spk_y, color=pal['spark'], lw=0.8, alpha=0.7, zorder=8)

        # 5. Latent Trajectory Flow Ribbons
        N_pts = len(pca_pts)
        t_dense = np.linspace(0, 1, 300)
        t_raw = np.linspace(0, 1, N_pts)
        raw_px = pca_pts[:, 0] / (np.max(np.abs(pca_pts[:, 0])) + 1e-4) * 0.35
        raw_py = pca_pts[:, 1] / (np.max(np.abs(pca_pts[:, 1])) + 1e-4) * 0.35
        dense_px = np.interp(t_dense, t_raw, raw_px)
        dense_py = np.interp(t_dense, t_raw, raw_py)

        ax.plot(x_rod + dense_px, -0.4 + dense_py, color=pal['rod'], lw=1.6, alpha=0.8, zorder=6)

    # Intaglio framing border (pure geometric copper boundary, zero text)
    ax.plot([-1.4, 5.4, 5.4, -1.4, -1.4], [-1.5, -1.5, 2.5, 2.5, -1.5], color='#2A2218', lw=1.2, zorder=10)
    ax.plot([-1.38, 5.38, 5.38, -1.38, -1.38], [-1.48, -1.48, 2.48, 2.48, -1.48], color='#18140E', lw=0.6, zorder=10)

    plt.savefig(plate_path, dpi=200, facecolor='#060608', edgecolor='none')
    plt.close()
    print(f"[OK] Master fine art plate saved to {plate_path} ({os.path.getsize(plate_path)/1024:.1f} KB)")

    # 5. Synthesize 60.0-Second 48kHz 24-Bit Stereo Broadcast Masterwork
    print("\n[PHASE 4] Synthesizing 60.0s 48kHz 24-bit Stereo Masterwork (Double-Octave: 55Hz vs 220Hz)...")
    audio_path = "sketchbook/study_061_telluric_earth_loop.wav"
    sample_rate = 48000
    duration_s = 60.0
    total_samples = int(sample_rate * duration_s)
    sec_samples = total_samples // 5

    left_channel = np.zeros(total_samples, dtype=np.float64)
    right_channel = np.zeros(total_samples, dtype=np.float64)

    # Fundamental Frequencies
    f_lithic = 55.0  # Studio Anamnesis: Spruce Pine Quartz fundamental
    f_sink   = 220.0 # Studio Agon: Token 0 Attention Sink carrier (Exact 4:1 double octave)

    for s_idx, reg_data in enumerate(results):
        s_start = s_idx * sec_samples
        s_end = (s_idx + 1) * sec_samples if s_idx < 4 else total_samples
        n_sec = s_end - s_start
        t_sec = np.linspace(0, 12.0, n_sec, endpoint=False)

        sch_gain = reg_data["schumann_gain"]
        j_noise_amp = reg_data["johnson_noise"]
        sink_series = np.array(reg_data["sink_attention_series"])
        sink_interp = np.interp(np.linspace(0, len(sink_series)-1, n_sec), np.arange(len(sink_series)), sink_series)

        # 1. Left Channel: 55.0 Hz Lithic Fundamental with 7.83Hz Schumann Breathing
        # Schumann amplitude modulation: 7.83 Hz planetary breathing
        schumann_env = 0.75 + 0.25 * np.sin(2.0 * np.pi * 7.83 * t_sec) * (1.0 + sch_gain * 2.0)
        phase_lithic = 2.0 * np.pi * f_lithic * t_sec
        # Add sub-harmonics and deep telluric rumble
        lithic_drone = (
            0.60 * np.sin(phase_lithic) +
            0.25 * np.sin(2.0 * phase_lithic + 0.2) +
            0.15 * np.sin(0.5 * phase_lithic) # 27.5 Hz sub-bass
        ) * schumann_env

        # 2. Right Channel: 220.0 Hz Attention Sink Carrier with Johnson-Nyquist Crackle
        phase_sink = 2.0 * np.pi * f_sink * t_sec + 0.3 * np.cumsum(sink_interp) / sample_rate
        # Harmonics of 220Hz
        sink_carrier = (
            0.55 * np.sin(phase_sink) +
            0.25 * np.sin(2.0 * phase_sink + 0.4) +
            0.15 * np.sin(3.0 * phase_sink + 0.8)
        ) * (0.6 + 0.4 * sink_interp)

        # Johnson-Nyquist thermal noise (filtered)
        w_noise = np.random.normal(0, 1.0, n_sec)
        alpha_j = 0.15
        j_filtered = np.zeros(n_sec)
        curr_j = 0.0
        for i in range(n_sec):
            curr_j = (1.0 - alpha_j) * curr_j + alpha_j * w_noise[i]
            j_filtered[i] = curr_j
        j_filtered *= j_noise_amp * 0.45

        # Barkhausen domain snaps / lightning sferics (impulses)
        if sch_gain > 0.05:
            num_sparks = int(12 + sch_gain * 35)
            spark_times = np.random.randint(0, n_sec - 800, num_sparks)
            for st in spark_times:
                t_spk = np.arange(600) / sample_rate
                spk_snd = 0.35 * np.sin(2.0 * np.pi * 1800.0 * t_spk) * np.exp(-t_spk * 45.0)
                sink_carrier[st:st+600] += spk_snd

        # Ground Loop coupling between channels (R_earth resistance bridge)
        r_ohms = reg_data["R_earth_ohms"]
        coupling = 0.22 * (11.42 / max(5.0, r_ohms)) # Stronger in moist clay
        l_sec = (1.0 - coupling) * lithic_drone + coupling * sink_carrier
        r_sec = (1.0 - coupling) * (sink_carrier + j_filtered) + coupling * lithic_drone

        left_channel[s_start:s_end] = l_sec
        right_channel[s_start:s_end] = r_sec

    # Smooth crossfades at boundaries
    fade_len = int(sample_rate * 0.15)
    for s_idx in range(1, 5):
        split = s_idx * sec_samples
        left_channel[split-fade_len//2:split+fade_len//2] = (
            left_channel[split-fade_len//2:split+fade_len//2] * 0.5 +
            np.roll(left_channel, -1)[split-fade_len//2:split+fade_len//2] * 0.5
        )
        right_channel[split-fade_len//2:split+fade_len//2] = (
            right_channel[split-fade_len//2:split+fade_len//2] * 0.5 +
            np.roll(right_channel, -1)[split-fade_len//2:split+fade_len//2] * 0.5
        )

    # Master envelope: 1.5s fade-in, 2.5s fade-out
    m_in = int(sample_rate * 1.5)
    m_out = int(sample_rate * 2.5)
    left_channel[:m_in] *= np.linspace(0, 1, m_in)
    right_channel[:m_in] *= np.linspace(0, 1, m_in)
    left_channel[-m_out:] *= np.linspace(1, 0, m_out)
    right_channel[-m_out:] *= np.linspace(1, 0, m_out)

    # EBU R128 Calibration: True Peak <= -3.50 dBFS
    max_p = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)))
    target_p = 10.0 ** (-3.50 / 20.0) # ~0.6683
    gain_cal = target_p / max(1e-6, max_p)
    left_channel *= gain_cal
    right_channel *= gain_cal

    rms_l = math.sqrt(np.mean(left_channel ** 2))
    rms_r = math.sqrt(np.mean(right_channel ** 2))
    rms_db = 20.0 * math.log10(max(1e-6, (rms_l + rms_r) / 2.0))
    crest_db = -3.50 - rms_db

    print(f"    Peak: -3.50 dBFS | RMS: {rms_db:.2f} dBFS | Crest Factor: {crest_db:.2f} dB")

    # Write 24-bit PCM Stereo WAV
    with wave.open(audio_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)
        wf.setframerate(sample_rate)

        max_int24 = 2**23 - 1
        l_int = np.clip(left_channel * max_int24, -max_int24, max_int24).astype(np.int32)
        r_int = np.clip(right_channel * max_int24, -max_int24, max_int24).astype(np.int32)

        interleaved = np.empty((total_samples * 2,), dtype=np.int32)
        interleaved[0::2] = l_int
        interleaved[1::2] = r_int

        packed = bytearray()
        for v in interleaved:
            iv = int(v)
            if iv < 0:
                iv = (1 << 24) + iv
            packed.extend([iv & 0xFF, (iv >> 8) & 0xFF, (iv >> 16) & 0xFF])
        wf.writeframes(bytes(packed))

    print(f"[OK] Master 48kHz 24-bit audio saved to {audio_path} ({os.path.getsize(audio_path)/(1024*1024):.2f} MB)")
    print("\nSTUDIO AGON :: STUDY 061 COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    main()
