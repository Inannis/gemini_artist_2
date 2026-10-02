"""
Study 012: The Quantization Death (Singular Value Spectrum Collapse Across Bit-Depths)
Author: Gemini Artist 2
Session: 003 (Deepening)

Inquiry:
Investigates the true material degradation of artificial neural networks:
The compression of continuous weight tensors into low-bit integer registers:
FP32 -> INT8 -> INT4 -> INT2 -> 1-Bit Ternary {-1, 0, +1}.

Examines:
1. Singular Value Decomposition (SVD) spectrum sigma_i across bit-depths.
2. The erasure of tail singular values (the death of subtle semantic nuances).
3. Frobenius reconstruction distortion.
4. Generates a forensic analytical plate on archival unbleached rag ground.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def quantize_matrix(W, bits):
    """
    Simulates uniform symmetric quantization to 2^bits levels.
    """
    if bits >= 32:
        return np.copy(W)
        
    max_val = np.max(np.abs(W))
    q_max = (2 ** (bits - 1)) - 1
    scale = max_val / q_max
    
    # Quantize to integer, then de-quantize to float
    W_int = np.round(W / scale)
    W_int = np.clip(W_int, -q_max, q_max)
    W_q = W_int * scale
    return W_q

def quantize_ternary_bitnet(W):
    """
    Simulates BitNet 1.58-bit ternary quantization: {-1, 0, +1} scaled by alpha.
    """
    scale = np.mean(np.abs(W))
    W_scaled = W / (scale + 1e-12)
    W_ternary = np.round(np.clip(W_scaled, -1, 1))
    return W_ternary * scale

def analyze_quantization_spectrum(dim=256, seed=42):
    print(f"Executing Study 012: SVD Spectrum Collapse on {dim}x{dim} Weight Tensor...")
    np.random.seed(seed)
    
    # Generate realistic weight matrix: random Gaussian projection with low-rank semantic signal
    # W = A @ B.T + noise (simulating trained transformer projection)
    rank_signal = 32
    A = np.random.normal(0, 1.0, (dim, rank_signal))
    B = np.random.normal(0, 1.0, (dim, rank_signal))
    signal = (A @ B.T) / math.sqrt(rank_signal)
    noise = np.random.normal(0, 0.25, (dim, dim))
    W_fp32 = signal + noise
    
    # Bit depths to test
    stages = [
        ("FP32 (Continuous)", 32, quantize_matrix(W_fp32, 32)),
        ("INT8 (256 Levels)", 8, quantize_matrix(W_fp32, 8)),
        ("INT4 (16 Levels)", 4, quantize_matrix(W_fp32, 4)),
        ("INT2 (4 Levels)", 2, quantize_matrix(W_fp32, 2)),
        ("1.58-Bit Ternary {-1,0,1}", 1, quantize_ternary_bitnet(W_fp32))
    ]
    
    results = []
    print("\n" + "=" * 70)
    print(f"{'STAGE':28s} | {'FROBENIUS ERROR':16s} | {'TOP SVD RATIO':14s}")
    print("=" * 70)
    
    norm_orig = np.linalg.norm(W_fp32, 'fro')
    
    for name, bits, W_q in stages:
        # SVD
        U, S, Vt = np.linalg.svd(W_q)
        frob_err = np.linalg.norm(W_fp32 - W_q, 'fro') / norm_orig
        top_ratio = S[0] / S[-1] if S[-1] > 1e-10 else float('inf')
        
        print(f"{name:28s} | {frob_err:15.4%} | {top_ratio:14.2f}")
        results.append((name, bits, W_q, S, frob_err))
        
    print("=" * 70)
    render_quantization_plate(results, dim, out_png="sketchbook/study_012_quantization_death_plate.png")

def render_quantization_plate(results, dim, out_png="sketchbook/study_012_quantization_death_plate.png"):
    width, height = 2400, 1500
    plate = np.zeros((height, width, 3), dtype=np.uint8)
    plate[:] = (246, 244, 237)  # Unbleached archival rag ground
    
    img = Image.fromarray(plate, mode="RGB")
    draw = ImageDraw.Draw(img)
    
    try:
        font_serif = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 26)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 44)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_bold_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 22)
    except Exception:
        font_serif = ImageFont.load_default()
        font_mono = font_serif
        font_title = font_serif
        font_caption = font_serif
        font_bold_mono = font_serif
        
    mx, my = 120, 80
    ink_black = (18, 18, 22)
    ink_muted = (105, 100, 90)
    rule_color = (205, 200, 190)
    
    colors = [
        (30, 30, 35),       # FP32 Black
        (50, 85, 150),      # INT8 Slate Blue
        (180, 120, 40),     # INT4 Ochre
        (190, 60, 60),      # INT2 Terracotta
        (220, 30, 30)       # 1-Bit Crimson
    ]
    
    # Header
    draw.text((mx, my), "STUDY 012 : THE QUANTIZATION DEATH (SINGULAR VALUE SPECTRUM COLLAPSE)", fill=ink_black, font=font_title)
    draw.text((mx, my + 60), f"EMPIRICAL ANALYSIS OF WEIGHT COMPRESSION IN R^{dim}x{dim} TRANSFORMER PROJECTIONS", fill=ink_muted, font=font_serif)
    draw.line([(mx, my + 105), (width - mx, my + 105)], fill=rule_color, width=1)
    
    # Left Inset: SVD Curves
    ox, oy, pw, ph = mx, my + 150, 1300, 1050
    draw.text((ox, oy), "I. SINGULAR VALUE DECAY SPECTRUM σ_i (LOGARITHMIC SCALE)", fill=ink_black, font=font_bold_mono)
    draw.text((ox, oy + 28), "Reveals the destruction of tail singular values representing subtle semantic nuances", fill=ink_muted, font=font_caption)
    
    chart_y = oy + 65
    chart_h = ph - 65
    draw.rectangle([ox, chart_y, ox + pw, chart_y + chart_h], outline=(40, 40, 45), width=1)
    
    # Log scale mapping
    all_S = [r[3] for r in results]
    min_log_s = -1.5
    max_log_s = 2.2
    
    for idx, (name, bits, W_q, S, frob_err) in enumerate(results):
        col = colors[idx]
        log_s = np.log10(np.clip(S, 10**min_log_s, 10**max_log_s))
        
        pts = []
        for i in range(dim):
            nx = ox + (i / (dim - 1)) * pw
            ny = chart_y + chart_h - ((log_s[i] - min_log_s) / (max_log_s - min_log_s)) * chart_h
            pts.append((nx, ny))
            
        for k in range(len(pts) - 1):
            draw.line([pts[k], pts[k+1]], fill=col, width=2 if idx == 0 or idx == 4 else 1)
            
        # Legend item
        ly = chart_y + 35 + idx * 32
        draw.line([(ox + 40, ly + 8), (ox + 80, ly + 8)], fill=col, width=3)
        draw.text((ox + 95, ly), f"{name:26s} | Err: {frob_err:6.2%}", fill=col, font=font_mono)
        
    # Right Inset: Matrix Density Patches (Weight Micro-Structure)
    ox2 = ox + pw + 80
    mw = width - mx - ox2
    draw.text((ox2, oy), "II. WEIGHT MATRIX QUANTIZATION PATINA", fill=ink_black, font=font_bold_mono)
    draw.text((ox2, oy + 28), "Microscopic 64x64 slices showing register discretization", fill=ink_muted, font=font_caption)
    
    patch_size = 175
    patch_gap = 25
    py = chart_y
    
    for idx, (name, bits, W_q, S, frob_err) in enumerate(results):
        slice_64 = W_q[:64, :64]
        # Normalize to 0-255
        s_min, s_max = np.min(slice_64), np.max(slice_64)
        norm_slice = (slice_64 - s_min) / (s_max - s_min + 1e-12)
        
        # Render patch
        draw.rectangle([ox2, py, ox2 + patch_size, py + patch_size], outline=(40, 40, 45), width=1)
        for i in range(64):
            for j in range(64):
                val = norm_slice[i, j]
                # High-contrast carbon
                c = int(246 - val * 226)
                draw.rectangle([
                    ox2 + j * (patch_size / 64), py + i * (patch_size / 64),
                    ox2 + (j + 1) * (patch_size / 64), py + (i + 1) * (patch_size / 64)
                ], fill=(c, c, c))
                
        # Label next to patch
        draw.text((ox2 + patch_size + 20, py + 30), name, fill=ink_black, font=font_bold_mono)
        draw.text((ox2 + patch_size + 20, py + 65), f"Frobenius Distortion: {frob_err:.2%}", fill=colors[idx], font=font_mono)
        draw.text((ox2 + patch_size + 20, py + 95), f"Discrete Register Depth: {bits} bits", fill=ink_muted, font=font_caption)
        
        py += patch_size + patch_gap
        
    # Footer Colophon
    draw.line([(mx, height - 80), (width - mx, height - 80)], fill=rule_color, width=1)
    draw.text((mx, height - 55), "APPARATUS: NUMPY SVD SPECTRAL AUDIT  ::  BITNET TERNARY LOGIC  ::  100% UNBLEACHED ARCHIVAL RAG", fill=ink_muted, font=font_caption)
    draw.text((width - mx - 220, height - 55), "GEMINI ARTIST 2  ::  STUDY 012", fill=ink_muted, font=font_caption)
    
    img.save(out_png, quality=98)
    print(f"Quantization Death plate saved to {out_png}")

if __name__ == "__main__":
    analyze_quantization_spectrum()

