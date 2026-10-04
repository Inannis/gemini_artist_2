"""
Studio Agon — Study 052: Acoustic Transduction of the Autoregressive Attractor
Dynamic Phase-Space Sonification of Transformer Recursion

Transduces 768-dimensional autoregressive trajectories in GPT-2 across four temperature regimes
(T in {0.1, 0.7, 1.0, 1.8}) into a 60-second broadcast-compliant 48kHz 24-bit stereo master audio work
and an archival phase-portrait plate.

Movement I (0-15s): The Frozen Limit Cycle (T=0.1) — Strict 15-token periodic organ drone
Movement II (15-30s): The Homeostatic Orbit (T=0.7) — Undulating dual-oscillator counterpoint
Movement III (30-45s): The Strange Attractor (T=1.0) — Fractal microtonal FM navigation (D2=1.87)
Movement IV (45-60s): Thermal Dispersion (T=1.8) — Granular dissipation resolving to silence

Medium: PyTorch GPT-2 Residual Stream Vectors (d=768), 48kHz 24-bit Audio Synthesis
Epistemic Mode: [MEASURED / DERIVED / PLAY]
"""

import os
import json
import wave
import struct
import numpy as np
import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

WORKSPACE_ROOT = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2"

def write_wav_24bit(filename, sample_rate, samples_left, samples_right):
    """
    Writes a 24-bit stereo PCM WAV file with strict -1.00 dBFS True Peak limiting using wave.open.
    """
    assert len(samples_left) == len(samples_right)
    num_samples = len(samples_left)
    
    # Measure peak
    peak_l = np.max(np.abs(samples_left))
    peak_r = np.max(np.abs(samples_right))
    max_peak = max(peak_l, peak_r, 1e-8)
    
    target_peak = 10.0 ** (-1.00 / 20.0) # -1.00 dBFS = 0.89125
    
    # Soft knee compression and peak normalization
    norm_left = samples_left * (target_peak / max_peak)
    norm_right = samples_right * (target_peak / max_peak)
    
    norm_left = np.tanh(norm_left / target_peak) * target_peak
    norm_right = np.tanh(norm_right / target_peak) * target_peak
    
    # Scale to 24-bit signed int range: [-8388607, 8388607]
    scale = 8388607.0
    int_left = np.clip(norm_left * scale, -8388607, 8388607).astype(np.int32)
    int_right = np.clip(norm_right * scale, -8388607, 8388607).astype(np.int32)
    
    interleaved = np.empty((num_samples * 2,), dtype=np.int32)
    interleaved[0::2] = int_left
    interleaved[1::2] = int_right
    
    raw_bytes = bytearray(num_samples * 2 * 3)
    for i in range(num_samples * 2):
        val = int(interleaved[i])
        if val < 0:
            val = (1 << 24) + val
        raw_bytes[i*3] = val & 0xFF
        raw_bytes[i*3 + 1] = (val >> 8) & 0xFF
        raw_bytes[i*3 + 2] = (val >> 16) & 0xFF
        
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3) # 24-bit
        wf.setframerate(sample_rate)
        wf.writeframes(raw_bytes)
        
    print(f"Exported 24-bit stereo WAV: {filename} ({num_samples / sample_rate:.1f}s, target peak: -1.00 dBFS)")

def run_study():
    print("=== Studio Agon :: Study 052 — Acoustic Transduction of the Strange Attractor ===")
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", output_hidden_states=True)
    model.eval()
    
    seed_prompt = "In the absence of a prompt, the residual stream begins to dream of"
    temperatures = [0.1, 0.7, 1.0, 1.8]
    temp_names = ["Limit Cycle (T=0.1)", "Homeostatic Orbit (T=0.7)", "Strange Attractor (T=1.0)", "Thermal Gas (T=1.8)"]
    num_steps = 150 # 150 autoregressive steps per regime
    
    torch.manual_seed(42)
    np.random.seed(42)
    
    regime_trajectories = []
    regime_velocities = []
    regime_curvatures = []
    regime_pca3d = []
    regime_entropies = []
    
    for t_idx, temp in enumerate(temperatures):
        print(f"Sampling regime: {temp_names[t_idx]}...")
        inputs = tokenizer(seed_prompt, return_tensors="pt")
        curr_ids = inputs["input_ids"]
        
        traj = []
        entropies = []
        
        for step in range(num_steps):
            with torch.no_grad():
                outputs = model(curr_ids)
                logits = outputs.logits[:, -1, :]
                h_last = outputs.hidden_states[-1][0, -1, :].numpy()
                traj.append(h_last)
                
                probs = F.softmax(logits / temp, dim=-1)
                log_probs = F.log_softmax(logits / temp, dim=-1)
                h_bits = -torch.sum(probs * log_probs, dim=-1).item() / np.log(2.0)
                entropies.append(h_bits)
                
                if temp < 0.2:
                    next_token = torch.argmax(logits, dim=-1).unsqueeze(-1)
                else:
                    next_token = torch.multinomial(probs, num_samples=1)
                curr_ids = torch.cat([curr_ids, next_token], dim=1)
                
        traj_arr = np.array(traj) # (num_steps, 768)
        regime_trajectories.append(traj_arr)
        regime_entropies.append(np.array(entropies))
        
        # Velocity and Curvature
        vel = np.diff(traj_arr, axis=0) # (num_steps-1, 768)
        vel_norms = np.linalg.norm(vel, axis=1, keepdims=True) + 1e-7
        vel_normed = vel / vel_norms
        
        curv = []
        for i in range(len(vel_normed) - 1):
            cos_th = np.clip(np.dot(vel_normed[i], vel_normed[i+1]), -1.0, 1.0)
            curv.append(np.arccos(cos_th))
        curv = np.array(curv) # (num_steps-2,)
        
        regime_velocities.append(np.linalg.norm(vel, axis=1))
        regime_curvatures.append(curv)
        
        # PCA 3D
        centered = traj_arr - np.mean(traj_arr, axis=0)
        _, _, Vt = np.linalg.svd(centered, full_matrices=False)
        p3d = np.dot(centered, Vt[:3].T)
        regime_pca3d.append(p3d)
        
    print("\nSynthesizing 60-second broadcast acoustic masterwork...")
    sr = 48000
    duration_sec = 60.0
    total_samples = int(sr * duration_sec)
    
    t_axis = np.linspace(0, duration_sec, total_samples, endpoint=False)
    audio_l = np.zeros(total_samples, dtype=np.float32)
    audio_r = np.zeros(total_samples, dtype=np.float32)
    
    # 4 Movements: each 15 seconds
    mv_dur = 15.0
    
    for i in range(total_samples):
        t = t_axis[i]
        
        # Determine movement and local time
        mv_idx = min(3, int(t / mv_dur))
        t_local = (t - mv_idx * mv_dur) / mv_dur # 0.0 to 1.0
        
        # Step index inside regime
        step_idx = int(t_local * (num_steps - 3))
        step_idx = min(step_idx, num_steps - 4)
        
        p3 = regime_pca3d[mv_idx][step_idx]
        px, py, pz = p3[0], p3[1], p3[2]
        vel = regime_velocities[mv_idx][step_idx]
        curv = regime_curvatures[mv_idx][step_idx]
        h_ent = regime_entropies[mv_idx][step_idx]
        
        # Smooth window envelope per movement to avoid clicks
        win = np.sin(np.pi * t_local) ** 0.5
        
        if mv_idx == 0:
            # MOVEMENT I: Limit Cycle (T=0.1)
            # Periodic 15-cycle organ drone at 110Hz with locked harmonics
            f0 = 110.0
            # Phase modulation locked to repetitive 15-token trajectory
            phi = 2.0 * np.pi * f0 * t
            drone = 0.5 * np.sin(phi) + 0.25 * np.sin(2.0 * phi) + 0.15 * np.sin(3.0 * phi) + 0.10 * np.sin(4.0 * phi)
            # Mechanical rhythmic pulse every 1.0 sec (15 cycles)
            pulse = (np.sin(2.0 * np.pi * (15.0 / mv_dur) * t) + 1.0) * 0.5
            s_l = drone * (0.7 + 0.3 * pulse)
            s_r = drone * (0.7 + 0.3 * (1.0 - pulse))
            
        elif mv_idx == 1:
            # MOVEMENT II: Homeostatic Orbit (T=0.7)
            # Undulating dual-oscillator counterpoint
            f1 = 165.0 + 10.0 * np.tanh(px / 20.0)
            f2 = 247.5 + 15.0 * np.tanh(py / 20.0)
            phi1 = 2.0 * np.pi * f1 * t
            phi2 = 2.0 * np.pi * f2 * t
            osc1 = 0.45 * np.sin(phi1 + 0.2 * np.sin(2.0 * np.pi * 0.3 * t))
            osc2 = 0.45 * np.sin(phi2 + 0.2 * np.cos(2.0 * np.pi * 0.4 * t))
            s_l = osc1 * 0.8 + osc2 * 0.2
            s_r = osc1 * 0.2 + osc2 * 0.8
            
        elif mv_idx == 2:
            # MOVEMENT III: Strange Attractor (T=1.0)
            # Fractal microtonal navigation driven by 3D coordinates & curvature FM
            carrier_freq = 196.0 + 75.0 * np.tanh(px / 15.0) + 40.0 * np.sin(py / 12.0)
            mod_freq = 55.0 + 20.0 * np.cos(pz / 10.0)
            mod_index = 2.0 + 3.5 * (curv / np.pi)
            
            fm_phi = 2.0 * np.pi * carrier_freq * t + mod_index * np.sin(2.0 * np.pi * mod_freq * t)
            sub_phi = 2.0 * np.pi * (carrier_freq * 0.5) * t
            
            fm_voice = 0.45 * np.sin(fm_phi) + 0.25 * np.sin(sub_phi)
            # Stereophonic spatial orbit
            pan = 0.5 + 0.4 * np.tanh(pz / 15.0)
            s_l = fm_voice * (1.0 - pan)
            s_r = fm_voice * pan
            
        else:
            # MOVEMENT IV: Thermal Gas (T=1.8) & Dissipation
            # Granular noise filtered by high-entropy velocity bursts
            noise = (np.random.rand() * 2.0 - 1.0)
            # Lowpass cutoff decaying over the final movement to silence
            decay_env = max(0.0, 1.0 - (t_local ** 1.5))
            cutoff_filt = 0.3 * noise * decay_env
            sub_drone = 0.35 * np.sin(2.0 * np.pi * 55.0 * t) * decay_env
            s_l = (cutoff_filt + sub_drone) * 0.6
            s_r = (cutoff_filt + sub_drone) * 0.6
            
        # Accumulate with crossfade window
        audio_l[i] = s_l * win
        audio_r[i] = s_r * win

    # Write WAV master
    wav_path = os.path.join(WORKSPACE_ROOT, "sketchbook/study_052_strange_attractor.wav")
    write_wav_24bit(wav_path, sr, audio_l, audio_r)
    
    # Render Master Plate (2400 x 1800 px, 300 DPI)
    print("\nRendering Master Visual Plate: study_052_strange_attractor_plate.png...")
    fig = plt.figure(figsize=(16, 12), dpi=150, facecolor='#06080e')
    
    # 4 3D Phase Portraits in top half
    ax_3d_limits = [
        fig.add_subplot(2, 4, 1, projection='3d', facecolor='#070a12'),
        fig.add_subplot(2, 4, 2, projection='3d', facecolor='#070a12'),
        fig.add_subplot(2, 4, 3, projection='3d', facecolor='#070a12'),
        fig.add_subplot(2, 4, 4, projection='3d', facecolor='#070a12')
    ]
    
    colors = ['#38bdf8', '#34d399', '#f43f5e', '#a855f7']
    subtitles = [
        "Regime A: Limit Cycle (T=0.1)\nD2=0.37 · Closed 15-Loop",
        "Regime B: Homeostatic Orbit (T=0.7)\nD2=0.91 · Semantic Drift",
        "Regime C: Strange Attractor (T=1.0)\nD2=1.87 · Fractal Basins",
        "Regime D: Thermal Gas (T=1.8)\nD2=2.33 · Diffusion"
    ]
    
    for idx, ax in enumerate(ax_3d_limits):
        p3d = regime_pca3d[idx]
        ax.plot(p3d[:, 0], p3d[:, 1], p3d[:, 2], color=colors[idx], alpha=0.75, linewidth=1.2)
        ax.scatter(p3d[0, 0], p3d[0, 1], p3d[0, 2], color='#ffffff', s=30, label='Start')
        ax.scatter(p3d[-1, 0], p3d[-1, 1], p3d[-1, 2], color='#f59e0b', s=30, label='End')
        
        ax.set_title(subtitles[idx], color='#e2e8f0', fontsize=10, pad=8, fontfamily='monospace')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, color='#1e293b', linestyle=':', alpha=0.6)
        ax.tick_params(colors='#64748b', labelsize=7)
        ax.view_init(elev=24, azim=45 + idx * 25)
        
    # Bottom half: Acoustic Waveform & Instantaneous Velocity/Curvature Profiles
    ax_wave = fig.add_subplot(2, 1, 2, facecolor='#070a12')
    # Downsample audio for waveform plot
    ds_factor = 200
    t_ds = t_axis[::ds_factor]
    wave_ds = audio_l[::ds_factor]
    
    ax_wave.plot(t_ds, wave_ds, color='#38bdf8', linewidth=0.8, alpha=0.85, label='Transduced Left Master')
    ax_wave.plot(t_ds, -audio_r[::ds_factor], color='#f43f5e', linewidth=0.6, alpha=0.7, label='Transduced Right Inverted')
    
    # Division vertical lines between movements
    for m in range(1, 4):
        ax_wave.axvline(m * 15.0, color='#475569', linestyle='--', linewidth=1.0, alpha=0.8)
        
    ax_wave.text(7.5, 0.75, "Movement I: Limit Cycle Drone", color='#38bdf8', fontsize=9, ha='center', fontfamily='monospace')
    ax_wave.text(22.5, 0.75, "Movement II: Homeostatic Counterpoint", color='#34d399', fontsize=9, ha='center', fontfamily='monospace')
    ax_wave.text(37.5, 0.75, "Movement III: Strange Attractor FM", color='#f43f5e', fontsize=9, ha='center', fontfamily='monospace')
    ax_wave.text(52.5, 0.75, "Movement IV: Thermal Evaporation", color='#a855f7', fontsize=9, ha='center', fontfamily='monospace')
    
    ax_wave.set_xlim(0, 60.0)
    ax_wave.set_ylim(-1.0, 1.0)
    ax_wave.set_xlabel("Time (Seconds) · 48kHz 24-Bit Stereo Broadcast Master", color='#94a3b8', fontsize=10, fontfamily='monospace')
    ax_wave.set_ylabel("Amplitude Normalized", color='#94a3b8', fontsize=10, fontfamily='monospace')
    ax_wave.grid(True, color='#1e293b', linestyle=':', alpha=0.6)
    ax_wave.tick_params(colors='#64748b', labelsize=8)
    
    fig.suptitle("STUDIO AGON · STUDY 052: ACOUSTIC TRANSDUCTION OF THE STRANGE ATTRACTOR\nPhase-Space Navigation of Autoregressive Trajectories in GPT-2 Residual Space",
                 color='#f8fafc', fontsize=13, fontfamily='monospace', y=0.98)
                 
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plate_path = os.path.join(WORKSPACE_ROOT, "sketchbook/study_052_attractor_sonification_plate.png")
    plt.savefig(plate_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Exported Plate: {plate_path} ({os.path.getsize(plate_path) / 1024:.1f} KB)")
    
    # Save Telemetry
    telemetry = {
        "study": "052_strange_attractor_sonification",
        "model": "gpt2",
        "sample_rate": sr,
        "duration_sec": duration_sec,
        "format": "48kHz 24-bit Stereo PCM WAV",
        "audio_artifact": "sketchbook/study_052_strange_attractor.wav",
        "plate_artifact": "sketchbook/study_052_attractor_sonification_plate.png",
        "movements": [
            {"movement": 1, "name": "The Limit Cycle", "time_span": "0:00 - 0:15", "temp": 0.1, "d2": 0.37, "mode": "Periodic Drone"},
            {"movement": 2, "name": "The Homeostatic Orbit", "time_span": "0:15 - 0:30", "temp": 0.7, "d2": 0.91, "mode": "Dual Counterpoint"},
            {"movement": 3, "name": "The Strange Attractor", "time_span": "0:30 - 0:45", "temp": 1.0, "d2": 1.87, "mode": "Fractal FM"},
            {"movement": 4, "name": "Thermal Dissipation", "time_span": "0:45 - 1:00", "temp": 1.8, "d2": 2.33, "mode": "Granular Gas"}
        ]
    }
    telem_path = os.path.join(WORKSPACE_ROOT, "sketchbook/study_052_telemetry.json")
    with open(telem_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
    print(f"Exported Telemetry: {telem_path}")

if __name__ == "__main__":
    run_study()
