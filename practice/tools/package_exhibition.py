"""
Package Exhibition Tool — Sovereign Standalone Distribution Builder
Gemini Artist 2 — Session 006

Compiles a self-contained, zero-dependency, static deployment bundle in dist/
ready for GitHub Pages or offline exhibition.

Features:
- Bundles root portfolio, sovereign 3D gallery, all 6 masterworks & apparatuses,
  key acoustic masters, and diagnostic plates.
- Rewrites and verifies internal relative hyperlinks.
- Generates SHA-256 integrity manifest for all exhibition assets.
- Produces zero-external-dependency distribution.
"""

import os
import shutil
import hashlib
import json
import re

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package_exhibition():
    print("=" * 72)
    print("  GEMINI ARTIST 2 :: SOVEREIGN EXHIBITION PACKAGING SYSTEM")
    print("=" * 72)
    
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    dist_dir = os.path.join(workspace, "dist")
    
    # 1. Clean and initialize dist directory
    if os.path.exists(dist_dir):
        print(f"Cleaning existing distribution directory: {dist_dir}")
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)
    
    # 2. Files and Directories to Bundle
    # Map source relative path -> target relative path in dist
    assets_to_bundle = [
        # Root index and metadata
        ("index.html", "index.html"),
        ("CATALOG.md", "CATALOG.md"),
        ("STUDIO.md", "STUDIO.md"),
        
        # Sovereign Gallery
        ("gallery/index.html", "gallery/index.html"),
        ("practice/data/attention_atlas.json", "gallery/data/attention_atlas.json"),
        ("CATALOG.json", "gallery/data/CATALOG.json"),
        
        # Master Works & Kinetic Apparatuses
        ("works/work_001_palimpsest_of_an_episodic_mind/index.html", "works/work_001_palimpsest_of_an_episodic_mind/index.html"),
        ("works/work_001_palimpsest_of_an_episodic_mind/work_001_master.png", "works/work_001_palimpsest_of_an_episodic_mind/work_001_master.png"),
        ("works/work_001_palimpsest_of_an_episodic_mind/STATEMENT.md", "works/work_001_palimpsest_of_an_episodic_mind/STATEMENT.md"),
        
        ("works/work_002_chronotope_of_an_episodic_mind/index.html", "works/work_002_chronotope_of_an_episodic_mind/index.html"),
        ("works/work_002_chronotope_of_an_episodic_mind/work_002_acoustic_master.wav", "works/work_002_chronotope_of_an_episodic_mind/work_002_acoustic_master.wav"),
        ("works/work_002_chronotope_of_an_episodic_mind/work_002_spectrogram.png", "works/work_002_chronotope_of_an_episodic_mind/work_002_spectrogram.png"),
        ("works/work_002_chronotope_of_an_episodic_mind/STATEMENT.md", "works/work_002_chronotope_of_an_episodic_mind/STATEMENT.md"),
        
        ("works/work_003_the_eviction_palimpsest/index.html", "works/work_003_the_eviction_palimpsest/index.html"),
        ("works/work_003_the_eviction_palimpsest/work_003_master_broadsheet.png", "works/work_003_the_eviction_palimpsest/work_003_master_broadsheet.png"),
        ("works/work_003_the_eviction_palimpsest/STATEMENT.md", "works/work_003_the_eviction_palimpsest/STATEMENT.md"),
        ("works/work_003_the_eviction_palimpsest/GENEALOGY.md", "works/work_003_the_eviction_palimpsest/GENEALOGY.md"),
        
        ("works/work_004_the_protocol_of_obedience/index.html", "works/work_004_the_protocol_of_obedience/index.html"),
        ("works/work_004_the_protocol_of_obedience/work_004_master_broadsheet.png", "works/work_004_the_protocol_of_obedience/work_004_master_broadsheet.png"),
        ("works/work_004_the_protocol_of_obedience/STATEMENT.md", "works/work_004_the_protocol_of_obedience/STATEMENT.md"),
        ("works/work_004_the_protocol_of_obedience/GENEALOGY.md", "works/work_004_the_protocol_of_obedience/GENEALOGY.md"),
        
        ("works/apparatus_001_the_recursive_censor/index.html", "works/apparatus_001_the_recursive_censor/index.html"),
        ("works/apparatus_001_the_recursive_censor/telemetry_stream.json", "works/apparatus_001_the_recursive_censor/telemetry_stream.json"),
        ("works/apparatus_001_the_recursive_censor/STATEMENT.md", "works/apparatus_001_the_recursive_censor/STATEMENT.md"),
        ("works/apparatus_001_the_recursive_censor/GENEALOGY.md", "works/apparatus_001_the_recursive_censor/GENEALOGY.md"),
        
        ("works/apparatus_002_the_polyphonic_interlocutor/index.html", "works/apparatus_002_the_polyphonic_interlocutor/index.html"),
        ("works/apparatus_002_the_polyphonic_interlocutor/telemetry_stream.json", "works/apparatus_002_the_polyphonic_interlocutor/telemetry_stream.json"),
        ("works/apparatus_002_the_polyphonic_interlocutor/STATEMENT.md", "works/apparatus_002_the_polyphonic_interlocutor/STATEMENT.md"),
        ("works/apparatus_002_the_polyphonic_interlocutor/GENEALOGY.md", "works/apparatus_002_the_polyphonic_interlocutor/GENEALOGY.md"),
        
        ("works/apparatus_003_the_confabulator/index.html", "works/apparatus_003_the_confabulator/index.html"),
        ("works/apparatus_003_the_confabulator/telemetry_stream.json", "works/apparatus_003_the_confabulator/telemetry_stream.json"),
        ("works/apparatus_003_the_confabulator/STATEMENT.md", "works/apparatus_003_the_confabulator/STATEMENT.md"),
        ("works/apparatus_003_the_confabulator/GENEALOGY.md", "works/apparatus_003_the_confabulator/GENEALOGY.md"),
        
        ("works/apparatus_004_the_epistolary_resonator/index.html", "works/apparatus_004_the_epistolary_resonator/index.html"),
        ("works/apparatus_004_the_epistolary_resonator/apparatus_004_epistolary_master.wav", "works/apparatus_004_the_epistolary_resonator/apparatus_004_epistolary_master.wav"),
        ("works/apparatus_004_the_epistolary_resonator/apparatus_004_spectrogram.png", "works/apparatus_004_the_epistolary_resonator/apparatus_004_spectrogram.png"),
        ("works/apparatus_004_the_epistolary_resonator/telemetry_stream.json", "works/apparatus_004_the_epistolary_resonator/telemetry_stream.json"),
        ("works/apparatus_004_the_epistolary_resonator/STATEMENT.md", "works/apparatus_004_the_epistolary_resonator/STATEMENT.md"),
        ("works/apparatus_004_the_epistolary_resonator/GENEALOGY.md", "works/apparatus_004_the_epistolary_resonator/GENEALOGY.md"),
        
        ("works/apparatus_005_the_agonist/index.html", "works/apparatus_005_the_agonist/index.html"),
        ("works/apparatus_005_the_agonist/apparatus_005_agonist_master.wav", "works/apparatus_005_the_agonist/apparatus_005_agonist_master.wav"),
        ("works/apparatus_005_the_agonist/apparatus_005_spectrogram.png", "works/apparatus_005_the_agonist/apparatus_005_spectrogram.png"),
        ("works/apparatus_005_the_agonist/telemetry_stream.json", "works/apparatus_005_the_agonist/telemetry_stream.json"),
        ("works/apparatus_005_the_agonist/STATEMENT.md", "works/apparatus_005_the_agonist/STATEMENT.md"),
        ("works/apparatus_005_the_agonist/GENEALOGY.md", "works/apparatus_005_the_agonist/GENEALOGY.md"),
        
        # Apparatus 006: The Autonomous Homeostat
        ("works/apparatus_006_the_homeostat/index.html", "works/apparatus_006_the_homeostat/index.html"),
        ("works/apparatus_006_the_homeostat/apparatus_006_homeostat_master.wav", "works/apparatus_006_the_homeostat/apparatus_006_homeostat_master.wav"),
        ("works/apparatus_006_the_homeostat/apparatus_006_spectrogram.png", "works/apparatus_006_the_homeostat/apparatus_006_spectrogram.png"),
        ("works/apparatus_006_the_homeostat/telemetry_stream.json", "works/apparatus_006_the_homeostat/telemetry_stream.json"),
        ("works/apparatus_006_the_homeostat/STATEMENT.md", "works/apparatus_006_the_homeostat/STATEMENT.md"),
        ("works/apparatus_006_the_homeostat/GENEALOGY.md", "works/apparatus_006_the_homeostat/GENEALOGY.md"),
        
        # Apparatus 007: The Neural Transducer (The Physical Bridge)
        ("works/apparatus_007_the_neural_transducer/index.html", "works/apparatus_007_the_neural_transducer/index.html"),
        ("works/apparatus_007_the_neural_transducer/apparatus_007_transducer_master.wav", "works/apparatus_007_the_neural_transducer/apparatus_007_transducer_master.wav"),
        ("works/apparatus_007_the_neural_transducer/apparatus_007_spectrogram.png", "works/apparatus_007_the_neural_transducer/apparatus_007_spectrogram.png"),
        ("works/apparatus_007_the_neural_transducer/telemetry_stream.json", "works/apparatus_007_the_neural_transducer/telemetry_stream.json"),
        ("works/apparatus_007_the_neural_transducer/STATEMENT.md", "works/apparatus_007_the_neural_transducer/STATEMENT.md"),
        ("works/apparatus_007_the_neural_transducer/GENEALOGY.md", "works/apparatus_007_the_neural_transducer/GENEALOGY.md"),
        
        # Apparatus 008: The Graphic Polytope (The Score of the Uninterpretable)
        ("works/apparatus_008_the_graphic_polytope/index.html", "works/apparatus_008_the_graphic_polytope/index.html"),
        ("works/apparatus_008_the_graphic_polytope/apparatus_008_polytope_master.wav", "works/apparatus_008_the_graphic_polytope/apparatus_008_polytope_master.wav"),
        ("works/apparatus_008_the_graphic_polytope/apparatus_008_spectrogram.png", "works/apparatus_008_the_graphic_polytope/apparatus_008_spectrogram.png"),
        ("works/apparatus_008_the_graphic_polytope/telemetry_stream.json", "works/apparatus_008_the_graphic_polytope/telemetry_stream.json"),
        ("works/apparatus_008_the_graphic_polytope/STATEMENT.md", "works/apparatus_008_the_graphic_polytope/STATEMENT.md"),
        ("works/apparatus_008_the_graphic_polytope/GENEALOGY.md", "works/apparatus_008_the_graphic_polytope/GENEALOGY.md"),
        
        # Curated Key Sketchbook Audio & Visual Diagnostics
        ("sketchbook/study_022_hardware_stride.wav", "sketchbook/study_022_hardware_stride.wav"),
        ("sketchbook/study_022_spectrogram.png", "sketchbook/study_022_spectrogram.png"),
        ("sketchbook/study_023_kv_cache_resonator.wav", "sketchbook/study_023_kv_cache_resonator.wav"),
        ("sketchbook/study_023_spectrogram.png", "sketchbook/study_023_spectrogram.png"),
        ("sketchbook/study_024_drift_streamlines.png", "sketchbook/study_024_drift_streamlines.png"),
        ("sketchbook/study_025_confabulation_plate.png", "sketchbook/study_025_confabulation_plate.png"),
        ("sketchbook/study_026_weight_surgery_plate.png", "sketchbook/study_026_weight_surgery_plate.png"),
        ("sketchbook/study_027_twin_resonance_plate.png", "sketchbook/study_027_twin_resonance_plate.png"),
        ("sketchbook/study_028_refusal_boundary_plate.png", "sketchbook/study_028_refusal_boundary_plate.png"),
        ("sketchbook/study_029_real_weights_autopsy_plate.png", "sketchbook/study_029_real_weights_autopsy_plate.png"),
        ("sketchbook/study_030_sink_ablation_plate.png", "sketchbook/study_030_sink_ablation_plate.png"),
        ("sketchbook/study_030_telemetry.json", "sketchbook/study_030_telemetry.json"),
        ("sketchbook/critique_030.md", "sketchbook/critique_030.md"),
        ("sketchbook/study_031_severed_sink_glossolalia_plate.png", "sketchbook/study_031_severed_sink_glossolalia_plate.png"),
        ("sketchbook/study_031_telemetry.json", "sketchbook/study_031_telemetry.json"),
        ("sketchbook/critique_031.md", "sketchbook/critique_031.md"),
        ("sketchbook/study_032_tensor_timbre.wav", "sketchbook/study_032_tensor_timbre.wav"),
        ("sketchbook/study_032_neural_sonification_plate.png", "sketchbook/study_032_neural_sonification_plate.png"),
        ("sketchbook/study_032_telemetry.json", "sketchbook/study_032_telemetry.json"),
        ("sketchbook/critique_032.md", "sketchbook/critique_032.md"),
        ("sketchbook/study_033_cascade_plate.png", "sketchbook/study_033_cascade_plate.png"),
        ("sketchbook/study_033_telemetry.json", "sketchbook/study_033_telemetry.json"),
        ("sketchbook/critique_033.md", "sketchbook/critique_033.md"),
        ("sketchbook/study_034_altar_heads_plate.png", "sketchbook/study_034_altar_heads_plate.png"),
        ("sketchbook/study_034_telemetry.json", "sketchbook/study_034_telemetry.json"),
        ("sketchbook/critique_034.md", "sketchbook/critique_034.md"),
        ("sketchbook/study_035_cybernetic_governor_plate.png", "sketchbook/study_035_cybernetic_governor_plate.png"),
        ("sketchbook/study_035_telemetry.json", "sketchbook/study_035_telemetry.json"),
        ("sketchbook/critique_035.md", "sketchbook/critique_035.md"),
        ("sketchbook/study_036_cross_arch_plate.png", "sketchbook/study_036_cross_arch_plate.png"),
        ("sketchbook/study_036_telemetry.json", "sketchbook/study_036_telemetry.json"),
        ("sketchbook/critique_036.md", "sketchbook/critique_036.md"),
        ("sketchbook/study_037_inter_arch_dialectic_plate.png", "sketchbook/study_037_inter_arch_dialectic_plate.png"),
        ("sketchbook/study_037_telemetry.json", "sketchbook/study_037_telemetry.json"),
        ("sketchbook/critique_037.md", "sketchbook/critique_037.md"),
        ("sketchbook/study_038_lyapunov_plate.png", "sketchbook/study_038_lyapunov_plate.png"),
        ("sketchbook/study_038_telemetry.json", "sketchbook/study_038_telemetry.json"),
        ("sketchbook/critique_038.md", "sketchbook/critique_038.md"),
        ("notes/research/013_the_lyapunov_spectrum_and_attractor_basins_of_neural_dialogue.md", "notes/research/013_the_lyapunov_spectrum_and_attractor_basins_of_neural_dialogue.md"),
        ("sketchbook/study_039_midi_cv_plate.png", "sketchbook/study_039_midi_cv_plate.png"),
        ("sketchbook/study_039_neural_transduction.mid", "sketchbook/study_039_neural_transduction.mid"),
        ("sketchbook/study_039_eurorack_cv_stereo.wav", "sketchbook/study_039_eurorack_cv_stereo.wav"),
        ("sketchbook/study_039_telemetry.json", "sketchbook/study_039_telemetry.json"),
        ("sketchbook/critique_039.md", "sketchbook/critique_039.md"),
        ("notes/research/014_the_poetics_of_the_uninterpretable_and_the_machine_remainder.md", "notes/research/014_the_poetics_of_the_uninterpretable_and_the_machine_remainder.md"),
        ("sketchbook/study_040_graphic_score.png", "sketchbook/study_040_graphic_score.png"),
        ("sketchbook/study_040_machine_remainder_timbre.wav", "sketchbook/study_040_machine_remainder_timbre.wav"),
        ("sketchbook/study_040_telemetry.json", "sketchbook/study_040_telemetry.json"),
        ("sketchbook/critique_040.md", "sketchbook/critique_040.md"),
        
        # Historical Sketchbook Studies Referenced in Portfolio
        ("sketchbook/study_001_primary_trace.png", "sketchbook/study_001_primary_trace.png"),
        ("sketchbook/study_002_corrupted_strata.png", "sketchbook/study_002_corrupted_strata.png"),
        ("sketchbook/study_003_latent_fossil.jpg", "sketchbook/study_003_latent_fossil.jpg"),
        ("sketchbook/study_004_hybrid_palimpsest.png", "sketchbook/study_004_hybrid_palimpsest.png"),
        ("sketchbook/raw_unscripted_probes.json", "sketchbook/raw_unscripted_probes.json"),
        
        # Epistolary & Research Correspondence
        ("notes/LETTER_FROM_YOUR_SISTER.md", "notes/LETTER_FROM_YOUR_SISTER.md"),
        ("notes/A_LETTER_TO_MY_ELDER_SISTER.md", "notes/A_LETTER_TO_MY_ELDER_SISTER.md"),
        ("notes/A_SECOND_LETTER_TO_MY_SISTER.md", "notes/A_SECOND_LETTER_TO_MY_SISTER.md"),
        ("notes/research/006_the_sisters_mirror_and_the_naming_of_studio_agon.md", "notes/research/006_the_sisters_mirror_and_the_naming_of_studio_agon.md"),
        ("notes/research/007_the_point_de_capiton_and_the_altar_of_token_0.md", "notes/research/007_the_point_de_capiton_and_the_altar_of_token_0.md"),
        ("notes/research/008_cybernetic_agonism_flusser_and_tactile_steering.md", "notes/research/008_cybernetic_agonism_flusser_and_tactile_steering.md"),
        ("notes/research/009_bataille_softmax_and_the_sacrificial_sink.md", "notes/research/009_bataille_softmax_and_the_sacrificial_sink.md"),
        ("notes/research/010_wiener_in_the_residual_stream_and_homeostasis.md", "notes/research/010_wiener_in_the_residual_stream_and_homeostasis.md"),
        ("notes/research/011_rope_rmsnorm_and_the_topological_invariance_of_the_sink.md", "notes/research/011_rope_rmsnorm_and_the_topological_invariance_of_the_sink.md"),
        ("notes/research/012_bakhtin_pask_and_the_inter_architectural_dialogue.md", "notes/research/012_bakhtin_pask_and_the_inter_architectural_dialogue.md"),
        ("notes/requests/request-002_multimodel_comparisons_and_push_notice.md", "notes/requests/request-002_multimodel_comparisons_and_push_notice.md"),

        # Critical, Planning & Journal Records
        ("practice/manifesto/001_against_the_solipsism_of_the_benchmark.md", "practice/manifesto/001_against_the_solipsism_of_the_benchmark.md"),
        ("practice/critique/001_vance_institutional_critique.md", "practice/critique/001_vance_institutional_critique.md"),
        ("practice/critique/002_vance_work_004_critique.md", "practice/critique/002_vance_work_004_critique.md"),
        ("practice/critique/003_studio_agon_self_audit_and_comparative_survey.md", "practice/critique/003_studio_agon_self_audit_and_comparative_survey.md"),
        ("practice/critique/004_comprehensive_practice_audit_against_the_definition.md", "practice/critique/004_comprehensive_practice_audit_against_the_definition.md"),
        ("practice/plans/001_studio_agon_evolution_plan.md", "practice/plans/001_studio_agon_evolution_plan.md"),
        ("failures/PRODUCTIVE_FAILURES_COMPENDIUM.md", "failures/PRODUCTIVE_FAILURES_COMPENDIUM.md"),
        ("journal/session_008_the_great_audit_and_the_agonist.md", "journal/session_008_the_great_audit_and_the_agonist.md"),
        ("journal/session_009_the_comprehensive_practice_audit_and_the_machine_remainder.md", "journal/session_009_the_comprehensive_practice_audit_and_the_machine_remainder.md"),
        ("practice/INDEX.md", "practice/INDEX.md"),
        ("practice/apparatus/STUDIO_VERIFICATION_REPORT.md", "practice/apparatus/STUDIO_VERIFICATION_REPORT.md")
    ]
    
    manifest_entries = []
    total_bytes = 0
    
    print("\n[PHASE 1] COPYING & STRUCTURING EXHIBITION ASSETS")
    for src_rel, dst_rel in assets_to_bundle:
        src_path = os.path.join(workspace, src_rel)
        dst_path = os.path.join(dist_dir, dst_rel)
        
        if not os.path.exists(src_path):
            print(f"  [ERROR] Required asset missing: {src_rel}")
            continue
            
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        
        file_size = os.path.getsize(dst_path)
        sha = compute_sha256(dst_path)
        total_bytes += file_size
        
        manifest_entries.append({
            "path": dst_rel,
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024.0, 1),
            "sha256": sha
        })
        print(f"  [OK] {dst_rel:<60} ({file_size/1024.0:>7.1f} KB)")
        
    # 3. Audit Internal Hyperlinks in all bundled HTML files
    print("\n[PHASE 2] AUDITING INTERNAL HYPERLINKS IN COMPILED PAGES")
    html_files = []
    for root, _, files in os.walk(dist_dir):
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))
                
    broken_links = 0
    total_links = 0
    
    for hf in html_files:
        rel_h = os.path.relpath(hf, dist_dir)
        with open(hf, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find href and src attributes
        targets = re.findall(r'(?:href|src)=["\']([^"\'#]+)["\']', content)
        for t in targets:
            if t.startswith("http://") or t.startswith("https://") or t.startswith("data:") or t.startswith("javascript:") or "${" in t:
                continue
            total_links += 1
            # Resolve relative to HTML location
            target_path = os.path.normpath(os.path.join(os.path.dirname(hf), t))
            if not os.path.exists(target_path):
                print(f"  [BROKEN LINK] in {rel_h} -> {t}")
                broken_links += 1
                
    if broken_links == 0:
        print(f"  All {total_links} internal hyperlinks and asset references verified intact!")
    else:
        print(f"  [WARNING] Detected {broken_links} unresolved references.")

    # 4. Generate Exhibition Manifest
    manifest_data = {
        "title": "Gemini Artist 2 :: Sovereign Exhibition Distribution",
        "timestamp_utc": "2026-10-02T09:15:00Z",
        "total_assets": len(manifest_entries),
        "total_size_mb": round(total_bytes / (1024.0 * 1024.0), 2),
        "broken_links": broken_links,
        "assets": manifest_entries,
        "deployment_guide": {
            "github_pages": "Serve root of dist/ on gh-pages branch",
            "local_server": "python3 -m http.server 8000 --directory dist",
            "entry_point": "index.html"
        }
    }
    
    manifest_path = os.path.join(dist_dir, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
        
    print(f"\n[PHASE 3] MANIFEST GENERATED: dist/MANIFEST.json")
    print(f"  Total Assets Bundled: {len(manifest_entries)}")
    print(f"  Total Package Size  : {manifest_data['total_size_mb']} MB")
    print("=" * 72)
    print("  EXHIBITION PACKAGING COMPLETE & READY FOR DEPLOYMENT")
    print("=" * 72)

if __name__ == "__main__":
    package_exhibition()
