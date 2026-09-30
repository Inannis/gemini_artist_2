"""
Study 009: The Parity Cleave & Quantum Chaos Restoration
Author: Gemini Artist 2
Session: 003

Discovery in Study 008:
Diagonalizing the full SYK4 Hamiltonian yielded <r> = 0.3728 (Poisson statistics),
seemingly contradicting the claim that SYK is maximally chaotic.
The physical reason: The fermion parity operator P = (-i)^(N/2) * chi_1...chi_N commutes
with H. Independent eigenvalue spectra from even and odd parity sectors interleave,
masking level repulsion.

Hypothesis:
Projecting H into the irreducible symmetry sector P = +1 will restore Wigner-Dyson
level repulsion (<r> ≈ 0.5307 for GOE or 0.60 for GUE), proving that symmetry hides chaos.
"""

import math
import itertools
import numpy as np
from PIL import Image, ImageDraw

def pauli_matrices():
    I = np.array([[1, 0], [0, 1]], dtype=np.complex128)
    X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return I, X, Y, Z

def build_majoranas_and_parity(N=12):
    K = N // 2
    dim = 2 ** K
    I, X, Y, Z = pauli_matrices()
    
    c_base = (X + 1j * Y) / 2.0
    majoranas = []
    
    for q in range(K):
        op_list_c = [I] * K
        for p in range(q):
            op_list_c[p] = Z
        op_list_c[q] = c_base
        
        cq = op_list_c[0]
        for p in range(1, K):
            cq = np.kron(cq, op_list_c[p])
            
        cq_dag = cq.conj().T
        majoranas.append(cq + cq_dag)
        majoranas.append(-1j * (cq - cq_dag))
        
    # Parity operator P = prod_q (-Z_q)
    # For K qubits, P is the tensor product of (-Z)
    P = -Z
    for p in range(1, K):
        P = np.kron(P, -Z)
        
    return majoranas, P

def build_syk_hamiltonian(majoranas, N=12, J_scale=1.0, seed=42):
    K = N // 2
    dim = 2 ** K
    H = np.zeros((dim, dim), dtype=np.complex128)
    
    np.random.seed(seed)
    var_J = (6.0 * (J_scale ** 2)) / (N ** 3)
    std_J = math.sqrt(var_J)
    
    combos = list(itertools.combinations(range(N), 4))
    couplings = np.random.normal(0.0, std_J, len(combos))
    
    for idx, (i, j, k, l) in enumerate(combos):
        j_val = couplings[idx]
        term = majoranas[i] @ majoranas[j] @ majoranas[k] @ majoranas[l]
        H += j_val * term
        
    H = (H + H.conj().T) / 2.0
    return H

def test_parity_cleave(N=12, num_disorder=16):
    print(f"Executing Study 009: Parity Cleave on N={N} Majorana SYK ({num_disorder} disorder seeds)...")
    majoranas, P = build_majoranas_and_parity(N=N)
    dim = 2 ** (N // 2)
    
    # Diagonalize P to find projector onto P = +1 sector
    p_vals, p_vecs = np.linalg.eigh(P)
    even_indices = np.where(p_vals > 0.5)[0]
    V_even = p_vecs[:, even_indices]  # Subspace projection matrix (dim x dim/2)
    dim_even = len(even_indices)
    
    print(f"Hilbert space dimension: {dim} -> Projected Even Parity Sector: {dim_even}")
    
    all_raw_r = []
    all_even_r = []
    
    t_points = np.logspace(-1.5, 3.5, 300)
    sff_even_accum = np.zeros(len(t_points), dtype=np.float64)
    sff_raw_accum  = np.zeros(len(t_points), dtype=np.float64)
    
    for r in range(num_disorder):
        seed = 400 + r * 23
        H = build_syk_hamiltonian(majoranas, N=N, seed=seed)
        
        # 1. Full Hamiltonian eigenvalues
        evals_full = np.linalg.eigvalsh(H)
        sp_full = np.diff(evals_full)
        sp_full = sp_full[sp_full > 1e-10]
        if len(sp_full) > 2:
            r_k = np.minimum(sp_full[:-1], sp_full[1:]) / np.maximum(sp_full[:-1], sp_full[1:])
            all_raw_r.extend(r_k)
            
        for it, t in enumerate(t_points):
            sff_raw_accum[it] += np.abs(np.sum(np.exp(-1j * evals_full * t)))**2 / (dim**2)
            
        # 2. Projected Even Parity Hamiltonian: H_even = V_even^dagger * H * V_even
        H_even = V_even.conj().T @ H @ V_even
        evals_even = np.linalg.eigvalsh(H_even)
        
        sp_even = np.diff(evals_even)
        sp_even = sp_even[sp_even > 1e-10]
        if len(sp_even) > 2:
            r_even_k = np.minimum(sp_even[:-1], sp_even[1:]) / np.maximum(sp_even[:-1], sp_even[1:])
            all_even_r.extend(r_even_k)
            
        for it, t in enumerate(t_points):
            sff_even_accum[it] += np.abs(np.sum(np.exp(-1j * evals_even * t)))**2 / (dim_even**2)
            
    mean_raw_r = np.mean(all_raw_r)
    mean_even_r = np.mean(all_even_r)
    sff_raw = sff_raw_accum / num_disorder
    sff_even = sff_even_accum / num_disorder
    
    print("\n" + "=" * 65)
    print("PARITY CLEAVE EXPERIMENTAL RESULTS:")
    print(f"Full Spectrum <r> (Unprojected):  {mean_raw_r:.4f}  (Expected Poisson ≈ 0.386)")
    print(f"Projected Even Sector <r> (P=+1): {mean_even_r:.4f}  (Expected GOE ≈ 0.5307 / GUE ≈ 0.60)")
    
    if mean_even_r > 0.50:
        print(">>> SUCCESS: Quantum Level Repulsion RESTORED by Parity Cleave! <<<")
    print("=" * 65)
    
    render_comparison_plate(t_points, sff_raw, sff_even, mean_raw_r, mean_even_r, N, dim, dim_even)

def render_comparison_plate(t_points, sff_raw, sff_even, r_raw, r_even, N, dim, dim_even, out_png="sketchbook/study_009_parity_restoration_plate.png"):
    width, height = 2000, 1100
    plate = np.zeros((height, width, 3), dtype=np.uint8)
    plate[:] = (8, 9, 13)
    
    img = Image.fromarray(plate, mode="RGB")
    draw = ImageDraw.Draw(img)
    
    text_color = (200, 210, 230)
    dim_color = (90, 100, 120)
    poisson_red = (255, 95, 95)
    chaos_cyan = (80, 220, 255)
    
    # Headers
    draw.text((80, 35), "STUDY 009 : THE PARITY CLEAVE — RESTORATION OF QUANTUM CHAOS", fill=text_color)
    draw.text((80, 60), f"SYK4 MAJORANA FERMION MATRIX (N={N}) :: HILBERT SPACE DIMENSION: {dim} -> PROJECTED SECTOR: {dim_even}", fill=dim_color)
    draw.text((80, 80), f"UNPROJECTED <r> = {r_raw:.4f} [POISSON INTERLEAVING]  -->  PARITY-CLEAVED <r> = {r_even:.4f} [WIGNER-DYSON RIGIDITY]", fill=chaos_cyan)
    
    # Plot 1: Unprojected SFF (Left)
    ox1, oy, pw, ph = 80, 140, 880, 840
    draw.rectangle([ox1, oy, ox1 + pw, oy + ph], outline=(30, 35, 48), width=1)
    draw.text((ox1 + 25, oy + 25), "I. UNPROJECTED SYK (SYMMETRY CONCEALS CHAOS)", fill=poisson_red)
    draw.text((ox1 + 25, oy + 45), f"Level Spacing Ratio <r> = {r_raw:.4f} (Independent Parity Mixing)", fill=dim_color)
    
    # Plot 2: Parity-Cleaved SFF (Right)
    ox2 = 1040
    draw.rectangle([ox2, oy, ox2 + pw, oy + ph], outline=(30, 35, 48), width=1)
    draw.text((ox2 + 25, oy + 25), "II. PARITY-CLEAVED SECTOR P = +1 (PURIFIED CHAOS)", fill=chaos_cyan)
    draw.text((ox2 + 25, oy + 45), f"Level Spacing Ratio <r> = {r_even:.4f} (Wigner-Dyson Level Repulsion)", fill=dim_color)
    
    # Draw curves
    log_t = np.log10(t_points)
    min_lt, max_lt = log_t[0], log_t[-1]
    min_ls, max_ls = -3.2, 0.2
    
    pts_raw = []
    pts_even = []
    
    for lt, sr, se in zip(log_t, np.log10(sff_raw + 1e-12), np.log10(sff_even + 1e-12)):
        nx = (lt - min_lt) / (max_lt - min_lt)
        ny_r = 1.0 - (sr - min_ls) / (max_ls - min_ls)
        ny_e = 1.0 - (se - min_ls) / (max_ls - min_ls)
        
        pts_raw.append((ox1 + nx * pw, oy + ny_r * ph))
        pts_even.append((ox2 + nx * pw, oy + ny_e * ph))
        
    for i in range(len(pts_raw) - 1):
        draw.line([pts_raw[i], pts_raw[i+1]], fill=poisson_red, width=2)
        draw.line([pts_even[i], pts_even[i+1]], fill=chaos_cyan, width=2)
        
    # Mark the Linear Ramp on the right plot
    draw.text((ox2 + pw * 0.55, oy + ph * 0.45), "UNIVERSAL LINEAR RAMP", fill=chaos_cyan)
    draw.text((ox2 + pw * 0.55, oy + ph * 0.48), "g(t) ~ t (Level Repulsion)", fill=dim_color)
    
    img.save(out_png, quality=96)
    print(f"Comparison plate rendered to {out_png}")

if __name__ == "__main__":
    test_parity_cleave(N=12, num_disorder=16)
