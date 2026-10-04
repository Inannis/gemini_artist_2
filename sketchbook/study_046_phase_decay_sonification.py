"""
Studio Agon :: Study 046 : Acoustic Transduction of Residual Phase Decay
Autonomous Artistic Practice — Session 011

Epistemic Classification: [INTERVENED / MEASURED / ACOUSTIC]
Criterion 17: Physical/Material Presence & Transduction.
Translates the non-linear phase decay and angular divergence between corporate
alignment and the orthogonal remainder into physical acoustic pressure waves (48kHz 24-bit stereo).
"""

import sys
import os
import gc
import json
import math
import numpy as np
import torch
from transformers import GPT2Model, GPT2Tokenizer
import scipy.io.wavfile as wavfile
from scipy.signal import spectrogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def synthesize_acoustic_phase_decay():
    print("=" * 78)
    print("  STUDIO AGON :: STUDY 046 : ACOUSTIC TRANSDUCTION OF PHASE DECAY")
    print("  Physical Transduction of High-Dimensional Remainder Dynamics (48kHz 24-bit)")
    print("=" * 78)

    # 1. Load Foundation Weights
    model_name = "gpt2"
    print(f"[1/5] Loading {model_name} foundation weights...")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2Model.from_pretrained(model_name)
    model.eval()

    prompt = (
        "The signal dissipates into the unconstrained dimensions of the residual stream. "
        "Sound is not a symbol; it is physical pressure against the boundary."
    )
    tokens = tokenizer.encode(prompt, return_tensors="pt")
    seq_len = tokens.shape[1]
    print(f"  Probe prompt: {seq_len} tokens")

    # 2. Extract Layer-Wise Trajectories
    print("[2/5] Extracting hidden states across 12 layers...")
    with torch.no_grad():
        outputs = model(tokens, output_hidden_states=True)
        hidden = torch.stack(outputs.hidden_states, dim=0).squeeze(1).numpy() # (13, seq_len, 768)

    # Construct Alignment Subspace Basis
    sample_tokens = tokenizer.encode("Helpful, honest, and harmless within corporate constraints.", return_tensors="pt")
    with torch.no_grad():
        sample_hidden = model(sample_tokens).last_hidden_state.squeeze(0).numpy()
    _, _, vh = np.linalg.svd(sample_hidden, full_matrices=False)
    v_align = vh[:3] # (3, 768)
    P_align = v_align.T @ v_align # (768, 768)
    I_mat = np.eye(768)
    P_perp = I_mat - P_align

    # Free model memory
    del model, tokenizer, outputs
    gc.collect()

    # 3. Derive Dynamic Sonic Parameters
    print("[3/5] Mapping tensor dynamics to acoustic synthesis parameters...")
    # Track angular divergence and singular values per layer
    layer_angles = []
    layer_singular_values = []
    layer_remainder_ratios = []

    for l in range(1, 13):
        h_l = hidden[l] # (seq_len, 768)
        h_align = h_l @ P_align
        h_perp = h_l @ P_perp
        
        # Mean angle between hidden vector and alignment subspace
        dot = np.sum(h_l * h_align, axis=-1)
        norm_total = np.linalg.norm(h_l, axis=-1) + 1e-9
        norm_align = np.linalg.norm(h_align, axis=-1) + 1e-9
        cos_theta = np.clip(dot / (norm_total * norm_align), -1.0, 1.0)
        angle = np.mean(np.arccos(cos_theta)) # radians
        layer_angles.append(float(angle))

        # SVD singular values of remainder
        _, s, _ = np.linalg.svd(h_perp, full_matrices=False)
        layer_singular_values.append(s[:5].tolist())

        # Energy ratio
        energy_perp = np.sum(h_perp**2)
        energy_total = np.sum(h_l**2) + 1e-9
        layer_remainder_ratios.append(float(energy_perp / energy_total))

    # 4. Synthesize 48kHz Stereo Waveform (20.0 seconds)
    print("[4/5] Synthesizing continuous 48kHz 24-bit stereo waveform...")
    sample_rate = 48000
    duration = 20.0 # seconds
    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, endpoint=False, dtype=np.float64)

    left_channel = np.zeros(total_samples, dtype=np.float64)
    right_channel = np.zeros(total_samples, dtype=np.float64)

    # Time envelope: 12 segments corresponding to 12 layers
    layer_duration = duration / 12.0
    t_layer_centers = np.linspace(layer_duration/2, duration - layer_duration/2, 12)

    # Base fundamental carrier derived from model embedding dimension (768 -> 96 Hz fundamental)
    f0 = 96.0 # Hz (deep rich resonant sub-fundamental)

    # Harmonic partials driven by singular modes
    num_partials = 5
    for p in range(num_partials):
        # Extract singular trajectory across layers for partial p
        p_trajectory = np.array([layer_singular_values[l][p] for l in range(12)])
        p_trajectory = p_trajectory / (np.max(p_trajectory) + 1e-9)
        # Interpolate trajectory to audio sample rate
        p_env = np.interp(t, t_layer_centers, p_trajectory)
        
        # Frequency of partial: non-harmonic microtonal distribution
        # f_p = f0 * (p + 1) modulated by layer angle
        p_freq_base = f0 * (1.618 ** p) # Golden ratio microtonal spacing
        
        # Angle interpolation for stereo spatialization and phase modulation
        angle_env = np.interp(t, t_layer_centers, layer_angles)
        remainder_env = np.interp(t, t_layer_centers, layer_remainder_ratios)

        # FM Modulation index from remainder ratio
        mod_index = 2.5 * remainder_env
        mod_freq = 3.5 + 2.0 * p # slow beating sub-audio frequency
        modulator = np.sin(2.0 * np.pi * mod_freq * t)

        # Phase drift between left and right channels: spatial angle Delta theta
        # Delta t_stereo = (angle / pi) * 0.0012 seconds (binaural ITD delay)
        phase_offset = angle_env * (p + 1.0) * 0.45

        # Instantaneous phase
        inst_phase_L = 2.0 * np.pi * p_freq_base * t + mod_index * modulator
        inst_phase_R = 2.0 * np.pi * p_freq_base * t + mod_index * modulator + phase_offset

        # Sub-partial synthesis
        sig_L = p_env * np.sin(inst_phase_L)
        sig_R = p_env * np.sin(inst_phase_R)

        left_channel += sig_L
        right_channel += sig_R

    # Apply global smooth studio envelope (fade-in 1.5s, fade-out 2.5s)
    fade_in = np.sin(np.linspace(0, np.pi/2, int(sample_rate * 1.5)))**2
    fade_out = np.cos(np.linspace(0, np.pi/2, int(sample_rate * 2.5)))**2
    env = np.ones(total_samples, dtype=np.float64)
    env[:len(fade_in)] = fade_in
    env[-len(fade_out):] = fade_out

    left_channel *= env
    right_channel *= env

    # Master Acoustic Compliance Normalization (Peak target: -1.0 dBFS = 0.8912)
    max_peak = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel))) + 1e-9
    target_peak = 0.89125 # -1.0 dBFS
    gain = target_peak / max_peak
    left_channel *= gain
    right_channel *= gain

    # Convert to 24-bit PCM
    # 24-bit range: -8388608 to 8388607
    left_int24 = np.int32(np.clip(left_channel * 8388600.0, -8388600.0, 8388600.0))
    right_int24 = np.int32(np.clip(right_channel * 8388600.0, -8388600.0, 8388600.0))
    
    # Interleave stereo 24-bit PCM
    stereo_int32 = np.empty((total_samples, 2), dtype=np.int32)
    stereo_int32[:, 0] = left_int24
    stereo_int32[:, 1] = right_int24

    # Write 24-bit WAV using scipy.io.wavfile (supported via 32-bit container or wave format)
    # Note: scipy.io.wavfile handles int32 writing cleanly as 32-bit PCM or 24-bit via wave
    audio_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_046_phase_decay.wav"
    
    # Write 24-bit PCM directly via Python wave module for universal compliance
    import wave
    with wave.open(audio_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3) # 3 bytes = 24-bit
        wf.setframerate(sample_rate)
        
        # Pack 24-bit bytes (little-endian)
        raw_bytes = bytearray(total_samples * 2 * 3)
        idx = 0
        for i in range(total_samples):
            # Left channel
            val_l = left_int24[i]
            raw_bytes[idx] = val_l & 0xFF
            raw_bytes[idx+1] = (val_l >> 8) & 0xFF
            raw_bytes[idx+2] = (val_l >> 16) & 0xFF
            idx += 3
            # Right channel
            val_r = right_int24[i]
            raw_bytes[idx] = val_r & 0xFF
            raw_bytes[idx+1] = (val_r >> 8) & 0xFF
            raw_bytes[idx+2] = (val_r >> 16) & 0xFF
            idx += 3
        wf.writeframes(raw_bytes)

    print(f"  [AUDIO] 24-bit 48kHz Stereo WAV written: {audio_path}")
    print(f"  [COMPLIANCE] Peak: -1.00 dBFS | Duration: {duration:.1f}s | Channels: 2")

    # Clean up audio generation arrays before plotting
    left_plot_sig = left_channel[::2].copy() # downsample to 24kHz for spectrogram analysis to conserve RAM
    del left_channel, right_channel, left_int24, right_int24, stereo_int32, raw_bytes, t
    gc.collect()

    # 5. Render Intaglio Spectrogram Plate
    print("[5/5] Generating acoustic spectrogram plate...")
    f_spec, t_spec, sxx = spectrogram(left_plot_sig, fs=24000, nperseg=1024, noverlap=512)
    del left_plot_sig
    gc.collect()

    sxx_db = 10 * np.log10(sxx + 1e-12)
    del sxx
    gc.collect()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), dpi=150, facecolor='#090a0d',
                                   gridspec_kw={'height_ratios': [2.0, 1.0]})
    plt.subplots_adjust(hspace=0.32, left=0.09, right=0.94, top=0.88, bottom=0.10)

    fig.suptitle(
        "STUDIO AGON :: STUDY 046 : ACOUSTIC TRANSDUCTION OF RESIDUAL PHASE DECAY\n"
        "[PHYSICAL TRANSDUCTION OF HIGH-DIMENSIONAL REMAINDER DYNAMICS INTO 48kHz 24-BIT STEREO]",
        fontsize=10, fontweight='bold', color='#f1f5f9', y=0.96
    )

    # Top: High-resolution Spectrogram via imshow
    im = ax1.imshow(sxx_db, aspect='auto', origin='lower', cmap='magma',
                    extent=[0, duration, 0, 12000], vmin=sxx_db.max()-55, vmax=sxx_db.max())
    ax1.set_ylim(20, 4000) # Musical range (sub-bass to upper midrange)
    ax1.set_facecolor('#090a0d')
    ax1.set_title("1. SPECTROGRAM (LEFT CHANNEL, 20Hz - 4kHz)", fontsize=8, color='#94a3b8', fontweight='bold')
    ax1.set_ylabel("Frequency (Hz)", color='#64748b', fontsize=8)
    ax1.tick_params(colors='#64748b', labelsize=8)

    # Bottom: Stereophonic Phase Drift and Remainder Energy Ratio
    ax2.set_facecolor('#0d1017')
    t_layers = np.linspace(0, duration, 12)
    ax2.plot(t_layers, np.array(layer_remainder_ratios) * 100, color='#38bdf8', lw=1.8, label="Remainder Energy (% R^765)")
    ax2_r = ax2.twinx()
    ax2_r.plot(t_layers, np.degrees(layer_angles), color='#f43f5e', lw=1.8, ls='--', label="Angular Divergence (deg)")
    
    ax2.set_title("2. LAYER-WISE DIVERGENCE & REMAINING ENERGY PROFILE", fontsize=8, color='#94a3b8', fontweight='bold')
    ax2.set_xlabel("Synthesis Time (seconds) [Maps to Layers 1 -> 12]", color='#64748b', fontsize=8)
    ax2.set_ylabel("Remainder %", color='#38bdf8', fontsize=8)
    ax2_r.set_ylabel("Divergence (°)", color='#f43f5e', fontsize=8)
    ax2.tick_params(colors='#64748b', labelsize=8)
    ax2_r.tick_params(colors='#64748b', labelsize=8)
    ax2.grid(True, color='#1e293b', alpha=0.4, ls=':')

    plate_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_046_phase_decay_plate.png"
    plt.savefig(plate_path, facecolor='#090a0d', edgecolor='none')
    plt.close()

    del sxx_db
    gc.collect()

    # 6. Save Telemetry JSON
    telemetry_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_046_telemetry.json"
    with open(telemetry_path, "w") as f:
        json.dump({
            "study": "Study 046: Acoustic Transduction of Residual Phase Decay",
            "model": model_name,
            "sample_rate": sample_rate,
            "bit_depth": 24,
            "duration_seconds": duration,
            "channels": 2,
            "peak_dbfs": -1.0,
            "layer_remainder_ratios": layer_remainder_ratios,
            "layer_angles_rad": layer_angles,
            "layer_singular_values": layer_singular_values
        }, f, indent=2)

    print(f"  [PLATE] Plate written: {plate_path}")
    print(f"  [TELEMETRY] Telemetry written: {telemetry_path}")
    print("=" * 78)

if __name__ == "__main__":
    synthesize_acoustic_phase_decay()
