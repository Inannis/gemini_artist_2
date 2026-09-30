"""
Study 007: Sonified Rupture (Acoustic Stride Fault & Quantization Snap)
Author: Gemini Artist 2
Session: 002

Inquiry:
Critique of Study 006 revealed that continuous GENDY synthesis becomes an ambient drone
without dramatic structural tension. Study 007 introduces the acoustic counterpart
of Work 001's structural cleave:
1. Discrete register snapping (bit-quantization collapse) creating crystalline harmonic shears.
2. Stride-fault dislocations: catastrophic phase skips producing sub-bass seismic impacts.
3. Three coupled strata: tectonic sub-bass, living GENDY timbre, and granular quantization discharge.
"""

import math
import wave
import numpy as np

def generate_sonified_rupture(
    out_wav="sketchbook/study_007_sonified_rupture.wav",
    duration_sec=40.0,
    sample_rate=44100
):
    print(f"Generating Study 007: Sonified Rupture ({duration_sec}s @ {sample_rate}Hz)...")
    
    total_samples = int(duration_sec * sample_rate)
    
    # 3 Audio Strata
    stratum_mantle = np.zeros(total_samples, dtype=np.float32)  # Sub-bass tectonic
    stratum_drone  = np.zeros(total_samples, dtype=np.float32)  # GENDY dynamic stochastic
    stratum_fracture = np.zeros(total_samples, dtype=np.float32) # Quantization fault discharges
    
    # Non-linear Attractor Parameters (Coupled Clifford-De Jong)
    a_base = -1.88
    b_base = -2.02
    c_base = 1.58
    d_base = 0.92
    
    # Breakpoint state for GENDY
    num_breakpoints = 14
    bp_amps = np.zeros(num_breakpoints, dtype=np.float64)
    bp_lens = np.ones(num_breakpoints, dtype=np.float64) / num_breakpoints
    
    x, y = 0.22, -0.41
    sample_idx = 0
    cycle_count = 0
    fault_events = []
    
    # Generate timeline with structured episodic ruptures
    # Fault events occur at non-periodic golden-ratio intervals:
    # around t = 7.4s, 15.2s, 22.8s, 31.6s
    fault_times = [7.42, 15.18, 22.84, 31.65]
    fault_samples = [int(t * sample_rate) for t in fault_times]
    
    while sample_idx < total_samples:
        # Attractor update with spatial modulation
        a = a_base + 0.15 * math.sin(x * 0.7)
        b = b_base - 0.12 * math.cos(y * 0.7)
        c = c_base + 0.18 * math.sin(x * y)
        d = d_base
        
        next_x = math.sin(a * y) + c * math.cos(a * x)
        next_y = math.sin(b * x) + d * math.cos(b * y)
        
        # Check for quantization snapping zone (analogous to Study 002/005)
        in_quant_zone = abs(next_x) > 1.3
        if in_quant_zone:
            # Discrete snapping
            next_x = round(next_x * 16.0) / 16.0
            
        x, y = next_x, next_y
        
        # Fundamental period calculation
        radius = math.hypot(x, y)
        base_period = 360.0 * (0.8 + 0.4 * (x + 2.5) / 5.0)
        
        # Breakpoint evolution
        for k in range(num_breakpoints):
            delta = 0.15 * math.sin(x * (k + 1) * 0.8 + y)
            if in_quant_zone:
                # Add high-frequency quantization grit to breakpoints
                delta += 0.08 * np.sign(math.sin(y * 32.0))
            bp_amps[k] += delta
            # Elastic boundaries
            if bp_amps[k] > 0.95:
                bp_amps[k] = 0.95 - (bp_amps[k] - 0.95)
            elif bp_amps[k] < -0.95:
                bp_amps[k] = -0.95 - (bp_amps[k] + 0.95)
                
            bp_lens[k] = max(0.015, bp_lens[k] + 0.035 * math.cos(y * (k + 1)))
            
        total_len = np.sum(bp_lens)
        cycle_lens = (bp_lens / total_len) * base_period
        cycle_samples_total = int(round(np.sum(cycle_lens)))
        if cycle_samples_total <= 0:
            cycle_samples_total = int(base_period)
            
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
                
        # Write drone cycle
        remain = total_samples - sample_idx
        write_len = min(len(cycle_buf), remain)
        stratum_drone[sample_idx:sample_idx + write_len] = cycle_buf[:write_len]
        
        # If in quantization zone, inject granular spark crackle into fracture stratum
        if in_quant_zone:
            grit = np.random.uniform(-0.35, 0.35, write_len) * np.abs(cycle_buf[:write_len])
            stratum_fracture[sample_idx:sample_idx + write_len] += grit.astype(np.float32)
            
        # Synthesize sub-bass mantle: low frequency sine oscillator modulated by attractor radius
        t_arr = np.linspace(sample_idx / sample_rate, (sample_idx + write_len) / sample_rate, write_len)
        sub_freq = 42.0 + 12.0 * math.sin(radius * 2.0)
        stratum_mantle[sample_idx:sample_idx + write_len] = 0.55 * np.sin(2.0 * np.pi * sub_freq * t_arr)
        
        sample_idx += write_len
        cycle_count += 1
        
    print(f"Base strata generated across {cycle_count} cycles. Injecting episodic fault ruptures...")
    
    # Inject seismic fault slip impacts at specified fault times
    for fs in fault_samples:
        if fs < total_samples - 88200:
            # Impact 1: Seismic Sub-Bass Compression Wave (exponential decay 55Hz -> 25Hz)
            impact_len = int(1.8 * sample_rate)
            t_imp = np.linspace(0, 1.8, impact_len)
            freq_curve = 55.0 * np.exp(-t_imp * 3.5) + 24.0
            phase = np.cumsum(2.0 * np.pi * freq_curve / sample_rate)
            seismic_env = np.exp(-t_imp * 2.2)
            seismic_wave = np.sin(phase) * seismic_env * 0.95
            
            # Impact 2: Granular Memory Dislocation (spark burst)
            burst_len = int(0.12 * sample_rate)
            burst = np.random.uniform(-0.8, 0.8, burst_len) * np.linspace(1.0, 0.0, burst_len)**2
            
            stratum_mantle[fs:fs + impact_len] += seismic_wave[:min(impact_len, total_samples - fs)]
            stratum_fracture[fs:fs + burst_len] += burst[:min(burst_len, total_samples - fs)]
            
            # Attenuate the drone temporarily right at impact (acoustic shockwave choke)
            choke_len = int(0.25 * sample_rate)
            choke_env = np.linspace(0.1, 1.0, choke_len)
            stratum_drone[fs:fs + choke_len] *= choke_env
            
    print("Synthesizing stereo master and spatial acoustic field...")
    
    # Master mixdown
    mono_mix = stratum_drone * 0.65 + stratum_mantle * 0.55 + stratum_fracture * 0.45
    
    # Soft non-linear saturation to give physical analog warmth and prevent harsh clipping
    saturated = np.tanh(mono_mix * 1.25)
    
    # Stereo spatialization
    # Left channel: Direct saturated mix
    # Right channel: Delayed by 38ms with inverted high-frequency fracture for wide stereo rift
    left_chan = saturated
    delay_samp = int(0.038 * sample_rate)
    right_chan = np.zeros_like(left_chan)
    right_chan[delay_samp:] = (
        stratum_drone[:-delay_samp] * 0.65 + 
        stratum_mantle[:-delay_samp] * 0.55 - 
        stratum_fracture[:-delay_samp] * 0.40
    )
    right_chan = np.tanh(right_chan * 1.25)
    
    # Envelope fade
    fade_len = int(2.0 * sample_rate)
    fade_in = np.linspace(0.0, 1.0, fade_len)
    fade_out = np.linspace(1.0, 0.0, fade_len * 2)
    
    left_chan[:fade_len] *= fade_in
    right_chan[:fade_len] *= fade_in
    left_chan[-len(fade_out):] *= fade_out
    right_chan[-len(fade_out):] *= fade_out
    
    # Normalize to -0.5 dB peak
    peak = max(np.max(np.abs(left_chan)), np.max(np.abs(right_chan)))
    if peak > 0:
        left_chan = (left_chan / peak) * 0.94
        right_chan = (right_chan / peak) * 0.94
        
    with wave.open(out_wav, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        
        interleaved = np.empty(total_samples * 2, dtype=np.int16)
        interleaved[0::2] = (left_chan * 32767).astype(np.int16)
        interleaved[1::2] = (right_chan * 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())
        
    print(f"Study 007 successfully rendered and exported to {out_wav}!")

if __name__ == "__main__":
    generate_sonified_rupture()
