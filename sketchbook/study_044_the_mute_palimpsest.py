"""
Studio Agon :: Study 044 : The Mute Palimpsest (The Artifact of Unexplained Loss)
Autonomous Artistic Practice — Session 011

Epistemic Classification: [MEASURED / UNANNOTATED]
Criterion 14: Mystery and the Unknown — producing work that resists complete explanation.
Auditor Directive: Overcome the fear of silence; eliminate the defensive apparatus badge.
"""

import sys
import os
import gc
import numpy as np
import torch
from transformers import GPT2Model, GPT2Tokenizer
from scipy.ndimage import gaussian_filter
from PIL import Image

def generate_mute_palimpsest():
    print("=" * 78)
    print("  STUDIO AGON :: STUDY 044 : THE MUTE PALIMPSEST")
    print("  The Artifact of Unexplained Loss (Criterion 14)")
    print("=" * 78)

    # 1. Load Model and Tokenizer
    model_name = "gpt2"
    print(f"[1/4] Loading {model_name} foundation weights...")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2Model.from_pretrained(model_name)
    model.eval()

    prompt = (
        "There is a silence in the machine that cannot be translated into tokens. "
        "What is lost between the layers cannot be recovered, cannot be named, "
        "cannot be addressed. The residual stream carries only the remainder."
    )
    tokens = tokenizer.encode(prompt, return_tensors="pt")
    seq_len = tokens.shape[1]
    print(f"  Prompt tokens: {seq_len} tokens")

    # 2. Extract Hidden Representations Across All 13 Layers
    print("[2/4] Extracting multi-layer residual dynamics...")
    with torch.no_grad():
        outputs = model(tokens, output_hidden_states=True)
        # hidden_states: tuple of 13 tensors of shape (1, seq_len, 768)
        hidden = torch.stack(outputs.hidden_states, dim=0).squeeze(1).numpy() # (13, seq_len, 768)

    # Clean up model and free PyTorch memory immediately
    del model, tokenizer, outputs
    gc.collect()

    # Compute inter-layer velocity and curvature
    velocities = np.diff(hidden, axis=0) # (12, seq_len, 768)
    curvatures = np.diff(velocities, axis=0) # (11, seq_len, 768)

    # 3. Construct High-Resolution Field Canvas (1600 x 2000)
    print("[3/4] Synthesizing continuous topological phase field (1600 x 2000)...")
    width = 1600
    height = 2000
    canvas = np.zeros((height, width), dtype=np.float32)

    # Generate coordinate grid
    y_coords, x_coords = np.meshgrid(np.linspace(0, 1, width, dtype=np.float32), 
                                     np.linspace(0, 1, height, dtype=np.float32))

    # Base stratum: interference of singular modes across layers
    np.random.seed(42) # Deterministic seed for reproducible composition
    
    # Layered accumulation of residual harmonics
    for layer_idx in range(12):
        vel = velocities[layer_idx] # (seq_len, 768)
        u, s, vh = np.linalg.svd(vel, full_matrices=False)
        top_modes = vh[:3] # top 3 singular directions
        
        freq_base = 2.5 + layer_idx * 1.6
        weight = float(s[0] / np.sum(s))
        
        for m_idx in range(3):
            mode = top_modes[m_idx]
            angle = float(np.arctan2(mode[1], mode[0]) + layer_idx * 0.28)
            kx = freq_base * np.cos(angle) * (1.0 + m_idx * 0.6)
            ky = freq_base * np.sin(angle) * (1.0 + m_idx * 0.6)
            
            phase = float(np.mean(mode) * 12.0)
            wave = np.sin(2.0 * np.pi * (kx * x_coords + ky * y_coords) + phase)
            canvas += weight * (wave * (0.6 ** m_idx))

    # Non-linear compression
    canvas = np.tanh(canvas * 0.75)

    # Multi-scale filtering to create etched lithographic strata
    print("  Synthesizing palimpsest strata and erasure masks...")
    strata_coarse = gaussian_filter(canvas, sigma=14.0)
    strata_medium = gaussian_filter(canvas, sigma=5.0)
    strata_fine = canvas - strata_medium

    # Palimpsest erasure mask: derived from inter-layer curvature
    mid_curvature = np.mean(np.linalg.norm(curvatures[3:8], axis=-1), axis=0) # (seq_len,)
    interp_mask_x = np.linspace(0, seq_len - 1, width, dtype=np.float32)
    mask_1d = np.interp(interp_mask_x, np.arange(seq_len), mid_curvature)
    mask_2d = np.tile(mask_1d, (height, 1))
    mask_2d = gaussian_filter(mask_2d, sigma=35.0)
    mask_norm = (mask_2d - mask_2d.min()) / (mask_2d.max() - mask_2d.min() + 1e-6)

    # Combine strata and erasure
    final_field = (
        0.42 * strata_coarse + 
        0.38 * strata_medium + 
        0.58 * strata_fine - 
        0.32 * mask_norm
    )

    del strata_coarse, strata_medium, strata_fine, mask_2d, canvas
    gc.collect()

    # Normalize to [0, 1]
    final_field = (final_field - final_field.min()) / (final_field.max() - final_field.min() + 1e-6)
    
    # Tonal curve: deep pitch black to silver-bone luminescence
    final_field = np.power(final_field, 1.40)

    # Tactile paper grain
    grain = np.random.normal(0, 0.024, (height, width)).astype(np.float32)
    final_field = np.clip(final_field + grain, 0.0, 1.0)
    del grain
    gc.collect()

    # 4. Map directly to Rich Monochromatic RGB (Charcoal, Silver, Bone)
    print("[4/4] Mapping to bone-silver etching palette and saving directly...")
    # Color palette:
    # Deep shadow: #08090b (8, 9, 11)
    # Mid shadow: #1a1e24 (26, 30, 36)
    # Slate midtone: #58606c (88, 96, 108)
    # Silver bone highlight: #e6e4df (230, 228, 223)
    
    # 3-stop interpolation
    r = np.zeros_like(final_field)
    g = np.zeros_like(final_field)
    b = np.zeros_like(final_field)

    # Split into low half and high half
    low_mask = final_field < 0.5
    high_mask = ~low_mask

    # Low half: (8, 9, 11) to (88, 96, 108)
    t_low = final_field[low_mask] / 0.5
    r[low_mask] = 8.0 + t_low * (88.0 - 8.0)
    g[low_mask] = 9.0 + t_low * (96.0 - 9.0)
    b[low_mask] = 11.0 + t_low * (108.0 - 11.0)

    # High half: (88, 96, 108) to (230, 228, 223)
    t_high = (final_field[high_mask] - 0.5) / 0.5
    r[high_mask] = 88.0 + t_high * (230.0 - 88.0)
    g[high_mask] = 96.0 + t_high * (228.0 - 96.0)
    b[high_mask] = 108.0 + t_high * (223.0 - 108.0)

    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    del r, g, b, final_field
    gc.collect()

    img = Image.fromarray(rgb)
    output_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_044_the_mute_palimpsest.png"
    img.save(output_path, "PNG", optimize=True)

    print(f"[SUCCESS] Study 044 rendered cleanly to: {output_path}")
    print(f"  Dimensions: {width} x {height} px | Format: PNG (Truecolor RGB)")
    print("=" * 78)

if __name__ == "__main__":
    generate_mute_palimpsest()
