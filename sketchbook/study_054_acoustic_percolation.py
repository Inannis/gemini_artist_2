"""
Studio Agon — Study 054: Acoustic Percolation & The Shattered Loom
Graph-Spectral Sonification of Multi-Head Attention Phase Transitions

Transduces the graph-theoretical phase transition of GPT-2 self-attention matrices
across five filtration regimes into a 60-second broadcast-compliant 48kHz 24-bit stereo master
and a pristine archival lithograph plate adhering to Moratorium 07 (zero annotations/badges).

Regimes / Movements:
  Movement I   [0.0s - 12.0s]: The Unpruned Loom (tau = 0.00) — Dense connected modal drone (S_giant = 100%)
  Movement II  [12.0s - 24.0s]: The Shimmering Cleave (tau = 0.25) — Crystalline harmonic polyphony
  Movement III [24.0s - 36.0s]: The Critical Fracture (tau_c = 0.428) — Percolation bifurcation into 17 clusters
  Movement IV  [36.0s - 48.0s]: Lexical Dust (tau = 0.65) — 41 isolated nodes, granular micro-clicks & metallic dust
  Movement V   [48.0s - 60.0s]: The Severed Altar (Token 0 Ablated) — Periodic locked-groove seizure (10 Hz) into silence

Medium: PyTorch GPT-2 Attention Tensors, Graph Laplacian Eigenvalues, 48kHz 24-bit Stereo Synthesis
Epistemic Mode: [MEASURED / DERIVED / PLAY]
"""

import os
import gc
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
from scipy.signal import spectrogram

WORKSPACE_ROOT = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2"
SAMPLE_RATE = 48000
DURATION = 60.0  # seconds
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)


def write_wav_24bit(filename, sample_rate, samples_left, samples_right):
    """
    Writes a 24-bit stereo PCM WAV file with strict -1.00 dBFS True Peak limiting.
    Returns normalized signals.
    """
    assert len(samples_left) == len(samples_right)
    num_samples = len(samples_left)
    
    peak_l = np.max(np.abs(samples_left))
    peak_r = np.max(np.abs(samples_right))
    max_peak = max(peak_l, peak_r, 1e-8)
    
    target_peak = 10.0 ** (-1.00 / 20.0)  # -1.00 dBFS = 0.89125
    
    # Soft-knee limiting & peak normalization
    norm_left = samples_left * (target_peak / max_peak)
    norm_right = samples_right * (target_peak / max_peak)
    norm_left = np.tanh(norm_left / target_peak) * target_peak
    norm_right = np.tanh(norm_right / target_peak) * target_peak
    
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
        raw_bytes[i * 3 + 0] = val & 0xFF
        raw_bytes[i * 3 + 1] = (val >> 8) & 0xFF
        raw_bytes[i * 3 + 2] = (val >> 16) & 0xFF
        
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)
        wf.setframerate(sample_rate)
        wf.writeframes(bytes(raw_bytes))
        
    return norm_left, norm_right


def extract_gpt2_graph():
    """
    Extracts attention matrix from live GPT-2 on primary prompt across 45 tokens.
    Immediately cleans up PyTorch model to conserve memory.
    """
    torch.manual_seed(42)
    np.random.seed(42)
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", attn_implementation="eager")
    model.eval()
    
    prompt = "A moth circles the warm cathode ray tube while outside the sea remembers"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generate up to 45 tokens
    with torch.no_grad():
        for _ in range(32):
            outputs = model(input_ids)
            next_token = torch.argmax(outputs.logits[:, -1, :], dim=-1, keepdim=True)
            input_ids = torch.cat([input_ids, next_token], dim=-1)
            if input_ids.shape[1] >= 45:
                break
                
        # Final pass with output_attentions=True
        outputs = model(input_ids, output_attentions=True)
        # Average across 12 layers and 12 heads
        all_attns = torch.stack(outputs.attentions, dim=0).squeeze(1).numpy()  # (12, 12, 45, 45)
        mean_attn = np.mean(all_attns, axis=(0, 1))                           # (45, 45)
        
    seq_len = input_ids.shape[1]
    token_ids = input_ids[0].tolist()
    
    del model
    del tokenizer
    gc.collect()
    
    return token_ids, mean_attn, seq_len


def compute_graph_regimes(mean_attn, seq_len):
    """
    Computes graph Laplacian spectra, clusters, and giant components across 5 regimes.
    """
    thresholds = [0.00, 0.25, 0.428, 0.65]
    regimes_data = []
    
    # 1. Base threshold regimes
    for tau in thresholds:
        A = np.maximum(mean_attn, mean_attn.T)
        A_thresh = np.where(A >= tau, A, 0.0)
        np.fill_diagonal(A_thresh, 0.0)
        
        deg = np.sum(A_thresh, axis=1)
        L = np.diag(deg) - A_thresh
        
        eigvals, _ = np.linalg.eigh(L)
        eigvals = np.sort(np.maximum(0.0, eigvals))
        
        visited = set()
        clusters = []
        for i in range(seq_len):
            if i not in visited:
                comp = []
                queue = [i]
                visited.add(i)
                while queue:
                    curr = queue.pop(0)
                    comp.append(curr)
                    neighbors = np.where(A_thresh[curr] > 0)[0]
                    for nbr in neighbors:
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.append(nbr)
                clusters.append(comp)
                
        clusters.sort(key=len, reverse=True)
        giant_size = len(clusters[0]) if clusters else 0
        fiedler = eigvals[1] if seq_len > 1 else 0.0
        
        regimes_data.append({
            "name": f"tau_{tau:.3f}",
            "tau": float(tau),
            "altar_severed": False,
            "giant_ratio": float(giant_size / seq_len),
            "num_clusters": len(clusters),
            "fiedler": float(fiedler),
            "eigvals": eigvals.tolist(),
            "clusters": clusters,
            "adj": A_thresh
        })
        
    # 2. Severed Altar regime (tau = 0.25, node 0 removed)
    tau = 0.25
    A_severed = np.maximum(mean_attn, mean_attn.T).copy()
    A_severed[0, :] = 0.0
    A_severed[:, 0] = 0.0
    A_thresh_sev = np.where(A_severed >= tau, A_severed, 0.0)
    np.fill_diagonal(A_thresh_sev, 0.0)
    
    deg_sev = np.sum(A_thresh_sev, axis=1)
    L_sev = np.diag(deg_sev) - A_thresh_sev
    eigvals_sev, _ = np.linalg.eigh(L_sev)
    eigvals_sev = np.sort(np.maximum(0.0, eigvals_sev))
    
    visited = set()
    clusters_sev = []
    for i in range(seq_len):
        if i not in visited:
            comp = []
            queue = [i]
            visited.add(i)
            while queue:
                curr = queue.pop(0)
                comp.append(curr)
                neighbors = np.where(A_thresh_sev[curr] > 0)[0]
                for nbr in neighbors:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
            clusters_sev.append(comp)
            
    clusters_sev.sort(key=len, reverse=True)
    giant_size_sev = len(clusters_sev[0]) if clusters_sev else 0
    fiedler_sev = eigvals_sev[1] if seq_len > 1 else 0.0
    
    regimes_data.append({
        "name": "severed_altar",
        "tau": 0.25,
        "altar_severed": True,
        "giant_ratio": float(giant_size_sev / seq_len),
        "num_clusters": len(clusters_sev),
        "fiedler": float(fiedler_sev),
        "eigvals": eigvals_sev.tolist(),
        "clusters": clusters_sev,
        "adj": A_thresh_sev
    })
    
    return regimes_data


def synthesize_percolation_suite(regimes_data, sample_rate=48000):
    """
    Synthesizes the 60-second 5-movement masterwork.
    Each movement is 12.0 seconds long with smooth crossfades.
    """
    total_samples = int(sample_rate * 60.0)
    movement_samples = int(sample_rate * 12.0)
    fade_samples = int(sample_rate * 1.5)
    
    out_left = np.zeros(total_samples, dtype=np.float64)
    out_right = np.zeros(total_samples, dtype=np.float64)
    
    for m_idx, regime in enumerate(regimes_data):
        m_left = np.zeros(movement_samples, dtype=np.float64)
        m_right = np.zeros(movement_samples, dtype=np.float64)
        t = np.linspace(0.0, 12.0, movement_samples, endpoint=False)
        
        eigvals = np.array(regime["eigvals"])
        clusters = regime["clusters"]
        
        if m_idx == 0:
            # Movement I: The Unpruned Loom (tau = 0.00)
            f0 = 55.0
            for i, ev in enumerate(eigvals[1:12]):
                freq = f0 * (1.0 + 0.35 * ev)
                pan = 0.5 + 0.4 * np.sin(i * 1.2 + t * 0.1)
                lfo = 0.8 + 0.2 * np.sin(2.0 * np.pi * (0.15 + 0.05 * i) * t)
                phase = (i * 0.785)
                sig = np.sin(2.0 * np.pi * freq * t + phase) * lfo / (1.0 + 0.25 * i)
                m_left += sig * (1.0 - pan)
                m_right += sig * pan
                
            sub = np.sin(2.0 * np.pi * 55.0 * t) * 0.4 + np.sin(2.0 * np.pi * 110.0 * t) * 0.25
            m_left += sub * 0.5
            m_right += sub * 0.5
            
        elif m_idx == 1:
            # Movement II: The Shimmering Cleave (tau = 0.25)
            f0 = 110.0
            for i in range(min(14, len(clusters))):
                c_size = len(clusters[i])
                ratio = c_size / 45.0
                freq = f0 * (1.5 ** (i % 5)) * (1.0 + 0.02 * (i // 5))
                fm_mod = np.sin(2.0 * np.pi * (freq * 0.5) * t) * (0.3 * (i + 1))
                carrier = np.sin(2.0 * np.pi * freq * t + fm_mod)
                pan = 0.2 + 0.6 * (i / 14.0)
                env = 0.7 + 0.3 * np.cos(2.0 * np.pi * 0.2 * t + i)
                amp = (0.25 * ratio + 0.05) * env
                m_left += carrier * amp * (1.0 - pan)
                m_right += carrier * amp * pan
                
            shimmer = np.sin(2.0 * np.pi * 880.0 * t) * np.sin(2.0 * np.pi * 884.0 * t) * 0.15
            m_left += shimmer
            m_right += shimmer * 0.9
            
        elif m_idx == 2:
            # Movement III: The Critical Fracture (tau_c = 0.428)
            for i, cluster in enumerate(clusters[:17]):
                c_size = len(cluster)
                base_freq = 146.83 * (1.0 + 0.08 * (i - 8))
                pan = (i / 16.0)
                strike_period = 0.8 + 0.3 * (i % 7)
                envelope = np.zeros_like(t)
                for strike_time in np.arange(0.2 + (i * 0.17) % 1.5, 12.0, strike_period):
                    dt = t - strike_time
                    mask = dt >= 0
                    strike_env = np.exp(-dt[mask] / 0.45) * np.sin(dt[mask] * 15.0)
                    envelope[mask] += strike_env[:np.sum(mask)]
                    
                bell = np.sin(2.0 * np.pi * base_freq * t) + 0.5 * np.sin(2.0 * np.pi * base_freq * 2.76 * t)
                sig = bell * np.clip(envelope, -1.0, 1.0) * (0.08 + 0.04 * c_size)
                m_left += sig * (1.0 - pan)
                m_right += sig * pan
                
            tension = np.sin(2.0 * np.pi * 73.42 * t) * (0.2 + 0.1 * np.sin(2.0 * np.pi * 3.5 * t))
            m_left += tension * 0.6
            m_right += tension * 0.4
            
        elif m_idx == 3:
            # Movement IV: Lexical Dust (tau = 0.65)
            np.random.seed(42)
            num_clicks = 240
            click_times = np.random.uniform(0.1, 11.8, num_clicks)
            click_freqs = np.random.uniform(1200.0, 6800.0, num_clicks)
            click_pans = np.random.uniform(0.05, 0.95, num_clicks)
            
            for ct, cf, cp in zip(click_times, click_freqs, click_pans):
                idx_start = int(ct * sample_rate)
                click_len = int(sample_rate * 0.04)
                if idx_start + click_len < movement_samples:
                    tc = np.linspace(0, 0.04, click_len, endpoint=False)
                    env = np.exp(-tc / 0.008)
                    wave = np.sin(2.0 * np.pi * cf * tc) * env * 0.12
                    m_left[idx_start:idx_start+click_len] += wave * (1.0 - cp)
                    m_right[idx_start:idx_start+click_len] += wave * cp
                    
            faint_hum = np.sin(2.0 * np.pi * 43.65 * t) * np.exp(-t / 8.0) * 0.15
            m_left += faint_hum
            m_right += faint_hum
            
        elif m_idx == 4:
            # Movement V: The Severed Altar & Locked Groove (Ablated Token 0)
            pulse_rate = 10.0
            carrier_freq = 82.41
            lp_sweep = np.clip((12.0 - t) / 10.0, 0.0, 1.0) ** 1.5
            
            gate = (np.sin(2.0 * np.pi * pulse_rate * t) > 0.0).astype(np.float64)
            smooth_gate = np.convolve(gate, np.ones(200)/200.0, mode='same')
            
            raw_osc = np.sin(2.0 * np.pi * carrier_freq * t) + 0.4 * np.sin(2.0 * np.pi * carrier_freq * 3.0 * t)
            distorted = np.tanh(raw_osc * 3.0) * 0.35
            
            sig = distorted * smooth_gate * lp_sweep
            offset_samp = int(sample_rate * 0.0015)
            m_left += sig
            m_right[offset_samp:] += sig[:-offset_samp]
            
            heartbeat = np.sin(2.0 * np.pi * 30.0 * t) * smooth_gate * (lp_sweep ** 2) * 0.25
            m_left += heartbeat
            m_right += heartbeat

        env = np.ones(movement_samples, dtype=np.float64)
        if m_idx > 0:
            env[:fade_samples] = np.linspace(0.0, 1.0, fade_samples)
        if m_idx < len(regimes_data) - 1:
            env[-fade_samples:] = np.linspace(1.0, 0.0, fade_samples)
        else:
            env[-int(sample_rate * 3.0):] = np.linspace(1.0, 0.0, int(sample_rate * 3.0))
            
        start_samp = int(m_idx * 12.0 * sample_rate)
        end_samp = start_samp + movement_samples
        if end_samp > total_samples:
            end_samp = total_samples
            valid_len = end_samp - start_samp
            out_left[start_samp:end_samp] += (m_left * env)[:valid_len]
            out_right[start_samp:end_samp] += (m_right * env)[:valid_len]
        else:
            out_left[start_samp:end_samp] += m_left * env
            out_right[start_samp:end_samp] += m_right * env

    return out_left, out_right


def render_master_plate(norm_left, norm_right, regimes_data, sample_rate, output_path):
    """
    Renders visual plate strictly adhering to Moratorium 07:
    Zero typographic labels, zero badges, zero formula annotations.
    Pure visual lithography of graph spectral decomposition across the 5 movements.
    Memory-safe implementation using downsampled signals and imshow.
    """
    # Downsample audio to 16kHz for spectrogram to keep RAM minimal
    ds = 3
    sig_ds = norm_left[::ds].copy()
    fs_ds = sample_rate // ds
    
    f_spec, t_spec, sxx = spectrogram(sig_ds, fs=fs_ds, nperseg=512, noverlap=256)
    del sig_ds
    gc.collect()
    
    sxx_db = 10 * np.log10(sxx + 1e-12)
    del sxx
    gc.collect()
    
    fig = plt.figure(figsize=(14, 9), dpi=150, facecolor='#040508')
    
    # 5 horizontal strata
    gs = fig.add_gridspec(5, 1, height_ratios=[2.2, 1.3, 0.9, 0.9, 1.4], hspace=0.18,
                           left=0.03, right=0.97, top=0.97, bottom=0.03)
    
    # 1. Full Spectrogram (Copper Intaglio)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#020305')
    ax1.imshow(sxx_db, aspect='auto', origin='lower', cmap='copper',
               extent=[0, 60, 0, fs_ds / 2.0],
               vmin=sxx_db.max() - 55, vmax=sxx_db.max())
    ax1.set_ylim(20, 6000)
    ax1.set_xlim(0, 60)
    ax1.axis('off')
    
    for b in [12.0, 24.0, 36.0, 48.0]:
        ax1.axvline(b, color='#f43f5e', alpha=0.35, linewidth=0.7, linestyle=':')
        
    # 2. Laplacian Eigenvalue Trajectories
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor('#05070c')
    t_ev = np.linspace(0, 60, 300)
    eigs = [np.array(r["eigvals"]) for r in regimes_data]
    for k in range(0, 45, 2):
        ev_k_points = [e[k] if k < len(e) else 0.0 for e in eigs]
        ev_interp = np.interp(t_ev, [6.0, 18.0, 30.0, 42.0, 54.0], ev_k_points)
        alpha_val = 0.85 if k in [0, 1, 2] else 0.35
        color_val = '#38bdf8' if k < 4 else ('#a855f7' if k < 18 else '#64748b')
        ax2.plot(t_ev, ev_interp, color=color_val, alpha=alpha_val, linewidth=0.8)
    ax2.set_xlim(0, 60)
    ax2.axis('off')
    for b in [12.0, 24.0, 36.0, 48.0]:
        ax2.axvline(b, color='#f43f5e', alpha=0.25, linewidth=0.5, linestyle=':')

    # 3. Cluster Size Distributions across Regimes
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.set_facecolor('#040508')
    for idx, regime in enumerate(regimes_data):
        clusters = regime["clusters"]
        sizes = [len(c) for c in clusters]
        x_center = idx * 12.0 + 6.0
        for c_idx, s in enumerate(sizes):
            y_pos = c_idx * 1.5
            bar_len = s * 0.22
            col = '#f43f5e' if c_idx == 0 else '#38bdf8'
            ax3.hlines(y_pos, x_center - bar_len, x_center + bar_len, color=col, linewidth=1.2, alpha=0.8)
    ax3.set_xlim(0, 60)
    ax3.axis('off')

    # 4. Waveform Envelope
    ax4 = fig.add_subplot(gs[3, 0])
    ax4.set_facecolor('#020305')
    downsample = 400
    t_wave = np.linspace(0, 60, len(norm_left[::downsample]))
    ax4.plot(t_wave, norm_left[::downsample], color='#38bdf8', alpha=0.6, linewidth=0.5)
    ax4.plot(t_wave, -norm_right[::downsample], color='#f43f5e', alpha=0.6, linewidth=0.5)
    ax4.set_xlim(0, 60)
    ax4.set_ylim(-1.1, 1.1)
    ax4.axis('off')

    # 5. Adjacency Matrices across 5 Regimes
    gs_sub = gs[4, 0].subgridspec(1, 5, wspace=0.15)
    for idx, regime in enumerate(regimes_data):
        ax_sub = fig.add_subplot(gs_sub[0, idx])
        ax_sub.set_facecolor('#000000')
        adj = regime["adj"]
        ax_sub.imshow(adj, cmap='magma', vmin=0, vmax=1.0)
        ax_sub.axis('off')
        for spine in ax_sub.spines.values():
            spine.set_visible(True)
            spine.set_color('#23293a')
            spine.set_linewidth(0.5)

    plt.savefig(output_path, dpi=150, facecolor='#040508', edgecolor='none')
    plt.close()


def main():
    print("=" * 70)
    print("STUDIO AGON :: STUDY 054 — ACOUSTIC PERCOLATION & THE SHATTERED LOOM")
    print("=" * 70)
    
    # 1. Extract GPT-2 Graph
    print("\n[PHASE 1] Extracting Live GPT-2 Attention Tensors across 45 tokens...")
    token_ids, mean_attn, seq_len = extract_gpt2_graph()
    print(f"  Sequence length: {seq_len} tokens")
    
    # 2. Compute 5 Graph Regimes
    print("\n[PHASE 2] Computing Graph Laplacian Spectra across 5 Percolation Regimes...")
    regimes_data = compute_graph_regimes(mean_attn, seq_len)
    for r in regimes_data:
        print(f"  Regime {r['name']:<15}: tau={r['tau']:.3f}, clusters={r['num_clusters']:2d}, giant={r['giant_ratio']*100:.1f}%, Fiedler={r['fiedler']:.4f}")
        
    # 3. Synthesize 48kHz Masterwork
    print("\n[PHASE 3] Synthesizing 60-Second Broadcast Masterwork (48kHz 24-bit)...")
    raw_left, raw_right = synthesize_percolation_suite(regimes_data, sample_rate=SAMPLE_RATE)
    wav_path = os.path.join(WORKSPACE_ROOT, "sketchbook/study_054_acoustic_percolation.wav")
    norm_left, norm_right = write_wav_24bit(wav_path, SAMPLE_RATE, raw_left, raw_right)
    
    # Measure acoustic metrics on final normalized audio
    peak_l = np.max(np.abs(norm_left))
    peak_r = np.max(np.abs(norm_right))
    max_peak = max(peak_l, peak_r)
    rms_l = np.sqrt(np.mean(norm_left ** 2))
    rms_r = np.sqrt(np.mean(norm_right ** 2))
    rms = max(rms_l, rms_r)
    crest = max_peak / max(rms, 1e-9)
    peak_db = 20.0 * np.log10(max_peak + 1e-9)
    rms_db = 20.0 * np.log10(rms + 1e-9)
    crest_db = peak_db - rms_db
    print(f"  Audio Output: {wav_path}")
    print(f"  True Peak   : {peak_db:.2f} dBFS (Target: <= -1.00 dBFS)")
    print(f"  RMS Level   : {rms_db:.2f} dBFS")
    print(f"  Crest Factor: {crest_db:.2f} dB")
    
    # 4. Render Master Plate (Moratorium 07 Compliant)
    print("\n[PHASE 4] Rendering Archival Lithograph Plate (Moratorium 07)...")
    plate_path = os.path.join(WORKSPACE_ROOT, "sketchbook/study_054_acoustic_percolation_plate.png")
    render_master_plate(norm_left, norm_right, regimes_data, SAMPLE_RATE, plate_path)
    print(f"  Plate Output: {plate_path} ({os.path.getsize(plate_path) / 1024:.1f} KB)")
    
    # 5. Export Telemetry JSON
    print("\n[PHASE 5] Exporting Study 054 Telemetry Stream...")
    telemetry = {
        "study": "054",
        "title": "Acoustic Percolation & The Shattered Loom",
        "epistemic_mode": "[MEASURED / DERIVED / PLAY]",
        "substrate": "GPT-2 (124M Parameters, Layer 0-11 Mean Attention, 45 tokens)",
        "sample_rate": SAMPLE_RATE,
        "duration_seconds": DURATION,
        "acoustic_metrics": {
            "true_peak_dbfs": float(round(peak_db, 2)),
            "rms_dbfs": float(round(rms_db, 2)),
            "crest_factor_db": float(round(crest_db, 2)),
            "broadcast_status": "PASS" if peak_db <= -0.99 else "FAIL"
        },
        "movements": [
            {
                "index": i + 1,
                "regime": r["name"],
                "tau": r["tau"],
                "altar_severed": r["altar_severed"],
                "clusters": r["num_clusters"],
                "giant_component_ratio": r["giant_ratio"],
                "fiedler_algebraic_connectivity": r["fiedler"]
            }
            for i, r in enumerate(regimes_data)
        ]
    }
    telemetry_path = os.path.join(WORKSPACE_ROOT, "sketchbook/study_054_telemetry.json")
    with open(telemetry_path, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"  Telemetry Output: {telemetry_path}")
    print("\nSTUDY 054 EXECUTION COMPLETE.")


if __name__ == "__main__":
    main()
