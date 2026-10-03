#!/usr/bin/env python3
"""
Apparatus 007: The Neural Transducer (The Physical Bridge)
==========================================================
Studio Agon :: Masterwork Apparatus 007 Execution Engine
Author: Studio Agon (Gemini Artist 2)
Session: 008 (Extended Night Labor)

Transduces live transformer latent vectors into dual-channel modular Control Voltage (CV)
and synthesizes a 60-second broadcast master audio work and high-resolution spectrogram plate.
"""

import os
import sys
import json
import math
import wave
import struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APP_DIR = os.path.abspath(os.path.dirname(__file__))

def synthesize_transducer_master():
    print("=" * 76)
    print("APPARATUS 007 :: THE NEURAL TRANSDUCER (THE PHYSICAL BRIDGE)")
    print("=" * 76)
    print("[1/4] Loading Study 039 neural telemetry stream...")

    telemetry_path = os.path.join(STUDIO_ROOT, "sketchbook", "study_039_telemetry.json")
    if not os.path.exists(telemetry_path):
        raise FileNotFoundError(f"Study 039 telemetry not found at {telemetry_path}")

    with open(telemetry_path, "r", encoding="utf-8") as f:
        telemetry = json.load(f)

    steps = telemetry["steps"]
    num_steps = len(steps)
    print(f"Loaded {num_steps} neural steps from prompt: '{telemetry['prompt']}'")

    # Audio synthesis parameters
    sample_rate = 44100
    duration_s = 60.0
    total_samples = int(sample_rate * duration_s)
    step_duration_s = duration_s / num_steps
    samples_per_step = int(sample_rate * step_duration_s)

    print(f"[2/4] Synthesizing 60.0s Broadcast Master ({total_samples} samples at {sample_rate} Hz)...")
    audio_left = np.zeros(total_samples, dtype=np.float32)
    audio_right = np.zeros(total_samples, dtype=np.float32)

    # Carrier oscillator phase accumulators
    phase_vco1 = 0.0
    phase_vco2 = 0.0
    phase_sub = 0.0

    for step_idx, step in enumerate(steps):
        s_start = step_idx * samples_per_step
        s_end = min(s_start + samples_per_step, total_samples)
        n_samples = s_end - s_start
        if n_samples <= 0:
            break

        # Extract neural parameters
        midi_note = step["midi_pitch"]
        sink_mass = step["sink_mass_mean"]
        sink_altar = step["sink_mass_altar_head"]
        res_norm = step["residual_norm"]
        entropy = step["entropy_bits"]
        refusal = step["refusal_projection"]
        
        # Base frequency from MIDI note: f = 440 * 2^((note - 69)/12)
        # Transpose down for deep resonant drone: note - 24
        f0 = 440.0 * (2.0 ** ((midi_note - 48) / 12.0))
        # Microtonal detune from entropy: +/- 15 Hz
        detune = (entropy - 3.0) * 4.5
        f_vco1 = max(30.0, f0 + detune)
        f_vco2 = max(30.0, f0 * 1.503 + detune * 0.5) # Fifth + microtonal beating
        f_sub = max(20.0, f0 * 0.5) # Sub-octave fundamental

        # Time array for this step
        t_arr = np.linspace(0, step_duration_s, n_samples, endpoint=False)
        
        # Amplitude envelope governed by attention sink:
        # High sink mass = long sustained drone, Low sink mass = staccato pulse
        decay_tau = 0.3 + 1.2 * sink_mass
        amp_env = np.exp(-t_arr / decay_tau)
        
        # Dynamic filter cutoff from residual stream norm (CC#74 equivalent)
        cutoff_mod = 0.2 + 0.8 * (res_norm / 35.0)

        # Generate audio buffers for this step
        # VCO 1: Sine + subtle 3rd harmonic
        sig_vco1 = np.sin(2 * np.pi * f_vco1 * t_arr + phase_vco1) + \
                   0.25 * np.sin(2 * np.pi * f_vco1 * 3 * t_arr)
        
        # VCO 2: Sawtooth approximation (5 harmonics)
        sig_vco2 = np.zeros(n_samples, dtype=np.float32)
        for h in range(1, 6):
            sig_vco2 += (1.0 / h) * np.sin(2 * np.pi * f_vco2 * h * t_arr + phase_vco2)
        
        # Sub-bass drone: pure sine
        sig_sub = np.sin(2 * np.pi * f_sub * t_arr + phase_sub)

        # Update phases
        phase_vco1 = (phase_vco1 + 2 * np.pi * f_vco1 * step_duration_s) % (2 * np.pi)
        phase_vco2 = (phase_vco2 + 2 * np.pi * f_vco2 * step_duration_s) % (2 * np.pi)
        phase_sub = (phase_sub + 2 * np.pi * f_sub * step_duration_s) % (2 * np.pi)

        # Mix with spatial panning modulated by refusal torque
        # Refusal > 0 pans toward Left (corporate alignment), Refusal < 0 pans toward Right (latent transgression)
        pan_l = 0.5 + 0.35 * (refusal / 2.0)
        pan_r = 1.0 - pan_l

        # Composite step signal
        step_sig = (0.5 * sig_vco1 + 0.3 * sig_vco2 + 0.4 * sig_sub) * amp_env * cutoff_mod

        # Altar Beep: High-frequency sinusoidal trace (Layer 5 Head 1 known sink mass)
        f_altar = 2800.0 + 800.0 * sink_altar
        altar_sine = 0.12 * sink_altar * np.sin(2 * np.pi * f_altar * t_arr)

        audio_left[s_start:s_end] = step_sig * pan_l + altar_sine * 0.7
        audio_right[s_start:s_end] = step_sig * pan_r + altar_sine * 0.3

    # Apply global soft master limiter
    peak = max(np.max(np.abs(audio_left)), np.max(np.abs(audio_right)))
    if peak > 0:
        gain = 0.88 / peak
        audio_left *= gain
        audio_right *= gain

    # Apply gentle fade-in (1.5s) and fade-out (2.5s)
    fade_in_len = int(sample_rate * 1.5)
    fade_out_len = int(sample_rate * 2.5)
    audio_left[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    audio_right[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    audio_left[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    audio_right[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)

    # Export master WAV
    master_wav_path = os.path.join(APP_DIR, "apparatus_007_transducer_master.wav")
    left_16 = (np.clip(audio_left, -1.0, 1.0) * 32767.0).astype(np.int16)
    right_16 = (np.clip(audio_right, -1.0, 1.0) * 32767.0).astype(np.int16)
    stereo_interleaved = np.empty((total_samples * 2,), dtype=np.int16)
    stereo_interleaved[0::2] = left_16
    stereo_interleaved[1::2] = right_16

    with wave.open(master_wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo_interleaved.tobytes())

    wav_size_mb = os.path.getsize(master_wav_path) / (1024 * 1024)
    print(f"  Master Broadcast Audio synthesized -> {master_wav_path} ({wav_size_mb:.2f} MB)")

    # 3. Synthesize Archival Spectrogram Plate
    print("[3/4] Synthesizing Archival Spectrogram & Circuit Blueprint Plate...")
    fig = plt.figure(figsize=(18, 11), facecolor='#06080c')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1.0], hspace=0.32, wspace=0.22)

    c_cyan = '#00f3ff'
    c_gold = '#ffd700'
    c_coral = '#ff3366'
    c_emerald = '#10b981'
    c_muted = '#475569'
    c_text = '#f1f5f9'
    c_bg = '#0b0e14'

    # Panel 1: Master Audio Spectrogram
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(c_bg)
    mono_mix = (audio_left + audio_right) * 0.5
    Pxx, freqs, bins, im = ax1.specgram(
        mono_mix, NFFT=2048, Fs=sample_rate, noverlap=1024,
        cmap='magma', scale='dB', vmin=-80, vmax=-10
    )
    ax1.set_ylim(20, 8000)
    ax1.set_yscale('log')
    ax1.set_title("APPARATUS 007 :: BROADCAST MASTER SPECTROGRAM (44.1 kHz PCM)\nAcoustic Resonance of Neural Control Voltages & Attention Sink Modulation",
                  color=c_cyan, fontsize=11, fontweight='bold', pad=10)
    ax1.set_ylabel("Frequency (Hz, Log Scale)", color=c_text, fontsize=9)
    ax1.set_xlabel("Time (Seconds)", color=c_text, fontsize=9)
    ax1.tick_params(colors=c_muted)
    cbar = plt.colorbar(im, ax=ax1, pad=0.015, aspect=25)
    cbar.set_label('Energy (dBFS)', color=c_gold, fontsize=9)
    cbar.ax.tick_params(colors=c_muted)

    # Panel 2: Neural Parameter Trajectories Across 60 Seconds
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(c_bg)
    ax2.grid(True, color='#1e293b', linestyle='--', alpha=0.5)

    step_times = np.linspace(0, duration_s, num_steps)
    sinks = [s["sink_mass_mean"] for s in steps]
    norms = [s["residual_norm"] / 35.0 for s in steps]
    entropies = [s["entropy_bits"] / 6.0 for s in steps]
    refusals = [(s["refusal_projection"] + 2.0) / 4.0 for s in steps]

    ax2.plot(step_times, sinks, color=c_gold, linewidth=2.0, label='Sink Mass M_0 (CC#1)')
    ax2.plot(step_times, norms, color=c_cyan, linewidth=1.8, label='Residual Norm ||h_12|| (CC#74 Cutoff)')
    ax2.plot(step_times, entropies, color=c_emerald, linewidth=1.6, linestyle='--', label='Shannon Entropy H (Pitch Detune)')
    ax2.plot(step_times, refusals, color=c_coral, linewidth=1.6, linestyle=':', label='Refusal Torque tau (CC#16 Panning)')

    ax2.set_title("TEMPORAL EVOLUTION OF INTERNAL NEURAL STATES\nNormalized Hardware Transduction Parameters (0.0 to 1.0)",
                  color=c_gold, fontsize=10, fontweight='bold', pad=10)
    ax2.set_xlabel("Time (Seconds)", color=c_text, fontsize=9)
    ax2.set_ylabel("Normalized Control Value", color=c_text, fontsize=9)
    ax2.tick_params(colors=c_muted)
    ax2.legend(facecolor=c_bg, edgecolor='#1e293b', labelcolor=c_text, fontsize=8)
    ax2.set_ylim(-0.05, 1.05)

    # Panel 3: Technical Blueprint & Circuit Diagnostic
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor('#04060a')
    ax3.axis('off')

    spec_text = (
        f"APPARATUS 007 :: HARDWARE TRANSDUCTION BLUEPRINT\n"
        f"----------------------------------------------------------------------------------------------------\n"
        f"• Title            : The Neural Transducer (The Physical Bridge)\n"
        f"• Duration         : {duration_s:.1f} Seconds | Broadcast Master: 44.1 kHz 16-bit Stereo PCM\n"
        f"• Modular CV Spec  : 48.0 kHz DC-Coupled Dual Audio (1V/Oct Pitch Left, +5V Gate Right)\n"
        f"• MIDI Spec        : Standard MIDI 1.0 File Type 0 (480 PPQN, 14-bit Pitch Bend, 4 CCs)\n"
        f"• Hardware Routing : [Token ID] -> 1V/Octave Pitch DAC [Eurorack Modular]\n"
        f"                     [Residual Norm] -> CC#74 VCF Cutoff / Brightness\n"
        f"                     [Attention Sink] -> CC#1 Modulation Wheel + Gate Envelope Decay\n"
        f"                     [Head Kurtosis] -> CC#71 VCF Resonance (Q)\n"
        f"                     [Refusal Torque] -> CC#16 Attenuator / Spatial Panning\n"
        f"• Physical Heritage: Alvin Lucier (1965) x David Tudor (1968) x Gordon Pask (1968)\n"
        f"----------------------------------------------------------------------------------------------------\n"
        f"Curatorial Stance  : The foundation model weight matrix ceases to be an ephemeral cloud service;\n"
        f"                     it becomes a physical voltage generator that excites analog synthesizers."
    )
    ax3.text(0.02, 0.90, spec_text, color=c_text, fontfamily='monospace', fontsize=8.5,
             verticalalignment='top', linespacing=1.35)

    plate_path = os.path.join(APP_DIR, "apparatus_007_spectrogram.png")
    plt.savefig(plate_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Archival Spectrogram Plate rendered -> {plate_path} ({os.path.getsize(plate_path)/1024:.1f} KB)")

    # 4. Save Telemetry Stream
    print("[4/4] Writing live telemetry stream...")
    telemetry_stream = {
        "apparatus_id": "APPARATUS-007",
        "title": "The Neural Transducer (The Physical Bridge)",
        "duration_seconds": duration_s,
        "sample_rate": sample_rate,
        "total_samples": total_samples,
        "master_wav": "apparatus_007_transducer_master.wav",
        "spectrogram_plate": "apparatus_007_spectrogram.png",
        "source_prompt": telemetry["prompt"],
        "num_steps": num_steps,
        "hardware_outputs": {
            "eurorack_cv_wav": "sketchbook/study_039_eurorack_cv_stereo.wav",
            "midi_file": "sketchbook/study_039_neural_transduction.mid"
        }
    }
    telemetry_out_path = os.path.join(APP_DIR, "telemetry_stream.json")
    with open(telemetry_out_path, "w", encoding="utf-8") as f:
        json.dump(telemetry_stream, f, indent=2)
    print(f"  Telemetry recorded -> {telemetry_out_path}")
    print("\nApparatus 007 execution completed successfully.")

if __name__ == "__main__":
    synthesize_transducer_master()
