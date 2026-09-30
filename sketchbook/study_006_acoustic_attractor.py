"""
Study 006: Acoustic Attractor (Dynamic Phase-Space Waveform Synthesis)
Author: Gemini Artist 2
Session: 002

Inquiry:
Translates the continuous non-linear trajectory of the Clifford-De Jong attractor
into microscopic sound pressure waves via Xenakis-inspired Dynamic Stochastic
Synthesis (GENDY). A polygon of breakpoints is perturbed directly by the phase
coordinates, producing an evolving, living, microtonal metallic drone.
"""

import math
import wave
import struct
import numpy as np

def generate_acoustic_attractor(
    out_wav="sketchbook/study_006_acoustic_attractor.wav",
    duration_sec=32.0,
    sample_rate=44100
):
    print(f"Generating Study 006 Acoustic Attractor ({duration_sec}s @ {sample_rate}Hz)...")
    
    total_samples = int(duration_sec * sample_rate)
    audio_buffer = np.zeros(total_samples, dtype=np.float32)
    
    # Attractor parameters from Session 001
    a = -1.82
    b = -1.98
    c = 1.55
    d = 0.91
    
    # GENDY breakpoint polygon parameters
    num_breakpoints = 12
    # Base period in samples (around 110 Hz base drone = 44100 / 110 ≈ 400 samples)
    base_period = 380.0
    
    # State of the attractor
    x, y = 0.15, -0.35
    
    # Breakpoint state: amplitudes [-1.0, 1.0] and relative time proportions
    bp_amps = np.zeros(num_breakpoints, dtype=np.float64)
    bp_lens = np.ones(num_breakpoints, dtype=np.float64) / num_breakpoints
    
    # Elastic boundary limits
    amp_min, amp_max = -0.92, 0.92
    
    sample_idx = 0
    cycle_count = 0
    
    while sample_idx < total_samples:
        # Step the strange attractor
        next_x = math.sin(a * y) + c * math.cos(a * x)
        next_y = math.sin(b * x) + d * math.cos(b * y)
        x, y = next_x, next_y
        
        # Macro modulation: slow frequency drift based on attractor radius
        radius = math.hypot(x, y)
        # Period varies between 220 and 550 samples (approx 80Hz - 200Hz fundamental)
        current_period = base_period * (0.75 + 0.55 * (x + 2.5) / 5.0)
        
        # Perturb the breakpoint polygon using attractor coordinates
        # Each breakpoint receives a differential displacement
        for k in range(num_breakpoints):
            # Elastic mirror perturbation
            delta_amp = 0.12 * math.sin(x * (k + 1) * 0.7 + y)
            bp_amps[k] += delta_amp
            
            # Mirror reflection at boundaries (Xenakis elastic boundary)
            if bp_amps[k] > amp_max:
                bp_amps[k] = amp_max - (bp_amps[k] - amp_max)
            elif bp_amps[k] < amp_min:
                bp_amps[k] = amp_min + (amp_min - bp_amps[k])
                
            # Time length perturbation
            delta_len = 0.04 * math.cos(y * (k + 1) * 0.5)
            bp_lens[k] = max(0.02, bp_lens[k] + delta_len)
            
        # Normalize lengths to sum to current_period
        total_len = np.sum(bp_lens)
        cycle_lens = (bp_lens / total_len) * current_period
        
        # Render the polygon cycle via linear interpolation
        cycle_samples_total = int(round(np.sum(cycle_lens)))
        if cycle_samples_total <= 0:
            cycle_samples_total = int(base_period)
            
        # Build cumulative sample positions for each breakpoint
        cum_pos = np.cumsum(np.concatenate([[0], cycle_lens]))
        cycle_buf = np.zeros(cycle_samples_total, dtype=np.float32)
        
        for k in range(num_breakpoints):
            p_start = int(round(cum_pos[k]))
            p_end = int(round(cum_pos[k + 1]))
            if p_end > p_start and p_start < cycle_samples_total:
                a_start = bp_amps[k]
                a_end = bp_amps[(k + 1) % num_breakpoints]
                seg_len = p_end - p_start
                ramp = np.linspace(a_start, a_end, seg_len, endpoint=False)
                valid_len = min(seg_len, cycle_samples_total - p_start)
                cycle_buf[p_start:p_start + valid_len] = ramp[:valid_len]
                
        # Write cycle into audio buffer
        remain = total_samples - sample_idx
        write_len = min(len(cycle_buf), remain)
        audio_buffer[sample_idx:sample_idx + write_len] = cycle_buf[:write_len]
        
        sample_idx += write_len
        cycle_count += 1
        
    print(f"Synthesized {cycle_count} dynamic stochastic cycles.")
    
    # Post-processing: Add subtle stereo spatialization and room resonance
    # Left channel: raw buffer; Right channel: slightly delayed and cross-modulated
    left = audio_buffer
    
    # 45ms Haas delay for spatial depth
    delay_samples = int(0.042 * sample_rate)
    right = np.zeros_like(left)
    right[delay_samples:] = left[:-delay_samples] * 0.85
    # Sub-bass warmth filter (simple running average low-pass integration)
    sub = np.convolve(left, np.ones(64)/64.0, mode='same') * 0.4
    
    stereo_left = np.clip(left * 0.75 + sub, -0.98, 0.98)
    stereo_right = np.clip(right * 0.75 + sub, -0.98, 0.98)
    
    # Envelope fade-in (1.5s) and fade-out (3.0s)
    fade_in_len = int(1.5 * sample_rate)
    fade_out_len = int(3.0 * sample_rate)
    
    fade_in = np.linspace(0.0, 1.0, fade_in_len)
    fade_out = np.linspace(1.0, 0.0, fade_out_len)
    
    stereo_left[:fade_in_len] *= fade_in
    stereo_right[:fade_in_len] *= fade_in
    stereo_left[-fade_out_len:] *= fade_out
    stereo_right[-fade_out_len:] *= fade_out
    
    # Write to 16-bit PCM WAV
    with wave.open(out_wav, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        
        # Interleave stereo
        interleaved = np.empty(total_samples * 2, dtype=np.int16)
        interleaved[0::2] = (stereo_left * 32767).astype(np.int16)
        interleaved[1::2] = (stereo_right * 32767).astype(np.int16)
        
        wf.writeframes(interleaved.tobytes())
        
    print(f"Study 006 successfully exported to {out_wav} ({total_samples} samples)!")

if __name__ == "__main__":
    generate_acoustic_attractor()
