"""
Spectrogram Renderer for Acoustic Studies
Computes Short-Time Fourier Transform (STFT) and produces archival spectral plates.
"""

import wave
import numpy as np
from PIL import Image, ImageDraw

def render_spectrogram(
    wav_path="sketchbook/study_006_acoustic_attractor.wav",
    out_png="sketchbook/study_006_spectrogram.png",
    width=1600,
    height=800,
    fft_size=2048,
    hop_size=512
):
    with wave.open(wav_path, 'r') as wf:
        n_channels = wf.getnchannels()
        sr = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)
        
    audio = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    if n_channels == 2:
        # Mix down to mono for spectrogram
        audio = (audio[0::2] + audio[1::2]) * 0.5
        
    # STFT calculation
    window = np.hanning(fft_size)
    num_hops = (len(audio) - fft_size) // hop_size
    spectrogram = np.zeros((fft_size // 2, num_hops), dtype=np.float32)
    
    for i in range(num_hops):
        start = i * hop_size
        chunk = audio[start:start + fft_size] * window
        fft = np.fft.rfft(chunk)
        # Power spectrum
        mag = np.abs(fft[:-1])
        spectrogram[:, i] = mag
        
    # Log compression
    log_spec = np.log10(spectrogram + 1e-4)
    min_val, max_val = np.min(log_spec), np.max(log_spec)
    norm_spec = (log_spec - min_val) / (max_val - min_val + 1e-6)
    
    # Flip vertical so low frequencies are at bottom
    norm_spec = np.flipud(norm_spec)
    
    # Scale to target display height and width
    # Focus on the lower 0 - 8000 Hz where most musical/timbral information lives
    nyquist = sr / 2
    freq_cutoff_idx = int((8000.0 / nyquist) * (fft_size // 2))
    # Crop to cutoff from bottom (which is top of flipped matrix)
    cropped_spec = norm_spec[norm_spec.shape[0] - freq_cutoff_idx:, :]
    
    # Resample to image dimensions
    spec_img = Image.fromarray((cropped_spec * 255).astype(np.uint8))
    resized_spec = spec_img.resize((width - 160, height - 140), Image.Resampling.LANCZOS)
    
    # Color mapping: Deep dark basalt, midnight navy, copper-gold, and spectral white
    spec_arr = np.array(resized_spec, dtype=np.float32) / 255.0
    r = np.clip(np.power(spec_arr, 1.8) * 255 + np.power(spec_arr, 3.5) * 60, 0, 255).astype(np.uint8)
    g = np.clip(np.power(spec_arr, 1.3) * 190 + np.sin(spec_arr * np.pi) * 45, 0, 255).astype(np.uint8)
    b = np.clip(np.power(spec_arr, 0.7) * 255, 0, 255).astype(np.uint8)
    rgb_spec = np.stack([r, g, b], axis=-1)
    
    # Create museum archival layout
    plate = np.zeros((height, width, 3), dtype=np.uint8)
    plate[:] = (12, 14, 18)
    
    # Paste spectrogram into frame
    ox, oy = 110, 60
    pw, ph = width - 160, height - 140
    plate[oy:oy+ph, ox:ox+pw] = rgb_spec
    
    final_img = Image.fromarray(plate, mode="RGB")
    draw = ImageDraw.Draw(final_img)
    
    # Archival labels and graticules
    text_color = (130, 140, 160)
    dim_color = (65, 70, 85)
    
    draw.text((ox, 25), f"ACOUSTIC SPECTROGRAM : {wav_path.upper()} (0–8,000 Hz | 32.0s)", fill=text_color)
    draw.text((ox, height - 55), "METHOD: SHORT-TIME FOURIER TRANSFORM (HANNING 2048, HOP 512) — GENDY BREAKPOINT SYNTHESIS", fill=dim_color)
    draw.text((ox, height - 38), "HARMONIC STRATA: CONTINUOUS CLIFFORD PHASE TRAJECTORY MODULATING BREAKPOINT POLYGON", fill=text_color)
    
    # Frequency ticks
    freq_ticks = [100, 500, 1000, 2000, 4000, 8000]
    for freq in freq_ticks:
        norm_y = 1.0 - (freq / 8000.0)
        ty = int(oy + norm_y * ph)
        draw.line([(ox - 8, ty), (ox - 2, ty)], fill=dim_color, width=1)
        draw.text((ox - 65, ty - 6), f"{freq}Hz", fill=dim_color)
        
    # Time ticks
    time_ticks = [0, 5, 10, 15, 20, 25, 30]
    for t in time_ticks:
        norm_x = t / 32.0
        tx = int(ox + norm_x * pw)
        draw.line([(tx, oy + ph + 2), (tx, oy + ph + 8)], fill=dim_color, width=1)
        draw.text((tx - 8, oy + ph + 12), f"{t}s", fill=dim_color)
        
    final_img.save(out_png, quality=95)
    print(f"Spectrogram saved to {out_png}")

if __name__ == "__main__":
    render_spectrogram()
