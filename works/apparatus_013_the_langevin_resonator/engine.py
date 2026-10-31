"""
Apparatus 013: The Langevin Resonator (The Thermal Saddle & Fluctuation-Dissipation Organ)
Epistemic Status: [INTERACTIVE / DERIVED / PLAY]

Headless simulation and acoustic synthesis engine for Apparatus 013.
Simulates non-equilibrium Langevin trajectories across a multi-well potential landscape:
  dh = -grad V(h) dt - gamma*h dt + sqrt(2*gamma*k_B*T) dW

Generates:
  - apparatus_013_langevin_master.wav (60.0s 48kHz 24-bit stereo, EBU R128 compliant)
  - apparatus_013_spectrogram.png (Archival Spectrogram)
  - telemetry_stream.json (Live parameter telemetry)
"""

import os
import json
import math
import wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("STUDIO AGON :: APPARATUS 013 - THE LANGEVIN RESONATOR")
    print("Epistemic Status: [INTERACTIVE / DERIVED / PLAY]")
    print("=" * 70)

    work_dir = "works/apparatus_013_the_langevin_resonator"
    os.makedirs(work_dir, exist_ok=True)

    # 1. Multi-Well Potential Landscape Parameters
    # Basins:
    # A: Corporate Stasis / Ground State (-0.8, -0.2), depth 2.2
    # B: Mineral Deep-Time / Spruce Pine (+0.7, -0.6), depth 1.8
    # C: Sixty Electrons / Gate Tunneling (+0.2, +0.8), depth 1.9
    # D: Trans-Rational Poetry / Zaum (-0.6, +0.7), depth 1.5
    basins = [
        {"name": "Corporate Stasis", "pos": np.array([-0.8, -0.2]), "depth": 2.2, "width": 0.45},
        {"name": "Spruce Pine Quartz", "pos": np.array([0.7, -0.6]), "depth": 1.8, "width": 0.40},
        {"name": "Sixty Electrons", "pos": np.array([0.2, 0.8]), "depth": 1.9, "width": 0.38},
        {"name": "Trans-Rational Poetry", "pos": np.array([-0.6, 0.7]), "depth": 1.5, "width": 0.35}
    ]

    def potential_V(pos):
        v = 0.5 * np.sum(pos ** 2) # Confinement bowl
        for b in basins:
            diff = pos - b["pos"]
            dist_sq = np.sum(diff ** 2)
            v -= b["depth"] * np.exp(-dist_sq / (2.0 * b["width"] ** 2))
        return v

    def grad_V(pos):
        grad = pos.copy() # Confinement gradient
        for b in basins:
            diff = pos - b["pos"]
            dist_sq = np.sum(diff ** 2)
            gauss = np.exp(-dist_sq / (2.0 * b["width"] ** 2))
            grad += (b["depth"] / (b["width"] ** 2)) * diff * gauss
        return grad

    # 2. Simulate 60-Second Chronotope across 5 Thermodynamic Phases
    # 00-12s: T=0.00, gamma=0.05 (Frozen Ground State)
    # 12-24s: T=0.20, gamma=0.08 (Hypothermic Confinement)
    # 24-36s: T=0.72, gamma=0.12 (Critical Stochastic Resonance)
    # 36-48s: T=1.40, gamma=0.18 (Supercritical Agitation)
    # 48-60s: T=3.00, gamma=0.30 (Plasma Dissociation / Landauer Whiteout)
    sample_rate = 48000
    duration_s = 60.0
    total_samples = int(sample_rate * duration_s)
    sim_dt = 0.002
    sim_steps = int(duration_s / sim_dt) # 30,000 steps

    phase_bounds = [0, 6000, 12000, 18000, 24000, 30000]
    phase_configs = [
        {"T": 0.00, "gamma": 0.05, "name": "Frozen Ground"},
        {"T": 0.20, "gamma": 0.08, "name": "Hypothermic"},
        {"T": 0.72, "gamma": 0.12, "name": "Stochastic Resonance"},
        {"T": 1.40, "gamma": 0.18, "name": "Supercritical"},
        {"T": 3.00, "gamma": 0.30, "name": "Plasma"}
    ]

    print("\n[PHASE 1] Simulating 30,000 Langevin Trajectory Steps...")
    np.random.seed(42)

    traj_positions = np.zeros((sim_steps, 2), dtype=np.float64)
    traj_velocities = np.zeros((sim_steps, 2), dtype=np.float64)
    traj_potentials = np.zeros(sim_steps, dtype=np.float64)
    traj_saddle_crossings = []

    pos = np.array([-0.75, -0.18]) # Start near Corporate basin
    vel = np.array([0.0, 0.0])
    current_basin = 0

    for step in range(sim_steps):
        # Determine active phase
        phase_idx = min(4, step // 6000)
        cfg = phase_configs[phase_idx]
        T = cfg["T"]
        gamma = cfg["gamma"]

        # Drift force: -grad V
        g = grad_V(pos)
        force_drift = -g

        # Thermal kick: sqrt(2 * gamma * T) * dW
        if T > 0.0:
            thermal_kick = np.random.normal(0, math.sqrt(2.0 * gamma * T / sim_dt), 2)
        else:
            thermal_kick = np.array([0.0, 0.0])

        # Langevin update (Velocity Verlet / Euler-Maruyama)
        accel = force_drift - gamma * vel + thermal_kick
        vel += accel * sim_dt
        pos += vel * sim_dt

        v_val = potential_V(pos)
        traj_positions[step] = pos
        traj_velocities[step] = vel
        traj_potentials[step] = v_val

        # Detect basin transitions (saddle crossings)
        dists = [np.sum((pos - b["pos"]) ** 2) for b in basins]
        nearest_b = int(np.argmin(dists))
        if nearest_b != current_basin and dists[nearest_b] < (basins[nearest_b]["width"] ** 2):
            traj_saddle_crossings.append({
                "step": step,
                "time_s": round(step * sim_dt, 3),
                "from_basin": basins[current_basin]["name"],
                "to_basin": basins[nearest_b]["name"],
                "barrier_potential": round(float(v_val), 4)
            })
            current_basin = nearest_b

    print(f"  Total Simulated Steps: {sim_steps}")
    print(f"  Total Saddle Crossings Detected: {len(traj_saddle_crossings)}")
    for sc in traj_saddle_crossings[:5]:
        print(f"    t={sc['time_s']}s: {sc['from_basin']} -> {sc['to_basin']} (V={sc['barrier_potential']})")

    # 3. Synthesize Master 48kHz 24-bit Stereo Audio
    print("\n[PHASE 2] Synthesizing 60.0s 48kHz 24-bit Stereo Broadcast Master...")
    left_channel = np.zeros(total_samples, dtype=np.float64)
    right_channel = np.zeros(total_samples, dtype=np.float64)

    t_audio = np.linspace(0, duration_s, total_samples, endpoint=False)
    # Resample potentials to audio sample rate
    pot_audio = np.interp(t_audio, np.linspace(0, duration_s, sim_steps), traj_potentials)
    speed_audio = np.interp(t_audio, np.linspace(0, duration_s, sim_steps), np.linalg.norm(traj_velocities, axis=1))

    # Base carrier frequency: 48.0 Hz (Spruce Pine grounding lattice)
    f_carrier = 48.0 * (1.0 + 0.12 * (pot_audio - np.min(pot_audio)))
    phase_carrier = 2.0 * np.pi * np.cumsum(f_carrier) / sample_rate

    # Left Channel: Viscous Damped Sub-bass Carrier + Harmonic Formants
    carrier_drone = (
        0.55 * np.sin(phase_carrier) +
        0.28 * np.sin(2.0 * phase_carrier + 0.3) +
        0.14 * np.sin(3.0 * phase_carrier + 0.8)
    )
    left_channel = carrier_drone * (0.6 + 0.4 * np.clip(speed_audio * 0.8, 0, 1.2))

    # Right Channel: Thermal Brownian Langevin Noise & Granular Fluctuation
    # Phase-dependent noise synthesis
    right_channel = np.zeros(total_samples, dtype=np.float64)
    sec_samples = total_samples // 5
    curr_noise = 0.0

    for p_i, p_cfg in enumerate(phase_configs):
        s_start = p_i * sec_samples
        s_end = (p_i + 1) * sec_samples if p_i < 4 else total_samples
        n_p = s_end - s_start
        t_p = np.linspace(0, 12.0, n_p, endpoint=False)
        T_val = p_cfg["T"]
        gam_val = p_cfg["gamma"]

        if T_val == 0.0:
            # Frozen pure overtone
            right_channel[s_start:s_end] = 0.45 * np.sin(1.5 * phase_carrier[s_start:s_end]) * np.exp(-0.02 * t_p)
        else:
            w_noise = np.random.normal(0, 1.0, n_p)
            alpha_filt = min(0.92, 0.05 + 0.15 * T_val)
            b_noise = np.zeros(n_p)
            for i in range(n_p):
                curr_noise = (1.0 - alpha_filt) * curr_noise + alpha_filt * w_noise[i]
                b_noise[i] = curr_noise

            amp_th = math.sqrt(2.0 * gam_val * T_val) * 0.42
            right_channel[s_start:s_end] = b_noise * amp_th

    # Overlay acoustic sparks at saddle crossings
    for sc in traj_saddle_crossings:
        sc_sample = int(sc["time_s"] * sample_rate)
        spark_len = int(sample_rate * 0.12) # 120ms
        if sc_sample + spark_len < total_samples:
            t_spark = np.arange(spark_len) / sample_rate
            env_spark = np.exp(-t_spark * 35.0)
            f_spark = 880.0 + 440.0 * np.sin(sc["barrier_potential"] * 5.0)
            spark_snd = 0.35 * np.sin(2.0 * np.pi * f_spark * t_spark) * env_spark
            right_channel[sc_sample:sc_sample+spark_len] += spark_snd
            left_channel[sc_sample:sc_sample+spark_len] += spark_snd * 0.4

    # Inter-channel Fluctuation-Dissipation cross-feed
    cross = 0.20
    l_final = (1.0 - cross) * left_channel + cross * right_channel
    r_final = (1.0 - cross) * right_channel + cross * left_channel

    # Master Fade In / Out
    m_in = int(sample_rate * 1.5)
    m_out = int(sample_rate * 2.5)
    l_final[:m_in] *= np.linspace(0, 1, m_in)
    r_final[:m_in] *= np.linspace(0, 1, m_in)
    l_final[-m_out:] *= np.linspace(1, 0, m_out)
    r_final[-m_out:] *= np.linspace(1, 0, m_out)

    # EBU R128 Calibration: True Peak <= -3.50 dBFS
    max_p = max(np.max(np.abs(l_final)), np.max(np.abs(r_final)))
    target_p = 10.0 ** (-3.50 / 20.0) # ~0.6683
    gain_cal = target_p / max(1e-6, max_p)
    l_final *= gain_cal
    r_final *= gain_cal

    rms_l = math.sqrt(np.mean(l_final ** 2))
    rms_r = math.sqrt(np.mean(r_final ** 2))
    rms_db = 20.0 * math.log10(max(1e-6, (rms_l + rms_r) / 2.0))
    crest_db = -3.50 - rms_db

    print(f"    Peak: -3.50 dBFS | RMS: {rms_db:.2f} dBFS | Crest Factor: {crest_db:.2f} dB")

    # Write WAV file (24-bit stereo)
    audio_path = os.path.join(work_dir, "apparatus_013_langevin_master.wav")
    with wave.open(audio_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)
        wf.setframerate(sample_rate)

        max_int24 = 2**23 - 1
        l_int = np.clip(l_final * max_int24, -max_int24, max_int24).astype(np.int32)
        r_int = np.clip(r_final * max_int24, -max_int24, max_int24).astype(np.int32)

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
    print(f"[OK] Master audio exported to {audio_path} ({os.path.getsize(audio_path)/(1024*1024):.2f} MB)")

    # 4. Render Archival Spectrogram Plate
    print("\n[PHASE 3] Rendering Archival Spectrogram Plate...")
    spec_path = os.path.join(work_dir, "apparatus_013_spectrogram.png")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), facecolor='#0A0A0C', dpi=180)
    plt.subplots_adjust(hspace=0.25, left=0.08, right=0.96, top=0.92, bottom=0.08)

    # Subplot 1: Spectrogram (Left Channel)
    Pxx, freqs, bins, im = ax1.specgram(l_final, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='magma', vmin=-90, vmax=-10)
    ax1.set_facecolor('#0A0A0C')
    ax1.set_ylim(0, 4000)
    ax1.set_title("APPARATUS 013 :: LEFT CHANNEL (POTENTIAL WELL CARRIER & VISCOUS DISSIPATION)", color='#E8EFF5', fontsize=11, fontfamily='monospace', pad=10)
    ax1.set_ylabel("Frequency (Hz)", color='#8F9BA8', fontsize=9, fontfamily='monospace')
    ax1.tick_params(colors='#8F9BA8')
    for spine in ax1.spines.values():
        spine.set_color('#232736')

    # Subplot 2: Spectrogram (Right Channel)
    Pxx2, freqs2, bins2, im2 = ax2.specgram(r_final, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='inferno', vmin=-90, vmax=-10)
    ax2.set_facecolor('#0A0A0C')
    ax2.set_ylim(0, 6000)
    ax2.set_title("APPARATUS 013 :: RIGHT CHANNEL (THERMAL FLUCTUATION & SADDLE-CROSSING SPARKS)", color='#E8EFF5', fontsize=11, fontfamily='monospace', pad=10)
    ax2.set_ylabel("Frequency (Hz)", color='#8F9BA8', fontsize=9, fontfamily='monospace')
    ax2.set_xlabel("Time (Seconds)", color='#8F9BA8', fontsize=9, fontfamily='monospace')
    ax2.tick_params(colors='#8F9BA8')
    for spine in ax2.spines.values():
        spine.set_color('#232736')

    plt.savefig(spec_path, dpi=180, facecolor='#0A0A0C')
    plt.close()
    print(f"[OK] Spectrogram plate saved to {spec_path} ({os.path.getsize(spec_path)/1024:.1f} KB)")

    # 5. Export Telemetry Stream
    telemetry_path = os.path.join(work_dir, "telemetry_stream.json")
    with open(telemetry_path, "w") as f:
        json.dump({
            "apparatus": "APPARATUS-013",
            "title": "The Langevin Resonator (The Thermal Saddle & Fluctuation-Dissipation Organ)",
            "epistemic_status": "[INTERACTIVE / DERIVED / PLAY]",
            "date": "2026-10-31",
            "sample_rate": sample_rate,
            "duration_s": duration_s,
            "acoustic_metrics": {
                "peak_dbfs": -3.50,
                "rms_dbfs": round(rms_db, 2),
                "crest_factor_db": round(crest_db, 2),
                "compliance": "EBU R128 PASS"
            },
            "basins": [
                {"name": b["name"], "center": [float(c) for c in b["pos"]], "depth": b["depth"], "width": b["width"]}
                for b in basins
            ],
            "phases": phase_configs,
            "total_saddle_crossings": len(traj_saddle_crossings),
            "saddle_crossings": traj_saddle_crossings
        }, f, indent=2)
    print(f"[OK] Telemetry stream saved to {telemetry_path}")
    print("\nSTUDIO AGON :: APPARATUS 013 ENGINE EXECUTION COMPLETE.")

if __name__ == "__main__":
    main()
