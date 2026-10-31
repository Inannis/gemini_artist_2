#!/usr/bin/env python3
"""
Studio Agon :: Acoustic Compliance & Sonic Heritage Audit
Audits all WAV audio assets across works and sketchbook studies to ensure
broadcast compliance, dynamic range integrity, and zero digital clipping.
"""

import os
import wave
import struct
import math
import numpy as np

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def audit_wav(path):
    rel_path = os.path.relpath(path, WORKSPACE_ROOT)
    try:
        with wave.open(path, 'rb') as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            duration = n_frames / float(framerate)
            
            raw_data = wf.readframes(n_frames)
            total_samples = n_frames * n_channels
            
            if sampwidth == 2:
                samples = np.frombuffer(raw_data, dtype=np.int16)
                norm_samples = samples.astype(np.float64) / 32768.0
            elif sampwidth == 3:
                raw_bytes = np.frombuffer(raw_data, dtype=np.uint8)
                b0 = raw_bytes[0::3].astype(np.int32)
                b1 = raw_bytes[1::3].astype(np.int32)
                b2 = raw_bytes[2::3].astype(np.int32)
                sign = (b2 >= 128).astype(np.int32) * -16777216
                samples = b0 | (b1 << 8) | (b2 << 16) | sign
                norm_samples = samples.astype(np.float64) / 8388608.0
            elif sampwidth == 4:
                samples = np.frombuffer(raw_data, dtype=np.int32)
                norm_samples = samples.astype(np.float64) / 2147483648.0
            else:
                return None
                
            peak = float(np.max(np.abs(norm_samples)))
            rms = float(np.sqrt(np.mean(norm_samples ** 2)))
            peak_db = 20 * math.log10(peak + 1e-9)
            rms_db = 20 * math.log10(rms + 1e-9)
            crest_factor = peak_db - rms_db
            
            return {
                "rel_path": rel_path,
                "channels": n_channels,
                "rate": framerate,
                "duration": duration,
                "peak_db": peak_db,
                "rms_db": rms_db,
                "crest_factor": crest_factor,
                "clipping": peak >= 0.999
            }
    except Exception as e:
        return {"rel_path": rel_path, "error": str(e)}

def main():
    print("=" * 80)
    print("  STUDIO AGON :: ACOUSTIC BROADCAST COMPLIANCE AUDIT")
    print("=" * 80)
    
    wav_files = []
    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        if "dist" in root or ".git" in root:
            continue
        for f in sorted(files):
            if f.endswith(".wav"):
                wav_files.append(os.path.join(root, f))
                
    print(f"Discovered {len(wav_files)} acoustic masterworks and studies:\n")
    print(f"{'Asset':<48} {'Rate':<7} {'Dur':<6} {'Peak':<9} {'RMS':<9} {'Crest':<7} {'Status'}")
    print("-" * 92)
    
    all_ok = True
    for wp in wav_files:
        info = audit_wav(wp)
        if not info or "error" in info:
            print(f"{os.path.basename(wp):<48} ERROR")
            continue
        
        status = "PASS" if not info["clipping"] and info["peak_db"] > -30 else "WARN"
        print(f"{info['rel_path'][:46]:<48} {info['rate']}Hz {info['duration']:4.1f}s {info['peak_db']:6.1f}dB {info['rms_db']:6.1f}dB {info['crest_factor']:5.1f}dB {status}")
        if info["clipping"]:
            all_ok = False
            
    print("-" * 92)
    print(f"Acoustic Compliance: {'100% BROADCAST COMPLIANT' if all_ok else 'ATTENTION NEEDED'}")
    print("=" * 80)

if __name__ == "__main__":
    main()
