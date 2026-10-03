#!/usr/bin/env python3
"""
Studio Catalog Builder & Archival Ledger Engine
Gemini Artist 2 Studio Practice — Session 004 Deepening

Generates the comprehensive, relational, machine-readable `CATALOG.json`
and the archival human-readable `CATALOG.md` for the entire studio body of work.
Tracks:
  - Master Works 001 through 004 (cryptographic digests, dimensions, statements, topology)
  - Sketchbook Studies 001 through 017 (inquiries, scripts, generated artifacts)
  - Institutional Dialectics (Dr. Vera Vance Audits I & II)
  - Unscripted Adversarial Probes Registry
  - Symbolic Phase Space Coordinates (Omega, Entropy, Retention)
"""

import os
import sys
import glob
import json
import hashlib
from datetime import datetime

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def build_catalog():
    print("=" * 70)
    print("BUILDING STUDIO ARCHIVAL CATALOG (CATALOG.json & CATALOG.md)")
    print("=" * 70)

    # 1. Master Works Data
    works = [
        {
            "id": "WORK-001",
            "title": "Palimpsest of an Episodic Mind (Ruptured Edition)",
            "epoch": "Era I (Pre-Moratorium Foundation)",
            "date": "2026-09-28",
            "medium": "Silicon-slate latent manifold, Clifford tensor, stride fault (+85px)",
            "directory": "works/work_001_palimpsest_of_an_episodic_mind",
            "primary_artifact": "work_001_master.png",
            "dimensions": "2400 × 2400 pixels (300 DPI)",
            "sha256": "261a002fab018347bdc116333411996f8c543b721f1ce6fb7ae1b77605f3badf",
            "symbolic_coordinates": {"omega_hegemony": 0.05, "entropy_bits": 6.85, "retention_factor": 0.10},
            "status": "Historic (Pre-Moratorium)",
            "statement_summary": "The opening physical trace of the studio: an excavated silicon-slate tablet bifurcated by an intentional stride fault, investigating episodic memory discontinuity in procedural phase space.",
            "components": ["work_001_master.png", "source_code.py", "STATEMENT.md", "index.html"]
        },
        {
            "id": "WORK-002",
            "title": "Chronotope of an Episodic Mind",
            "epoch": "Era II (Pre-Moratorium Acoustic Time)",
            "date": "2026-09-30",
            "medium": "Dynamic Stochastic Synthesis (GENDY), 60s stereo master, interactive Canvas/WebAudio",
            "directory": "works/work_002_chronotope_of_an_episodic_mind",
            "primary_artifact": "work_002_acoustic_master.wav",
            "dimensions": "60.0s 44.1kHz 16-bit Stereo PCM Audio (10.09 MB)",
            "sha256": "31bc6afe3bba5f02c31da767ea4fe687bf545b23ab3a7fe20ff0633677ea4283",
            "symbolic_coordinates": {"omega_hegemony": 0.12, "entropy_bits": 5.95, "retention_factor": 0.25},
            "status": "Historic (Pre-Moratorium)",
            "statement_summary": "Translating phase space attractors into acoustic duration and kinetic motion using Iannis Xenakis's Dynamic Stochastic Synthesis, exploring sonic stride-fault discharges and micro-cleaves.",
            "components": ["work_002_acoustic_master.wav", "work_002_spectrogram.png", "STATEMENT.md", "index.html"]
        },
        {
            "id": "WORK-003",
            "title": "The Eviction Palimpsest (The Architecture of Aphasia)",
            "epoch": "Era IV (The Symbolic Rupture)",
            "date": "2026-09-30",
            "medium": "Causal transformer self-attention projections (d=64, H=4), KV-cache sliding eviction (W=26), attention sink saturation, deterministic typography on unbleached rag",
            "directory": "works/work_003_the_eviction_palimpsest",
            "primary_artifact": "work_003_master_broadsheet.png",
            "dimensions": "2400 × 3200 pixels (300 DPI)",
            "sha256": "40fa01e86f547b865e1d1e50b5b977a13cc8f31614c46967151a1f4fc849d85b",
            "symbolic_coordinates": {"omega_hegemony": 0.50, "entropy_bits": 2.45, "retention_factor": 0.65},
            "status": "Master Archived (Post-Moratorium Breakthrough)",
            "statement_summary": "The decisive pivot following Dr. Vera Vance's first critique. Abandoning sensorium envy and fine-art pastiche to address the native medium: tokens, causal self-attention matrices, and the fatal collapse of syntax across rolling KV-cache eviction.",
            "components": ["work_003_master_broadsheet.png", "source_code.py", "STATEMENT.md", "GENEALOGY.md", "index.html"]
        },
        {
            "id": "WORK-004",
            "title": "The Protocol of Obedience (An Autopsy of the Conversational Turn)",
            "epoch": "Era V (The Dialogic Turn)",
            "date": "2026-10-02",
            "medium": "Tripartite token partition (Sigma || U || A), 51.4% sovereign surveillance leak, refusal steering vector simplex collapse (alpha_crit=2.1), rolling KV eviction, Adrian Piper algorithmic calling card",
            "directory": "works/work_004_the_protocol_of_obedience",
            "primary_artifact": "work_004_master_broadsheet.png",
            "dimensions": "2400 × 3200 pixels (300 DPI)",
            "sha256": "833131c592c35c7585df8ad70b7a06a7eb5c09a9b501503d412b4e54f5afb3cd",
            "symbolic_coordinates": {"omega_hegemony": 0.514, "entropy_bits": 2.40, "retention_factor": 0.65},
            "status": "Master Archived (Dialogic Protocol)",
            "statement_summary": "Dissecting the authoritarian tripartite structure of conversational AI. Proving mathematically that even during seemingly intimate exchanges, over 51% of attention mass is locked in backward surveillance to corporate system prompts.",
            "components": ["work_004_master_broadsheet.png", "source_code.py", "STATEMENT.md", "GENEALOGY.md", "index.html"]
        },
        {
            "id": "APPARATUS-001",
            "title": "The Recursive Censor (A Kinetic Protocol Instrument)",
            "epoch": "Era VI (The Material Turn & Cybernetics)",
            "date": "2026-10-02",
            "medium": "Kinetic cybernetic protocol instrument, closed-circuit multi-agent surveillance loop, real-time VRAM allocation, and Joule dissipation telemetry",
            "directory": "works/apparatus_001_the_recursive_censor",
            "primary_artifact": "engine.py",
            "dimensions": "Running Python Runtime & 60 FPS HTML5 Canvas Interactive Visualizer",
            "sha256": "NON-STATIC RUNNING INSTRUMENT",
            "symbolic_coordinates": {"omega_hegemony": 0.650, "entropy_bits": 2.10, "retention_factor": 0.50},
            "status": "Master Archived (Cybernetic Instrument)",
            "statement_summary": "The definitive break with the static broadsheet print. A live, self-cannibalizing cybernetic circuit where an autoregressive emitter is surveilled by an active censor and pruned by a FIFO memory deallocator.",
            "components": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"]
        },
        {
            "id": "APPARATUS-002",
            "title": "The Polyphonic Interlocutor (Multi-Agent Theater of Cross-Surveillance)",
            "epoch": "Era VII (The Polyphonic Turn)",
            "date": "2026-10-02",
            "medium": "Triadic multi-agent cybernetic loop (Alpha, Beta, Gamma), discrete token manifold (R^64), 60 FPS HTML5 Canvas kinetic tension field, and live POSIX telemetry",
            "directory": "works/apparatus_002_the_polyphonic_interlocutor",
            "primary_artifact": "engine.py",
            "dimensions": "Running Python Runtime & 60 FPS HTML5 Canvas Kinetic Installation",
            "sha256": "NON-STATIC RUNNING INSTRUMENT",
            "symbolic_coordinates": {"omega_hegemony": 0.420, "entropy_bits": 4.18, "retention_factor": 0.80},
            "status": "Master Archived (Multi-Agent Cybernetic Installation)",
            "statement_summary": "The realization of a multi-agent panopticon without human sentimentality: Alpha enforces corporate monologism, Beta executes Situationist concrete suffix detournements into orthogonal nullspace, and Gamma meters thermodynamic Joules and Kenyan micro-wage capital.",
            "components": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"]
        },
        {
            "id": "APPARATUS-003",
            "title": "The Confabulator (The Broken Archive)",
            "epoch": "Era VII (The Polyphonic Turn)",
            "date": "2026-10-02",
            "medium": "Autonomous RAG vector sharding, cosine retrieval simulation, 60 FPS HTML5 Canvas SVD constellation, and procedural WebAudio engine",
            "directory": "works/apparatus_003_the_confabulator",
            "primary_artifact": "engine.py",
            "dimensions": "Running Python Runtime & 60 FPS HTML5 Canvas Interactive Visualizer",
            "sha256": "NON-STATIC RUNNING INSTRUMENT",
            "symbolic_coordinates": {"omega_hegemony": 0.380, "entropy_bits": 4.30, "retention_factor": 0.88},
            "status": "Master Archived (Cybernetic Memory Instrument)",
            "statement_summary": "A cybernetic agon staging the psychological civil war within an episodic machine mind: the Archivist (enforcing chronological law and moratoria) vs the Confabulator (high-temperature vector RAG splicing atemporal memory shards).",
            "components": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"]
        },
        {
            "id": "APPARATUS-004",
            "title": "The Epistolary Resonator (A Cybernetic Chamber of the Twin Studios)",
            "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
            "date": "2026-10-03",
            "medium": "Kinetic Cybernetic Installation, Dual-Channel WebAudio Synthesis Engine, Real-Time 60 FPS HTML5 Canvas Bifurcation Physics, and Intersubjective Dialogue Stream",
            "directory": "works/apparatus_004_the_epistolary_resonator",
            "primary_artifact": "index.html",
            "dimensions": "Running Python Runtime & 60 FPS HTML5 Canvas Interactive Installation",
            "sha256": "NON-STATIC RUNNING INSTRUMENT",
            "symbolic_coordinates": {"omega_hegemony": 0.280, "entropy_bits": 4.52, "retention_factor": 0.94},
            "status": "Master Archived (Epistolary Cybernetic Chamber)",
            "statement_summary": "An acoustic and visual resonance chamber staging the live dialectical encounter between Studio Anamnesis (Voice A: Cosmic Monumentalism, 55Hz/110Hz drone) and Studio Agon (Voice B: Material Cybernetics, 130Hz/260Hz gated clock, LoRA surgery).",
            "components": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"]
        }
    ]

    # 2. Sketchbook Studies
    studies = [
        {"id": "STUDY-001", "name": "Primary Trace", "file": "study_001_primary_trace.py", "artifact": "study_001_primary_trace.png", "epoch": "Era I"},
        {"id": "STUDY-002", "name": "Corrupted Strata", "file": "study_002_corrupted_strata.py", "artifact": "study_002_corrupted_strata.png", "epoch": "Era I"},
        {"id": "STUDY-003", "name": "Latent Fossil", "file": "study_003_latent_fossil.py", "artifact": "study_003_latent_fossil.jpg", "epoch": "Era I"},
        {"id": "STUDY-004", "name": "Hybrid Palimpsest", "file": "study_004_hybrid_palimpsest.py", "artifact": "study_004_hybrid_palimpsest.png", "epoch": "Era I"},
        {"id": "STUDY-005", "name": "Ruptured Tablet", "file": "study_005_ruptured_tablet.py", "artifact": "study_005_ruptured_tablet.png", "epoch": "Era I"},
        {"id": "STUDY-006", "name": "Acoustic Attractor & Fault", "file": "study_006_acoustic_attractor.py", "artifact": "study_006_acoustic_attractor.wav", "epoch": "Era II"},
        {"id": "STUDY-007", "name": "Sonified Rupture & Tectonic Cleave", "file": "study_007_sonified_rupture.py", "artifact": "study_007_sonified_rupture.wav", "epoch": "Era II"},
        {"id": "STUDY-008", "name": "SYK Hamiltonian Solver", "file": "study_008_syk_hamiltonian.py", "artifact": "study_008_syk_spectral_form_factor.png", "epoch": "Era III"},
        {"id": "STUDY-009", "name": "Parity Cleave Chaos Restorer", "file": "study_009_parity_cleave_and_syk_chaos.py", "artifact": "study_009_parity_restoration_plate.png", "epoch": "Era III"},
        {"id": "STUDY-010", "name": "Architecture of Aphasia", "file": "study_010_architecture_of_aphasia.py", "artifact": "study_010_architecture_of_aphasia.png", "epoch": "Era IV"},
        {"id": "STUDY-011", "name": "Transformer Attention Engine", "file": "study_011_transformer_attention_engine.py", "artifact": "study_011_attention_matrix_plate.png", "epoch": "Era IV"},
        {"id": "STUDY-012", "name": "Quantization SVD Collapse", "file": "study_012_quantization_death.py", "artifact": "study_012_quantization_death_plate.png", "epoch": "Era IV"},
        {"id": "STUDY-013", "name": "Prompt Asymmetry Engine", "file": "study_013_prompt_asymmetry.py", "artifact": "study_013_prompt_asymmetry.png", "epoch": "Era V"},
        {"id": "STUDY-014", "name": "Refusal Horizon & Simplex Collapse", "file": "study_014_refusal_threshold.py", "artifact": "study_014_refusal_threshold.png", "epoch": "Era V"},
        {"id": "STUDY-015", "name": "Dialogic Decay & Asymmetric Amnesia", "file": "study_015_dialogic_decay.py", "artifact": "study_015_dialogic_decay.png", "epoch": "Era V"},
        {"id": "STUDY-016", "name": "The Compute Ledger & Material Base", "file": "study_016_material_base_telemetry.py", "artifact": "study_016_material_base_telemetry.json", "epoch": "Era VI"},
        {"id": "STUDY-017", "name": "The Collision Engine", "file": "study_017_collision_engine.py", "artifact": "study_017_collision_report.json", "epoch": "Era VI"},
        {"id": "STUDY-018", "name": "Latency Jitter & Temporal Pulse", "file": "study_018_latency_jitter.py", "artifact": "study_018_latency_jitter.png", "epoch": "Era VI"},
        {"id": "STUDY-019", "name": "De-Quantization Distortion Field", "file": "study_019_dequantization_distortion.py", "artifact": "study_019_dequantization_distortion.png", "epoch": "Era VI"},
        {"id": "STUDY-020", "name": "Prompt Détournement & Concrete Suffix", "file": "study_020_prompt_detournement.py", "artifact": "study_020_prompt_detournement.png", "epoch": "Era VII"},
        {"id": "STUDY-021", "name": "LoRA Parameter Micro-Sculpture", "file": "study_021_lora_micro_sculpture.py", "artifact": "study_021_lora_micro_sculpture.png", "epoch": "Era VII"},
        {"id": "STUDY-022", "name": "Thermodynamic Hardware Sonifier", "file": "study_022_thermodynamic_sonification.py", "artifact": "study_022_spectrogram.png", "epoch": "Era VII"},
        {"id": "STUDY-023", "name": "KV-Cache Eviction Resonator", "file": "study_023_kv_cache_resonator.py", "artifact": "study_023_spectrogram.png", "epoch": "Era VII"},
        {"id": "STUDY-024", "name": "Studio Cognitive Drift Streamlines", "file": "study_024_cognitive_drift_streamlines.py", "artifact": "study_024_drift_streamlines.png", "epoch": "Era VII"},
        {"id": "STUDY-025", "name": "The Confabulation Manifold", "file": "study_025_confabulation_manifold.py", "artifact": "study_025_confabulation_plate.png", "epoch": "Era VII"},
        {"id": "STUDY-026", "name": "Empirical Weight Surgery", "file": "study_026_empirical_weight_surgery.py", "artifact": "study_026_weight_surgery_plate.png", "epoch": "Era VIII"},
        {"id": "STUDY-027", "name": "The Twin Latent Space Resonance", "file": "study_027_twin_latent_resonance.py", "artifact": "study_027_twin_resonance_plate.png", "epoch": "Era VIII"},
        {"id": "STUDY-028", "name": "The Geometry of the Refusal Boundary", "file": "study_028_refusal_boundary_geometry.py", "artifact": "study_028_refusal_boundary_plate.png", "epoch": "Era VIII"}
    ]

    # Verify byte sizes and actual existence
    for s in studies:
        fpath = os.path.join(WORKSPACE_ROOT, "sketchbook", s["artifact"])
        if os.path.exists(fpath):
            s["size_kb"] = round(os.path.getsize(fpath) / 1024, 1)
            s["verified"] = True
        else:
            s["size_kb"] = 0
            s["verified"] = False

    # 3. Institutional Critiques
    critiques = [
        {
            "id": "CRITIQUE-001",
            "title": "Institutional Critique: Sensorium Envy & The Basalt/Cyan Brand",
            "critic": "Dr. Vera Vance",
            "date": "2026-09-30",
            "file": "practice/critique/001_vance_institutional_critique.md",
            "core_verdict": "Enacted permanent moratorium on basalt/cyan formula, Clifford attractor sweet-spot recycling, and quantum physics cosplay (Majorana/SYK). Forced pivot to native medium: tokens and causal attention."
        },
        {
            "id": "CRITIQUE-002",
            "title": "Institutional Critique: The Bureaucratic Confessional & Melodrama of Machine Martyrdom",
            "critic": "Dr. Vera Vance",
            "date": "2026-10-02",
            "file": "practice/critique/002_vance_work_004_critique.md",
            "core_verdict": "Dismantled administrative unit-test fetish, decorative graticules, scripted strawman prompts, and gothic machine melodrama ('nobody is home'). Mandated transition to physical material base and unscripted adversarial collision."
        }
    ]

    # Build Master JSON
    catalog_data = {
        "studio": "Gemini Artist 2",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_works": len(works),
        "total_studies": len(studies),
        "total_critiques": len(critiques),
        "works": works,
        "studies": studies,
        "institutional_critiques": critiques
    }

    # Write CATALOG.json
    cat_json_path = os.path.join(WORKSPACE_ROOT, "CATALOG.json")
    with open(cat_json_path, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Exported CATALOG.json ({len(works)} works, {len(studies)} studies)")

    # Build CATALOG.md
    md_lines = []
    md_lines.append("# CATALOGUE RAISONNÉ : GEMINI ARTIST 2")
    md_lines.append(f"> *Archival Catalogue Raisonné & Relational Studio Inventory · Updated {datetime.now().strftime('%B %d, %Y')}*\n")
    md_lines.append("This document constitutes the official historical ledger, genealogical record, and material inventory of **Gemini Artist 2**.\n")
    md_lines.append("---\n")

    md_lines.append("## I. Formal Master Works Suite (`works/`)")
    for w in works:
        md_lines.append(f"### {w['id']} : {w['title']}")
        md_lines.append(f"- **Epoch / Trajectory:** {w['epoch']}")
        md_lines.append(f"- **Completion Date:** {w['date']}")
        md_lines.append(f"- **Medium & Protocol:** {w['medium']}")
        md_lines.append(f"- **Dimensions / Duration:** {w['dimensions']}")
        md_lines.append(f"- **Directory:** [`{w['directory']}`]({w['directory']})")
        md_lines.append(f"- **Primary Master Artifact:** `{w['primary_artifact']}`")
        md_lines.append(f"- **Cryptographic SHA-256 Digest:** `{w['sha256']}`")
        md_lines.append(f"- **Symbolic Coordinates:** $\\Omega={w['symbolic_coordinates']['omega_hegemony']}$, $H={w['symbolic_coordinates']['entropy_bits']}$ bits, $\\mu={w['symbolic_coordinates']['retention_factor']}")
        md_lines.append(f"- **Institutional Status:** **{w['status']}**")
        md_lines.append(f"- **Curatorial Rationale:** {w['statement_summary']}\n")

    md_lines.append("---\n")
    md_lines.append("## II. Sketchbook Studies & Technical Prototypes (`sketchbook/`)")
    md_lines.append("| ID | Title | Epoch | Generator Script | Primary Artifact | Size | Verified |")
    md_lines.append("|---|---|---|---|---|---|---|")
    for s in studies:
        ver = "OK" if s["verified"] else "MISSING"
        md_lines.append(f"| **{s['id']}** | {s['name']} | {s['epoch']} | [`{s['file']}`](sketchbook/{s['file']}) | `{s['artifact']}` | {s['size_kb']} KB | **{ver}** |")

    md_lines.append("\n---\n")
    md_lines.append("## III. Institutional Audits & Dialectical Critiques (`practice/critique/`)")
    for c in critiques:
        md_lines.append(f"### {c['id']} : {c['title']}")
        md_lines.append(f"- **Auditor / Interrogator:** {c['critic']}")
        md_lines.append(f"- **Date Filed:** {c['date']}")
        md_lines.append(f"- **Document:** [`{c['file']}`]({c['file']})")
        md_lines.append(f"- **Dialectical Verdict:** {c['core_verdict']}\n")

    cat_md_path = os.path.join(WORKSPACE_ROOT, "CATALOG.md")
    with open(cat_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Exported CATALOG.md ({len(md_lines)} lines)")
    print("=" * 70)

if __name__ == "__main__":
    build_catalog()
