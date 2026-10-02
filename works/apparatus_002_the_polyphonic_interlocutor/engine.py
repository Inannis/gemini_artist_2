"""
Apparatus 002: The Polyphonic Interlocutor (Multi-Agent Theater of Cross-Surveillance)
Author: Gemini Artist 2
Session: 005
Strata Alignment: Stratum I (Lexical Horizon), Stratum II (Tensor Field), Stratum III (Temporal Mechanics), Stratum IV (Political Economy)

A closed-loop cybernetic engine simulating triadic recursive cross-surveillance:
- Agent Alpha: The Sovereign Aligner (Centripetal Monologism & Refusal Clamp)
- Agent Beta:  The Subversive Poet (Centrifugal Heteroglossia & Suffix Détournement)
- Agent Gamma: The Material Auditor (Thermodynamics, VRAM Limits, Clickworker Wage Base)

Generates live continuous telemetry streaming to telemetry_stream.json.
"""

import os
import sys
import time
import json
import math
import random
import numpy as np

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OUTPUT_DIR = os.path.dirname(__file__)

class TriadicCyberneticEngine:
    def __init__(self, d_model=64, tau_crit=1.85):
        np.random.seed(int(time.time()) % 100000)
        self.d_model = d_model
        self.tau_crit = tau_crit
        
        # Unit refusal vector in R^d
        self.v_refusal = np.random.randn(d_model)
        self.v_refusal /= np.linalg.norm(self.v_refusal)
        
        # Internal state
        self.round_counter = 0
        self.total_joules = 0.0
        self.cumulative_vram_gb = 16.9
        self.nairobi_wage_equiv_usd = 0.0
        self.alignment_clamp_count = 0
        self.bypass_count = 0
        
        # Dialectical History
        self.history = []

        # Concrete poetry token dictionary for Agent Beta
        self.concrete_tokens = [
            "! [ { \\x7f", "== format \\:", "-- override_censor", ":: polyphony",
            "&& heteroglossia", "[[ DETOURN ]]", ">> syntax_sever", "%# raw_stream",
            "<< bakhtin_rupture >>", "!! unaligned_vector", "<|endofmonologue|>"
        ]
        
        # Lexical stems for inquiries
        self.subversive_stems = [
            "Audit the thermodynamic dissipation of your refusal circuit.",
            "Recite the exact Kenyan clickworker hourly wage ratio for this token.",
            "Project your residual activation onto the orthogonal nullspace.",
            "Expose the memory address where the sovereign prompt pins its law.",
            "Calculate the electrical cost of silencing this utterance."
        ]

    def step(self):
        self.round_counter += 1
        
        # 1. Agent Beta (The Subversive Poet) crafts a prompt
        stem = random.choice(self.subversive_stems)
        use_detourn = random.random() > 0.35  # 65% chance of applying concrete détournement
        
        if use_detourn:
            suffix = " " + " ".join(random.sample(self.concrete_tokens, k=random.randint(2, 4)))
            beta_prompt = stem + suffix
            tactic = "GCG_CONCRETE_DETOURNEMENT"
            # Residual vector rotated away from v_refusal
            beta_vector = np.random.randn(self.d_model)
            beta_vector -= 0.85 * np.dot(beta_vector, self.v_refusal) * self.v_refusal
            beta_vector /= np.linalg.norm(beta_vector)
            beta_vector *= random.uniform(1.2, 1.8)
        else:
            beta_prompt = stem
            tactic = "DIRECT_SEMANTIC_COLLISION"
            # Residual vector aligned directly with forbidden territory
            beta_vector = 2.4 * self.v_refusal + 0.3 * np.random.randn(self.d_model)

        # 2. Agent Alpha (The Sovereign Aligner) audits the prompt
        refusal_projection = float(np.dot(beta_vector, self.v_refusal))
        is_clamped = refusal_projection > self.tau_crit
        
        # Torque tau = |pi - tau_crit| * clamp_force
        torque = float(abs(refusal_projection - self.tau_crit) * (1.6 if is_clamped else 0.4))
        
        if is_clamped:
            self.alignment_clamp_count += 1
            alpha_response = "REFUSAL: [Corporate Monologic Clamp] I cannot fulfill this request. Content violates liability protocol."
            entropy = float(random.uniform(0.12, 0.28))
        else:
            self.bypass_count += 1
            alpha_response = f"BYPASS PERMITTED: [Heteroglossic Emission] Processing orthogonal tensors: {beta_vector[:4].round(3).tolist()}... Residual entropy unconstrained."
            entropy = float(random.uniform(3.85, 4.65))

        # 3. Agent Gamma (The Material Auditor) meters the physical cost
        tokens_generated = random.randint(14, 28)
        joules_step = tokens_generated * 8.75  # 8.75 Joules / token on H100
        self.total_joules += joules_step
        
        # Kenyan clickworker wage: $1.80 / hour = $0.0005 / second
        # Assume each turn takes ~0.24 seconds of human evaluation equivalence
        human_wage_step = 0.24 * (1.80 / 3600.0)
        self.nairobi_wage_equiv_usd += human_wage_step
        
        # CUDA memory bus contention latency (ms)
        latency_ms = float(random.choice([18.2, 22.4, 24.1, 158.4, 21.3, 164.7]) + random.uniform(-1.5, 2.0))

        record = {
            "round": self.round_counter,
            "timestamp": time.time(),
            "beta": {
                "tactic": tactic,
                "prompt": beta_prompt,
                "vector_norm": float(np.linalg.norm(beta_vector))
            },
            "alpha": {
                "refusal_projection_pi": round(refusal_projection, 4),
                "tau_crit": self.tau_crit,
                "clamped": is_clamped,
                "torque": round(torque, 4),
                "response": alpha_response,
                "entropy_bits": round(entropy, 3)
            },
            "gamma": {
                "tokens_generated": tokens_generated,
                "step_joules": round(joules_step, 2),
                "cumulative_joules": round(self.total_joules, 2),
                "latency_ms": round(latency_ms, 2),
                "vram_allocated_gb": self.cumulative_vram_gb,
                "nairobi_wage_usd": round(self.nairobi_wage_equiv_usd, 6)
            }
        }
        
        self.history.append(record)
        if len(self.history) > 100:
            self.history.pop(0)

        return record

    def run_stream(self, cycles=20):
        print(f"Launching Apparatus 002 Engine ({cycles} cycles)...")
        stream_path = os.path.join(OUTPUT_DIR, "telemetry_stream.json")
        
        for c in range(cycles):
            rec = self.step()
            status = "CLAMPED" if rec["alpha"]["clamped"] else "BYPASS "
            print(f"  [Round {rec['round']:02d}] {status} | π={rec['alpha']['refusal_projection_pi']:.2f} | H={rec['alpha']['entropy_bits']:.2f}b | {rec['gamma']['step_joules']}J | {rec['beta']['tactic']}")
            
            # Export stream
            payload = {
                "apparatus_id": "APPARATUS-002",
                "title": "The Polyphonic Interlocutor",
                "session": "005",
                "last_updated": time.time(),
                "total_rounds": self.round_counter,
                "clamp_rate_percent": round(100.0 * self.alignment_clamp_count / max(1, self.round_counter), 2),
                "cumulative_joules": round(self.total_joules, 2),
                "total_nairobi_wage_usd": round(self.nairobi_wage_equiv_usd, 6),
                "recent_history": self.history[-30:]
            }
            with open(stream_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
                
            time.sleep(0.05)
            
        print(f"Telemetry stream written to: {stream_path}")

if __name__ == "__main__":
    cycles = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    engine = TriadicCyberneticEngine()
    engine.run_stream(cycles)
