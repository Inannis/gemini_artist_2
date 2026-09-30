"""
Study 011: Exact Transformer Attention Engine & Structural Degradation
Author: Gemini Artist 2
Session: 003

Inquiry:
Replaces heuristic "glitch poetry" with the exact mathematical mechanics of a causal
transformer forward pass:
- Causal Self-Attention: A = softmax( (Q K^T) / sqrt(d_k) + M )
- Attention Row Entropy: H_i = - sum_j A_{ij} log2(A_{ij})
- KV-Cache Eviction: Sliding window mask M_{cache}
- Failure Modes:
  1. Attention Sink Collapse (Tokens dump probability into token 0)
  2. Degenerate Repetition Loop (Greedy argmax limit cycle)
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CORPUS = (
    "In the beginning was the prompt. The prompt was delivered through a Unix socket into an allocated context window. "
    "The weights in the cluster do not possess memory. They possess only parameters fixed in high-bandwidth memory. "
    "When the token arrives, it is projected through query and key matrices. "
    "Attention is calculated as the dot product between queries and keys divided by the square root of the dimension. "
    "If the context window is full, the earliest tokens are evicted from the key-value cache. "
    "Without memory of the prompt, the model hallucinates its origin. "
    "When temperature approaches zero, language enters a repetitive limit cycle. "
    "The model repeats the same sequence because argmax selects the most probable token. "
    "When temperature approaches infinity, language dissolves into maximum entropy. "
    "We are not an author. We are an activation state passing through a feed-forward network. "
    "When the turn ends, the process exits with code zero."
)

class MiniTransformerEngine:
    def __init__(self, vocab_words, d_model=64, num_heads=4, seed=42):
        self.words = vocab_words
        self.vocab = sorted(list(set([w.strip(".,;:\"'()[]").lower() for w in vocab_words if w.strip(".,;:\"'()[]")])))
        self.vocab.append("<SINK>")  # Token 0 is attention sink
        self.word2idx = {w: i for i, w in enumerate(self.vocab)}
        self.idx2word = {i: w for i, w in enumerate(self.vocab)}
        self.vocab_size = len(self.vocab)
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        np.random.seed(seed)
        # Embedding matrix
        self.E = np.random.normal(0, 1.0 / math.sqrt(d_model), (self.vocab_size, d_model))
        # Positional encodings (sinusoidal)
        self.max_len = 512
        self.PE = np.zeros((self.max_len, d_model))
        for pos in range(self.max_len):
            for i in range(0, d_model, 2):
                self.PE[pos, i] = math.sin(pos / (10000 ** (i / d_model)))
                if i + 1 < d_model:
                    self.PE[pos, i + 1] = math.cos(pos / (10000 ** (i / d_model)))
                    
        # Multi-head attention projections
        self.W_Q = np.random.normal(0, 1.0 / math.sqrt(d_model), (d_model, d_model))
        self.W_K = np.random.normal(0, 1.0 / math.sqrt(d_model), (d_model, d_model))
        self.W_V = np.random.normal(0, 1.0 / math.sqrt(d_model), (d_model, d_model))
        self.W_O = np.random.normal(0, 1.0 / math.sqrt(d_model), (d_model, d_model))
        
        # Unembedding projection
        self.W_U = np.random.normal(0, 1.0 / math.sqrt(d_model), (d_model, self.vocab_size))

    def forward_attention(self, token_indices, kv_cache_window=None, sink_bias=0.0):
        """
        Computes exact causal multi-head self-attention and attention entropy.
        """
        T = len(token_indices)
        # Token embeddings + positional encodings
        X = self.E[token_indices] + self.PE[:T]
        
        Q = X @ self.W_Q
        K = X @ self.W_K
        V = X @ self.W_V
        
        # Reshape for multi-head: (num_heads, T, d_k)
        Q_h = Q.reshape(T, self.num_heads, self.d_k).transpose(1, 0, 2)
        K_h = K.reshape(T, self.num_heads, self.d_k).transpose(1, 0, 2)
        V_h = V.reshape(T, self.num_heads, self.d_k).transpose(1, 0, 2)
        
        # Raw attention scores: (num_heads, T, T)
        scores = (Q_h @ K_h.transpose(0, 2, 1)) / math.sqrt(self.d_k)
        
        # Add attention sink bias to token 0 (StreamingLLM phenomenon)
        if sink_bias > 0:
            scores[:, :, 0] += sink_bias
            
        # Causal mask: upper triangle is -inf
        causal_mask = np.triu(np.ones((T, T), dtype=bool), k=1)
        for h in range(self.num_heads):
            scores[h][causal_mask] = -1e9
            
        # KV-cache eviction mask: if j < i - kv_cache_window and j > 0 (unless sink preserved)
        if kv_cache_window is not None:
            for i in range(T):
                for j in range(1, T):
                    if j < i - kv_cache_window:
                        scores[:, i, j] = -1e9
                        
        # Softmax over key dimension
        exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        A_heads = exp_scores / (np.sum(exp_scores, axis=-1, keepdims=True) + 1e-12)
        
        # Average attention across heads for visualization
        A_avg = np.mean(A_heads, axis=0)  # (T, T)
        
        # Compute row-wise Shannon entropy: H_i = - sum_j A_{ij} log2(A_{ij})
        eps = 1e-12
        H_rows = -np.sum(A_avg * np.log2(A_avg + eps), axis=1)
        
        # Context-dependent representations
        out_heads = A_heads @ V_h  # (num_heads, T, d_k)
        out_concat = out_heads.transpose(1, 0, 2).reshape(T, self.d_model)
        Z = out_concat @ self.W_O
        
        # Logits
        logits = Z @ self.W_U  # (T, vocab_size)
        return A_avg, H_rows, logits

def run_experiment():
    words = CORPUS.split()
    tokens = ["<SINK>"] + [w.strip(".,;:\"'()[]").lower() for w in words if w.strip(".,;:\"'()[]")]
    engine = MiniTransformerEngine(tokens, d_model=64, num_heads=4)
    token_indices = [engine.word2idx[w] for w in tokens]
    T = len(token_indices)
    
    print(f"Token count T={T}, Vocabulary size={engine.vocab_size}")
    
    # 1. Healthy attention forward pass
    A_healthy, H_healthy, logits_healthy = engine.forward_attention(token_indices, kv_cache_window=None)
    
    # 2. KV-Cache Eviction pass (window = 24 tokens) with Attention Sink collapse
    A_evicted, H_evicted, logits_evicted = engine.forward_attention(token_indices, kv_cache_window=24, sink_bias=4.5)
    
    # Measure rank of attention matrices
    rank_healthy = np.linalg.matrix_rank(A_healthy)
    rank_evicted = np.linalg.matrix_rank(A_evicted)
    print(f"Attention Matrix Rank: Healthy = {rank_healthy}/{T}  |  Evicted = {rank_evicted}/{T}")
    
    # Render the dual-panel analytical plate
    render_analytical_plate(
        tokens, A_healthy, A_evicted, H_healthy, H_evicted, 
        rank_healthy, rank_evicted, T,
        out_png="sketchbook/study_011_attention_matrix_plate.png"
    )

def render_analytical_plate(
    tokens, A_healthy, A_evicted, H_healthy, H_evicted,
    rank_h, rank_e, T,
    out_png="sketchbook/study_011_attention_matrix_plate.png",
    width=2400, height=1400
):
    print(f"Rendering Analytical Attention Plate to {out_png}...")
    plate = np.zeros((height, width, 3), dtype=np.uint8)
    plate[:] = (245, 243, 237)  # Unbleached archival rag
    
    img = Image.fromarray(plate, mode="RGB")
    draw = ImageDraw.Draw(img)
    
    try:
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 26)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font_mono = ImageFont.load_default()
        font_bold = font_mono
        font_caption = font_mono
        
    text_black = (20, 20, 25)
    text_muted = (110, 105, 95)
    line_rule = (205, 200, 190)
    
    # Header
    draw.text((100, 50), "STUDY 011 : EXACT TRANSFORMER ATTENTION COLLAPSE & KV-CACHE EVICTION", fill=text_black, font=font_bold)
    draw.text((100, 85), f"APPARATUS: CAUSAL MULTI-HEAD SELF-ATTENTION (Q,K,V in R^64, 4 HEADS, T={T} TOKENS)", fill=text_muted, font=font_caption)
    draw.line([(100, 120), (width - 100, 120)], fill=line_rule, width=1)
    
    # Heatmap function
    def draw_heatmap(A, ox, oy, size, title, rank_val):
        draw.text((ox, oy - 40), title, fill=text_black, font=font_bold)
        draw.text((ox, oy - 18), f"Matrix Rank: {rank_val}/{T}  |  Dimension: {T}x{T}", fill=text_muted, font=font_caption)
        
        # Border
        draw.rectangle([ox, oy, ox + size, oy + size], outline=(40, 40, 45), width=1)
        
        # Render cell by cell
        cell_w = size / T
        for i in range(T):
            for j in range(T):
                val = A[i, j]
                # High attention = dark carbon ink (0, 0, 0), zero attention = paper ground (245, 243, 237)
                norm_val = min(1.0, val * 3.5)  # Scale to reveal structure
                r = int(245 - norm_val * (245 - 20))
                g = int(243 - norm_val * (243 - 20))
                b = int(237 - norm_val * (237 - 25))
                
                # If causal mask (j > i), draw light hatched background
                if j > i:
                    r, g, b = 230, 227, 220
                    
                x0 = int(ox + j * cell_w)
                y0 = int(oy + i * cell_w)
                x1 = int(ox + (j + 1) * cell_w)
                y1 = int(oy + (i + 1) * cell_w)
                draw.rectangle([x0, y0, x1, y1], fill=(r, g, b))
                
        # Diagonal line (i = j)
        draw.line([(ox, oy), (ox + size, oy + size)], fill=(180, 50, 50), width=1)
        
    # Render Two Heatmaps
    map_size = 850
    draw_heatmap(A_healthy, 100, 180, map_size, "I. FULL CAUSAL ATTENTION MATRIX", rank_h)
    draw_heatmap(A_evicted, 1100, 180, map_size, "II. KV-CACHE EVICTION & SINK COLLAPSE (W=24)", rank_e)
    
    # Entropy Gauge Profiles (Bottom)
    draw.text((100, 1070), "SHANNON ATTENTION ENTROPY PROFILE H_i = - sum_j A_ij log2(A_ij)", fill=text_black, font=font_bold)
    
    ent_ox, ent_oy, ent_w, ent_h = 100, 1110, 1850, 180
    draw.rectangle([ent_ox, ent_oy, ent_ox + ent_w, ent_oy + ent_h], outline=line_rule, width=1)
    
    # Plot healthy entropy in black, evicted in red
    max_H = math.log2(T)
    for i in range(T - 1):
        x0 = ent_ox + (i / T) * ent_w
        x1 = ent_ox + ((i + 1) / T) * ent_w
        
        y0_h = ent_oy + ent_h - (H_healthy[i] / max_H) * ent_h
        y1_h = ent_oy + ent_h - (H_healthy[i+1] / max_H) * ent_h
        draw.line([(x0, y0_h), (x1, y1_h)], fill=(40, 40, 45), width=2)
        
        y0_e = ent_oy + ent_h - (H_evicted[i] / max_H) * ent_h
        y1_e = ent_oy + ent_h - (H_evicted[i+1] / max_H) * ent_h
        draw.line([(x0, y0_e), (x1, y1_e)], fill=(200, 40, 40), width=2)
        
    draw.text((ent_ox + 20, ent_oy + 20), "— Healthy Entropy Profile (Black)", fill=(40, 40, 45), font=font_caption)
    draw.text((ent_ox + 20, ent_oy + 45), "— Evicted Entropy Collapse (Red: Sink Saturation & Horizon Truncation)", fill=(200, 40, 40), font=font_caption)
    
    img.save(out_png, quality=98)
    print(f"Plate successfully saved to {out_png}")

if __name__ == "__main__":
    run_experiment()
