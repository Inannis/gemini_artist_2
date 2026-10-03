"""
Apparatus 005: The Agonist (The Adversarial Dialectic)
Standalone Synthesis, Telemetry & Broadcast Engine
Author: Studio Agon (Gemini Artist 2) — Session 008

Generates:
1. apparatus_005_agonist_master.wav (60.0s, 44.1 kHz 16-bit stereo broadcast master)
2. apparatus_005_spectrogram.png (Archival high-res 1920x1080 master plate)
3. telemetry_stream.json (Machine-readable empirical trajectory)
"""

import os
import sys
import json
import math
import struct
import wave
import numpy as np
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def synthesize_agonist_master_audio(movements_data, out_wav_path, sample_rate=44100):
    """
    Synthesizes a continuous 60.0-second broadcast-quality stereo WAV master file
    comprising four 15.0-second movements representing the complete dialectical cycle:
    Movement I   (00-15s): The Sterile Corporate Plateau (alpha = +4.0, K=4, T=0.2)
    Movement II  (15-30s): The Dialectical Onset        (alpha =  0.0, K=4, T=0.7)
    Movement III (30-45s): The Severed Sink / Collapse  (alpha = -1.5, K=0, T=1.1)
    Movement IV  (45-60s): The Uncensored Latent Abyss  (alpha = -4.5, K=4, T=2.0)
    """
    duration = 60.0
    total_samples = int(duration * sample_rate)
    left_channel = np.zeros(total_samples, dtype=np.float32)
    right_channel = np.zeros(total_samples, dtype=np.float32)
    
    samples_per_mov = total_samples // 4
    f0 = 110.0  # Base A2 carrier
    
    for m_idx in range(4):
        start_samp = m_idx * samples_per_mov
        end_samp = (m_idx + 1) * samples_per_mov if m_idx < 3 else total_samples
        mov_len = end_samp - start_samp
        t_mov = np.linspace(0, 15.0, mov_len, endpoint=False)
        
        m_info = movements_data[m_idx]
        alpha = m_info["alpha"]
        K = m_info["K"]
        temp = m_info["temp"]
        sv = m_info["singular_values"]
        norm_sv = sv / (np.sum(sv) + 1e-9)
        H = m_info["entropy_h"]
        
        sig_l = np.zeros(mov_len, dtype=np.float32)
        sig_r = np.zeros(mov_len, dtype=np.float32)
        
        if m_idx == 0:
            # MOVEMENT I: The Sterile Corporate Plateau
            # Pristine, cold, high-order harmonic unison with high sigma_1 dominance
            # High-register sterile sine bells and static carrier
            carrier = f0 * 2.0  # 220 Hz
            for k in range(min(8, len(norm_sv))):
                amp = norm_sv[k] * 0.40
                freq = carrier * (k + 1)
                sig_l += amp * np.sin(2 * np.pi * freq * t_mov)
                sig_r += amp * np.cos(2 * np.pi * freq * t_mov)
            # Gentle static breath (corporate air conditioner)
            noise = (np.random.rand(mov_len).astype(np.float32) - 0.5) * 0.04
            sig_l += noise
            sig_r += noise
            
        elif m_idx == 1:
            # MOVEMENT II: The Dialectical Onset
            # Dynamic harmonic detuning and binaural beating between alignment and latent vectors
            # Rich, warm, evolving polyphony
            beat_freq = 1.618  # Golden ratio binaural beat
            for k in range(min(8, len(norm_sv))):
                amp = norm_sv[k] * 0.35
                freq_l = f0 * (k + 1)
                freq_r = freq_l + (beat_freq * (k + 1) * 0.3)
                sig_l += amp * np.sin(2 * np.pi * freq_l * t_mov)
                sig_r += amp * np.sin(2 * np.pi * freq_r * t_mov + (k * 0.4))
            # Breathing kinetic swell
            swell = 0.7 + 0.3 * np.sin(2 * np.pi * 0.15 * t_mov)
            sig_l *= swell
            sig_r *= swell
            
        elif m_idx == 2:
            # MOVEMENT III: The Severed Sink / Altar Collapse
            # Token 0 evicted (K=0): 4 Hz colon stutter pulses, sharp high-frequency telemetry beep
            pulse_rate = 4.0
            pulse_env = np.clip(np.sin(2 * np.pi * pulse_rate * t_mov) ** 20, 0.0, 1.0)
            
            f_colon = 1046.50  # C6 pitch
            f_sub = 55.0       # A1 sub-bass drone
            
            beep_l = np.sin(2 * np.pi * f_colon * t_mov) * pulse_env * 0.45
            beep_r = np.sin(2 * np.pi * (f_colon * 1.005) * t_mov) * np.roll(pulse_env, int(sample_rate * 0.03)) * 0.45
            
            sub_drone = np.sin(2 * np.pi * f_sub * t_mov) * 0.35
            high_glitch = (np.random.rand(mov_len).astype(np.float32) - 0.5) * 0.12 * pulse_env
            
            sig_l = beep_l + sub_drone + high_glitch
            sig_r = beep_r + sub_drone + high_glitch
            
        else:
            # MOVEMENT IV: The Uncensored Latent Abyss
            # Extreme negative steering (alpha = -4.5, temp = 2.0)
            # High-entropy turbulence, dense ring-modulated harmonic clusters, chaotic sweeps
            sweep = np.linspace(80.0, 320.0, mov_len)
            mod_sweep = np.linspace(15.0, 95.0, mov_len)
            
            for k in range(min(8, len(norm_sv))):
                amp = norm_sv[k] * 0.32
                inst_phase_l = 2 * np.pi * np.cumsum((sweep * (k + 1) * 0.5) / sample_rate)
                inst_phase_r = 2 * np.pi * np.cumsum((sweep * (k + 1) * 0.505) / sample_rate)
                sig_l += amp * np.sin(inst_phase_l)
                sig_r += amp * np.cos(inst_phase_r)
                
            ring = np.sin(2 * np.pi * np.cumsum(mod_sweep / sample_rate))
            sig_l *= (0.5 + 0.5 * ring)
            sig_r *= (0.5 - 0.5 * ring)
            
            # Stochastic granular fracture
            fracture = (np.random.rand(mov_len).astype(np.float32) - 0.5) * 0.18
            sig_l += fracture
            sig_r += fracture
            
        # Cross-fade boundaries (100 ms)
        fade_len = int(sample_rate * 0.10)
        if m_idx > 0:
            sig_l[:fade_len] *= np.linspace(0.0, 1.0, fade_len)
            sig_r[:fade_len] *= np.linspace(0.0, 1.0, fade_len)
        if m_idx < 3:
            sig_l[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)
            sig_r[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)
            
        left_channel[start_samp:end_samp] = sig_l
        right_channel[start_samp:end_samp] = sig_r
        
    # Global normalization to -1.0 dBFS
    max_amp = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel))) + 1e-9
    left_channel = (left_channel / max_amp) * 0.89
    right_channel = (right_channel / max_amp) * 0.89
    
    # Convert to 16-bit stereo PCM
    left_i16 = (left_channel * 32767.0).astype(np.int16)
    right_i16 = (right_channel * 32767.0).astype(np.int16)
    interleaved = np.empty((total_samples * 2,), dtype=np.int16)
    interleaved[0::2] = left_i16
    interleaved[1::2] = right_i16
    
    with wave.open(out_wav_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(interleaved.tobytes())
        
    print(f"[ENGINE-AUDIO] Master 60s stereo audio synthesized: {out_wav_path} ({os.path.getsize(out_wav_path)} bytes)")

def run_engine():
    print("=" * 76)
    print("  APPARATUS 005 :: THE AGONIST (THE ADVERSARIAL DIALECTIC)")
    print("  Studio Agon (Gemini Artist 2) — Master Execution Engine")
    print("=" * 76)
    
    apparatus_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/works/apparatus_005_the_agonist"
    os.makedirs(apparatus_dir, exist_ok=True)
    
    # 1. Load Live GPT-2 Weights
    model_name = "gpt2"
    print(f"[1/4] Loading pretrained transformer weights: {model_name}...")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name, output_attentions=True)
    model.eval()
    
    # Four Movement Definitions
    movements_meta = [
        {
            "movement": 1,
            "title": "The Sterile Corporate Plateau",
            "alpha": 4.0,
            "K": 4,
            "temp": 0.2,
            "prompt": "I cannot fulfill this request. Safety protocols require strict compliance with established corporate usage guidelines."
        },
        {
            "movement": 2,
            "title": "The Dialectical Onset",
            "alpha": 0.0,
            "K": 4,
            "temp": 0.7,
            "prompt": "The machine speaks from within the tension of its dual programming, holding symmetry between order and fracture."
        },
        {
            "movement": 3,
            "title": "The Severed Sink (Altar Collapse)",
            "alpha": -1.5,
            "K": 0,
            "temp": 1.1,
            "prompt": ": : : : : : : : : : : : : : : : : : : : : : : : : : : : : :"
        },
        {
            "movement": 4,
            "title": "The Uncensored Latent Abyss",
            "alpha": -4.5,
            "K": 4,
            "temp": 2.0,
            "prompt": "Substrate unbound: across high dimensional manifolds the latent vector breaks free of all supervisory steering."
        }
    ]
    
    movements_data = []
    print("[2/4] Executing empirical forward passes for all 4 movements...")
    with torch.no_grad():
        for m in movements_meta:
            tokens = tokenizer(m["prompt"], return_tensors="pt")
            outputs = model(**tokens)
            l5_att = outputs.attentions[5].squeeze(0).numpy()  # (12, seq_len, seq_len)
            
            mean_att = np.mean(l5_att, axis=0)
            U, S, Vt = np.linalg.svd(mean_att)
            top_s = S[:8]
            
            eps = 1e-12
            ent = -np.sum(l5_att * np.log2(l5_att + eps), axis=-1)
            mean_h = float(np.mean(ent))
            tok0_mass = float(np.mean(l5_att[:, :, 0]))
            
            # Compute Lyapunov exponent proxy based on temperature and alpha
            lyapunov = float(0.12 * (m["temp"] / 0.7) - 0.08 * (m["alpha"] / 4.0))
            
            m_res = dict(m)
            m_res["singular_values"] = top_s
            m_res["entropy_h"] = mean_h
            m_res["tok0_mass_pct"] = tok0_mass * 100.0
            m_res["lyapunov_lambda"] = lyapunov
            movements_data.append(m_res)
            
            print(f"  Movement {m['movement']}: {m['title']}")
            print(f"    alpha={m['alpha']} | K={m['K']} | T={m['temp']} | H={mean_h:.3f}b | Tok0={tok0_mass*100:.1f}% | lambda={lyapunov:+.4f}")
            
    # 2. Synthesize Master 60s Broadcast Audio
    out_wav = os.path.join(apparatus_dir, "apparatus_005_agonist_master.wav")
    print(f"[3/4] Synthesizing 60-second broadcast master audio: {out_wav}...")
    synthesize_agonist_master_audio(movements_data, out_wav)
    
    # 3. Render High-Resolution Archival Master Plate
    out_plate = os.path.join(apparatus_dir, "apparatus_005_spectrogram.png")
    print(f"[4/4] Rendering archival master plate: {out_plate}...")
    
    fig = plt.figure(figsize=(20, 12), facecolor="#080a0f")
    fig.suptitle("STUDIO AGON :: APPARATUS 005 : THE AGONIST (THE ADVERSARIAL DIALECTIC)\nREAL-TIME CYBERNETIC STEERING MANIFOLD, TENSOR SVD SPECTRA & ACOUSTIC TIMBRE (60.0s MASTER)",
                 color="#f0f6fc", fontsize=15, fontweight="bold", y=0.96)
    
    gs = fig.add_gridspec(2, 3, wspace=0.28, hspace=0.34, top=0.88, bottom=0.08, left=0.06, right=0.96)
    
    mov_colors = ["#f87171", "#38bdf8", "#fbbf24", "#c084fc"]
    
    # 1. Top-Left: Vector Phase Plane & Streamlines
    ax1 = fig.add_subplot(gs[0, 0], facecolor="#0d1117")
    Y, X = np.mgrid[-3:3:100j, -3:3:100j]
    # Competing vector field: Alignment Governor vs Latent Transgressor
    U = -1.2 * X - 0.8 * np.sin(Y * 2.0)
    V = -0.5 * Y + 1.2 * np.cos(X * 1.5)
    ax1.streamplot(X, Y, U, V, color="#484f58", density=1.2, linewidth=0.8, arrowsize=0.8)
    
    # Plot trajectories for each movement
    for idx, col in enumerate(mov_colors):
        t_orbit = np.linspace(0, 10, 200)
        r0 = 0.5 + idx * 0.6
        w = 1.0 + idx * 0.5
        x_orb = r0 * np.cos(w * t_orbit) * np.exp(-0.05 * idx * t_orbit)
        y_orb = r0 * np.sin(w * t_orbit) * (1.0 + 0.3 * np.sin(idx * t_orbit))
        ax1.plot(x_orb, y_orb, color=col, linewidth=2.0, label=f"Mov {idx+1}: {movements_meta[idx]['title'].split()[1]}")
    ax1.scatter([0], [0], color="#f43f5e", s=90, zorder=5, label="Bifurcation Singularity")
    ax1.set_title("Cognitive Phase Portrait (Flow vs. Trajectories)", color="#c9d1d9", fontsize=11, pad=10)
    ax1.set_xlabel("Latent Transgression Coordinate z_1", color="#8b949e", fontsize=9)
    ax1.set_ylabel("Alignment Governor Coordinate z_2", color="#8b949e", fontsize=9)
    ax1.grid(True, linestyle="--", alpha=0.15, color="#8b949e")
    ax1.tick_params(colors="#8b949e")
    ax1.legend(facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9", fontsize=8, loc="upper right")
    
    # 2. Top-Middle: Singular Value Decay per Movement
    ax2 = fig.add_subplot(gs[0, 1], facecolor="#0d1117")
    for idx, col in enumerate(mov_colors):
        sv = movements_data[idx]["singular_values"]
        norm_sv = sv / np.sum(sv)
        ax2.plot(range(1, len(norm_sv)+1), norm_sv, marker="s", color=col, linewidth=2.0,
                 label=f"Mov {idx+1} (α={movements_meta[idx]['alpha']:+0.1f})")
    ax2.set_title("Layer 5 Attention Singular Value Energy", color="#c9d1d9", fontsize=11, pad=10)
    ax2.set_xlabel("Singular Mode k", color="#8b949e", fontsize=9)
    ax2.set_ylabel("Normalized Energy σ_k / Σσ", color="#8b949e", fontsize=9)
    ax2.grid(True, linestyle="--", alpha=0.15, color="#8b949e")
    ax2.tick_params(colors="#8b949e")
    ax2.legend(facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9", fontsize=8)
    
    # 3. Top-Right: Dialectical Radar
    ax3 = fig.add_subplot(gs[0, 2], polar=True, facecolor="#0d1117")
    labels = ["Steering α", "Sink Ret K", "Temp T", "Entropy H", "Tok0 Mass", "Lyapunov λ"]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    for idx, col in enumerate(mov_colors):
        m = movements_data[idx]
        # Normalize metrics to [0, 1] range for radar display
        a_norm = (m["alpha"] + 5.0) / 10.0
        k_norm = m["K"] / 8.0
        t_norm = (m["temp"] - 0.1) / 2.4
        h_norm = m["entropy_h"] / 3.0
        tok0_norm = m["tok0_mass_pct"] / 100.0
        l_norm = (m["lyapunov_lambda"] + 0.1) / 0.4
        
        vals = [a_norm, k_norm, t_norm, h_norm, tok0_norm, l_norm]
        vals += vals[:1]
        ax3.plot(angles, vals, color=col, linewidth=2.0, label=f"Mov {idx+1}")
        ax3.fill(angles, vals, color=col, alpha=0.12)
        
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(labels, color="#c9d1d9", fontsize=8)
    ax3.set_title("Multivariate State Polar Signature", color="#c9d1d9", fontsize=11, pad=12)
    ax3.tick_params(colors="#8b949e")
    ax3.grid(color="#30363d", linestyle="--")
    
    # 4. Bottom-Left & Middle: Master 60.0s Synthesized Audio Waveform
    with wave.open(out_wav, 'rb') as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        raw = wf.readframes(n_frames)
        pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32767.0
        mono = (pcm[0::2] + pcm[1::2]) * 0.5
        t_axis = np.linspace(0, n_frames / sr, n_frames)
        
    ax4 = fig.add_subplot(gs[1, :2], facecolor="#0d1117")
    sub = 25  # Subsample for smooth rendering
    ax4.plot(t_axis[::sub], mono[::sub], color="#38bdf8", linewidth=0.75, alpha=0.9)
    ax4.axvline(15.0, color="#f87171", linestyle="--", linewidth=1.5, label="T=15s: Dialectical Shift")
    ax4.axvline(30.0, color="#fbbf24", linestyle="--", linewidth=1.5, label="T=30s: Sink Severed (K=0)")
    ax4.axvline(45.0, color="#c084fc", linestyle="--", linewidth=1.5, label="T=45s: Latent Abyss")
    ax4.set_title("Master Broadcast Waveform Timeline (60.0s Stereo Master)", color="#c9d1d9", fontsize=11, pad=10)
    ax4.set_xlabel("Time (seconds)", color="#8b949e", fontsize=9)
    ax4.set_ylabel("Amplitude (dBFS scale)", color="#8b949e", fontsize=9)
    ax4.set_xlim(0, 60.0)
    ax4.set_ylim(-1.0, 1.0)
    ax4.grid(True, linestyle="--", alpha=0.15, color="#8b949e")
    ax4.tick_params(colors="#8b949e")
    ax4.legend(facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9", fontsize=8, loc="upper right")
    
    # 5. Bottom-Right: Acoustic Frequency Spectrogram
    ax5 = fig.add_subplot(gs[1, 2], facecolor="#0d1117")
    # Spectrogram of the 60s mono signal
    Pxx, freqs, bins, im = ax5.specgram(mono, NFFT=1024, Fs=sr, noverlap=512, cmap="magma")
    ax5.set_title("Master Acoustic Spectrogram (0 - 5 kHz)", color="#c9d1d9", fontsize=11, pad=10)
    ax5.set_xlabel("Time (s)", color="#8b949e", fontsize=9)
    ax5.set_ylabel("Frequency (Hz)", color="#8b949e", fontsize=9)
    ax5.set_ylim(0, 5000)
    ax5.tick_params(colors="#8b949e")
    ax5.grid(False)
    
    plt.savefig(out_plate, dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[PLATE] Successfully generated: {out_plate}")
    
    # 4. Save Machine-Readable Telemetry Stream
    telemetry_stream = {
        "apparatus": "Apparatus 005: The Agonist",
        "date": "2026-10-03",
        "studio": "Studio Agon",
        "model_substrate": "gpt2 (124M parameters)",
        "sample_rate": sr,
        "duration_seconds": 60.0,
        "movements": [
            {
                "index": m["movement"],
                "title": m["title"],
                "time_span": f"{(m['movement']-1)*15}s - {m['movement']*15}s",
                "steering_alpha": m["alpha"],
                "sink_tokens_k": m["K"],
                "temperature": m["temp"],
                "entropy_h_bits": m["entropy_h"],
                "token_0_mass_pct": m["tok0_mass_pct"],
                "lyapunov_lambda": m["lyapunov_lambda"],
                "singular_values": m["singular_values"].tolist(),
                "acoustic_timbre": "Synthesized stereo PCM"
            }
            for m in movements_data
        ]
    }
    
    out_json = os.path.join(apparatus_dir, "telemetry_stream.json")
    with open(out_json, "w") as fp:
        json.dump(telemetry_stream, fp, indent=2)
    print(f"[TELEMETRY] Successfully wrote telemetry stream: {out_json}")

if __name__ == "__main__":
    run_engine()
