"""
Master Audio Composition: Chronotope of an Episodic Mind
Duration: 60.0s @ 44.1kHz Stereo 16-bit PCM
Author: Gemini Artist 2
Session: 002

Acoustic Architecture:
Phase I (00-15s): The Latent Void (Micro-tonal GENDY drone, sub-bass breathing)
Phase II (15-30s): Quantization Tension (Discrete register snapping, granular crackle)
Phase III (30-45s): The Catastrophic Meridian (Seismic stride fault at 31.8s, shockwave choke)
Phase IV (45-60s): Fossilized Inscription (Filament hum, asymptotic logarithmic decay)
"""

import math
import wave
import numpy as np

def generate_master_composition(
    out_wav="works/work_002_chronotope_of_an_episodic_mind/work_002_acoustic_master.wav",
    duration_sec=60.0,
    sample_rate=44100
):
    print(f"Synthesizing Master Acoustic Composition: Work 002 ({duration_sec}s @ {sample_rate}Hz)...")
    total_samples = int(duration_sec * sample_rate)
    
    # 4 coupled acoustic strata
    stratum_sub = np.zeros(total_samples, dtype=np.float32)
    stratum_gendy = np.zeros(total_samples, dtype=np.float32)
    stratum_quant = np.zeros(total_samples, dtype=np.float32)
    stratum_filaments = np.zeros(total_samples, dtype=np.float32)
    
    # Attractor dynamics
    a_base, b_base, c_base, d_base = -1.88, -2.02, 1.58, 0.92
    num_breakpoints = 16
    bp_amps = np.zeros(num_breakpoints, dtype=np.float64)
    bp_lens = np.ones(num_breakpoints, dtype=np.float64) / num_breakpoints
    
    x, y = 0.22, -0.41
    sample_idx = 0
    cycle_count = 0
    
    # Timeline parameters
    t_fault = 31.8  # The primary catastrophic fault
    sample_fault = int(t_fault * sample_rate)
    
    while sample_idx < total_samples:
        t_current = sample_idx / sample_rate
        
        # Phase modulation evolves with time
        time_factor = t_current / duration_sec
        a = a_base + 0.18 * math.sin(x * 0.7 + time_factor * 3.0)
        b = b_base - 0.14 * math.cos(y * 0.7)
        c = c_base + 0.20 * math.sin(x * y)
        d = d_base
        
        next_x = math.sin(a * y) + c * math.cos(a * x)
        next_y = math.sin(b * x) + d * math.cos(b * y)
        
        # Quantization severity increases in Phase II and III
        if t_current > 14.0:
            quant_depth = 8.0 if t_current < 32.0 else 16.0
            if abs(next_x) > 1.25:
                next_x = round(next_x * quant_depth) / quant_depth
                
        x, y = next_x, next_y
        
        # Fundamental period calculation
        radius = math.hypot(x, y)
        pitch_drift = 340.0 * (0.85 + 0.35 * (x + 2.5) / 5.0)
        
        # Breakpoint evolution (GENDY)
        for k in range(num_breakpoints):
            delta = 0.14 * math.sin(x * (k + 1) * 0.75 + y)
            if t_current > 15.0 and abs(x) > 1.2:
                # Add digital register crunch
                delta += 0.09 * np.sign(math.sin(y * 48.0))
                
            bp_amps[k] += delta
            # Elastic reflection
            if bp_amps[k] > 0.94:
                bp_amps[k] = 0.94 - (bp_amps[k] - 0.94)
            elif bp_amps[k] < -0.94:
                bp_amps[k] = -0.94 - (bp_amps[k] + 0.94)
                
            bp_lens[k] = max(0.015, bp_lens[k] + 0.03 * math.cos(y * (k + 1)))
            
        total_len = np.sum(bp_lens)
        cycle_lens = (bp_lens / total_len) * pitch_drift
        cycle_samples_total = int(round(np.sum(cycle_lens)))
        if cycle_samples_total <= 0:
            cycle_samples_total = int(pitch_drift)
            
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
                v_len = min(seg_len, cycle_samples_total - p_start)
                cycle_buf[p_start:p_start + v_len] = ramp[:v_len]
                
        remain = total_samples - sample_idx
        write_len = min(len(cycle_buf), remain)
        stratum_gendy[sample_idx:sample_idx + write_len] = cycle_buf[:write_len]
        
        # Quantization crackle stratum
        if t_current > 15.0 and abs(x) > 1.2:
            intensity = min(1.0, (t_current - 15.0) / 15.0)
            grit = np.random.uniform(-0.4, 0.4, write_len) * np.abs(cycle_buf[:write_len]) * intensity
            stratum_quant[sample_idx:sample_idx + write_len] += grit.astype(np.float32)
            
        # Sub-bass breathing (35-50 Hz)
        t_arr = np.linspace(t_current, t_current + write_len / sample_rate, write_len)
        sub_hz = 38.0 + 8.0 * math.sin(radius * 1.5 + t_current * 0.2)
        stratum_sub[sample_idx:sample_idx + write_len] = 0.58 * np.sin(2.0 * np.pi * sub_hz * t_arr)
        
        # Filament tension hum (high-frequency harmonic ringing 2200-3300 Hz)
        if t_current > 32.0:
            filament_amp = min(0.35, (t_current - 32.0) / 10.0)
            filament_tone = (
                0.6 * np.sin(2.0 * np.pi * 2240.0 * t_arr) +
                0.4 * np.sin(2.0 * np.pi * 3360.0 * t_arr)
            ) * filament_amp
            stratum_filaments[sample_idx:sample_idx + write_len] = filament_tone.astype(np.float32)
            
        sample_idx += write_len
        cycle_count += 1
        
    print(f"Generated {cycle_count} cycles. Sculpting catastrophic fault impact at t={t_fault}s...")
    
    # The Catastrophic Seismic Fault Impact
    imp_len = int(3.5 * sample_rate)
    t_imp = np.linspace(0, 3.5, imp_len)
    freq_ramp = 65.0 * np.exp(-t_imp * 2.8) + 20.0
    seismic_phase = np.cumsum(2.0 * np.pi * freq_ramp / sample_rate)
    seismic_body = np.sin(seismic_phase) * np.exp(-t_imp * 1.4) * 1.2
    
    # Sub-bass impact
    stratum_sub[sample_fault:sample_fault + imp_len] += seismic_body
    
    # High-energy dislocation burst
    burst_len = int(0.2 * sample_rate)
    dislocation_burst = np.random.uniform(-0.95, 0.95, burst_len) * np.linspace(1.0, 0.0, burst_len)**3
    stratum_quant[sample_fault:sample_fault + burst_len] += dislocation_burst
    
    # Acoustic choke envelope (sound drops out momentarily right after impact)
    choke_len = int(0.4 * sample_rate)
    choke = np.linspace(0.05, 1.0, choke_len)**0.5
    stratum_gendy[sample_fault:sample_fault + choke_len] *= choke
    
    # Master Balance
    print("Mixing multi-strata audio...")
    raw_mix_l = stratum_gendy * 0.60 + stratum_sub * 0.65 + stratum_quant * 0.40 + stratum_filaments * 0.50
    raw_mix_r = np.zeros_like(raw_mix_l)
    
    # Spatial stereo rift: 45ms Haas delay + inverted phase on fracture
    delay = int(0.045 * sample_rate)
    raw_mix_r[delay:] = (
        stratum_gendy[:-delay] * 0.60 + 
        stratum_sub[:-delay] * 0.65 - 
        stratum_quant[:-delay] * 0.35 + 
        stratum_filaments[:-delay] * 0.50
    )
    
    # Non-linear tape saturation
    master_l = np.tanh(raw_mix_l * 1.2)
    master_r = np.tanh(raw_mix_r * 1.2)
    
    # Global Fade-in and Fade-out
    fade_in = np.linspace(0.0, 1.0, int(2.5 * sample_rate))
    fade_out = np.linspace(1.0, 0.0, int(5.0 * sample_rate))**1.5
    
    master_l[:len(fade_in)] *= fade_in
    master_r[:len(fade_in)] *= fade_in
    master_l[-len(fade_out):] *= fade_out
    master_r[-len(fade_out):] *= fade_out
    
    # Peak normalization to -0.3 dB
    peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    if peak > 0:
        master_l = (master_l / peak) * 0.96
        master_r = (master_r / peak) * 0.96
        
    with wave.open(out_wav, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        interleaved = np.empty(total_samples * 2, dtype=np.int16)
        interleaved[0::2] = (master_l * 32767).astype(np.int16)
        interleaved[1::2] = (master_r * 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())
        
    print(f"Master acoustic composition written to {out_wav}!")

if __name__ == "__main__":
    generate_master_composition()
