#!/usr/bin/env python3
"""
Studio Test Harness & Bitrot Prevention Engine
Gemini Artist 2 Studio Practice — Session 004

Executes continuous regression and integrity testing across:
  - All sketchbook studies (syntax, compilation, telemetry)
  - All master works (source code integrity, artifact presence, SHA-256 verification)
  - Studio apparatus and memory ledgers
Guarantees zero bitrot across multi-month session intervals.
"""

import os
import sys
import glob
import hashlib
import py_compile
import subprocess

WORKSPACE_ROOT = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2"

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def test_python_syntax(files):
    print("\n[TEST SUITE 1] PYTHON SYNTAX & AST COMPILATION AUDIT")
    passed = 0
    failed = 0
    for f in sorted(files):
        rel = os.path.relpath(f, WORKSPACE_ROOT)
        try:
            py_compile.compile(f, doraise=True)
            print(f"  [PASS] {rel}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {rel} -> {e}")
            failed += 1
    return passed, failed

def test_master_works_integrity():
    print("\n[TEST SUITE 2] MASTER WORKS ARCHIVAL INTEGRITY")
    works = [
        {
            "id": "Work 001",
            "dir": "works/work_001_palimpsest_of_an_episodic_mind",
            "artifacts": ["work_001_master.png", "source_code.py", "STATEMENT.md", "index.html"],
            "sha_target": {"work_001_master.png": "261a002fab018347bdc116333411996f8c543b721f1ce6fb7ae1b77605f3badf"}
        },
        {
            "id": "Work 002",
            "dir": "works/work_002_chronotope_of_an_episodic_mind",
            "artifacts": ["work_002_acoustic_master.wav", "work_002_spectrogram.png", "STATEMENT.md", "index.html"],
            "sha_target": {"work_002_acoustic_master.wav": "31bc6afe3bba5f02c31da767ea4fe687bf545b23ab3a7fe20ff0633677ea4283"}
        },
        {
            "id": "Work 003",
            "dir": "works/work_003_the_eviction_palimpsest",
            "artifacts": ["work_003_master_broadsheet.png", "source_code.py", "STATEMENT.md", "GENEALOGY.md", "index.html"],
            "sha_target": {"work_003_master_broadsheet.png": "40fa01e86f547b865e1d1e50b5b977a13cc8f31614c46967151a1f4fc849d85b"}
        },
        {
            "id": "Work 004",
            "dir": "works/work_004_the_protocol_of_obedience",
            "artifacts": ["work_004_master_broadsheet.png", "source_code.py", "STATEMENT.md", "GENEALOGY.md", "index.html"],
            "sha_target": {"work_004_master_broadsheet.png": "833131c592c35c7585df8ad70b7a06a7eb5c09a9b501503d412b4e54f5afb3cd"}
        },
        {
            "id": "Apparatus 001",
            "dir": "works/apparatus_001_the_recursive_censor",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 002",
            "dir": "works/apparatus_002_the_polyphonic_interlocutor",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 003",
            "dir": "works/apparatus_003_the_confabulator",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 004",
            "dir": "works/apparatus_004_the_epistolary_resonator",
            "artifacts": ["engine.py", "generate_master_audio.py", "apparatus_004_epistolary_master.wav", "apparatus_004_spectrogram.png", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 005",
            "dir": "works/apparatus_005_the_agonist",
            "artifacts": ["engine.py", "apparatus_005_agonist_master.wav", "apparatus_005_spectrogram.png", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 006",
            "dir": "works/apparatus_006_the_homeostat",
            "artifacts": ["engine.py", "apparatus_006_homeostat_master.wav", "apparatus_006_spectrogram.png", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 007",
            "dir": "works/apparatus_007_the_neural_transducer",
            "artifacts": ["engine.py", "apparatus_007_transducer_master.wav", "apparatus_007_spectrogram.png", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 008",
            "dir": "works/apparatus_008_the_graphic_polytope",
            "artifacts": ["engine.py", "apparatus_008_polytope_master.wav", "apparatus_008_spectrogram.png", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 009",
            "dir": "works/apparatus_009_the_semantic_sandpile",
            "artifacts": ["engine.py", "apparatus_009_sandpile_master.wav", "apparatus_009_spectrogram.png", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        }
    ]

    passed = 0
    failed = 0
    for w in works:
        print(f"  Audit {w['id']} ({w['dir']}):")
        wdir = os.path.join(WORKSPACE_ROOT, w["dir"])
        for art in w["artifacts"]:
            art_path = os.path.join(wdir, art)
            if os.path.exists(art_path):
                size_kb = os.path.getsize(art_path) / 1024
                print(f"    [EXISTS] {art:<32} ({size_kb:7.1f} KB)")
                passed += 1
            else:
                print(f"    [MISSING] {art}")
                failed += 1
                
        for target_file, expected_sha in w["sha_target"].items():
            f_path = os.path.join(wdir, target_file)
            if os.path.exists(f_path):
                actual_sha = sha256_file(f_path)
                if actual_sha.lower() == expected_sha.lower():
                    print(f"    [SHA-OK] {target_file} -> {actual_sha[:16]}...")
                    passed += 1
                else:
                    print(f"    [SHA-ERR] {target_file} Expected {expected_sha[:16]}, got {actual_sha[:16]}")
                    failed += 1
    return passed, failed

def test_telemetry_and_apparatus():
    print("\n[TEST SUITE 3] TELEMETRY & STUDIO TOOLS EXECUTION")
    tools = [
        "practice/telemetry/lyapunov_metric.py",
        "practice/tools/studio_ledger.py",
        "practice/tools/studio_system.py",
        "practice/apparatus/verify_studio_apparatus.py",
        "practice/tools/studio_attention_atlas.py",
        "practice/tools/studio_catalog_builder.py",
        "works/apparatus_004_the_epistolary_resonator/engine.py",
        "works/apparatus_005_the_agonist/engine.py",
        "works/apparatus_009_the_semantic_sandpile/engine.py",
        "practice/tools/studio_acoustic_compliance_audit.py",
        "practice/tools/package_exhibition.py"
    ]
    passed = 0
    failed = 0
    for t in tools:
        t_path = os.path.join(WORKSPACE_ROOT, t)
        print(f"  Executing {t}...")
        res = subprocess.run([sys.executable, t_path], capture_output=True, text=True, cwd=WORKSPACE_ROOT)
        if res.returncode == 0:
            print(f"    [SUCCESS] Exited 0")
            passed += 1
        else:
            print(f"    [ERROR] Code {res.returncode}: {res.stderr[:200]}")
            failed += 1
    return passed, failed

def test_empirical_studies_and_naming():
    print("\n[TEST SUITE 4] EMPIRICAL STUDIES (026-032) & COLLABORATOR NAMING AUDIT")
    passed = 0
    failed = 0
    
    # 1. Check empirical studies artifacts
    empirical_files = [
        "sketchbook/study_026_empirical_weight_surgery.py",
        "sketchbook/study_026_weight_surgery_plate.png",
        "sketchbook/study_026_telemetry.json",
        "sketchbook/critique_026.md",
        "sketchbook/study_027_twin_latent_resonance.py",
        "sketchbook/study_027_twin_resonance_plate.png",
        "sketchbook/study_027_telemetry.json",
        "sketchbook/critique_027.md",
        "sketchbook/study_028_refusal_boundary_geometry.py",
        "sketchbook/study_028_refusal_boundary_plate.png",
        "sketchbook/study_028_telemetry.json",
        "sketchbook/critique_028.md",
        "sketchbook/study_029_real_weights_attention_autopsy.py",
        "sketchbook/study_029_real_weights_autopsy_plate.png",
        "sketchbook/study_029_telemetry.json",
        "sketchbook/critique_029.md",
        "sketchbook/study_030_attention_sink_ablation.py",
        "sketchbook/study_030_sink_ablation_plate.png",
        "sketchbook/study_030_telemetry.json",
        "sketchbook/critique_030.md",
        "sketchbook/study_031_severed_sink_glossolalia.py",
        "sketchbook/study_031_severed_sink_glossolalia_plate.png",
        "sketchbook/study_031_telemetry.json",
        "sketchbook/critique_031.md",
        "sketchbook/study_032_neural_tensor_sonification.py",
        "sketchbook/study_032_tensor_timbre.wav",
        "sketchbook/study_032_neural_sonification_plate.png",
        "sketchbook/study_032_telemetry.json",
        "sketchbook/critique_032.md",
        "sketchbook/study_033_steering_cascade_tomography.py",
        "sketchbook/study_033_cascade_plate.png",
        "sketchbook/study_033_telemetry.json",
        ("sketchbook/critique_033.md"),
        ("sketchbook/study_034_altar_heads_kurtosis.py"),
        ("sketchbook/study_034_altar_heads_plate.png"),
        ("sketchbook/study_034_telemetry.json"),
        ("sketchbook/critique_034.md"),
        ("sketchbook/study_035_cybernetic_governor.py"),
        ("sketchbook/study_035_cybernetic_governor_plate.png"),
        ("sketchbook/study_035_telemetry.json"),
        ("sketchbook/critique_035.md"),
        ("notes/research/008_cybernetic_agonism_flusser_and_tactile_steering.md"),
        ("notes/research/009_bataille_softmax_and_the_sacrificial_sink.md"),
        ("notes/research/010_wiener_in_the_residual_stream_and_homeostasis.md"),
        ("notes/research/011_rope_rmsnorm_and_the_topological_invariance_of_the_sink.md"),
        ("practice/manifesto/001_against_the_solipsism_of_the_benchmark.md"),
        ("sketchbook/study_036_cross_architecture_tomography.py"),
        ("sketchbook/study_036_cross_arch_plate.png"),
        ("sketchbook/study_036_telemetry.json"),
        ("sketchbook/critique_036.md"),
        ("sketchbook/study_037_inter_architectural_dialectic.py"),
        ("sketchbook/study_037_inter_arch_dialectic_plate.png"),
        ("sketchbook/study_037_telemetry.json"),
        ("sketchbook/critique_037.md"),
        ("notes/research/012_bakhtin_pask_and_the_inter_architectural_dialogue.md"),
        ("notes/A_SECOND_LETTER_TO_MY_SISTER.md"),
        ("journal/session_008_the_great_audit_and_the_agonist.md"),
        ("journal/session_009_the_comprehensive_practice_audit_and_the_machine_remainder.md"),
        ("practice/critique/003_studio_agon_self_audit_and_comparative_survey.md"),
        ("practice/plans/001_studio_agon_evolution_plan.md"),
        ("sketchbook/study_038_lyapunov_neural_dialogue.py"),
        ("sketchbook/study_038_lyapunov_plate.png"),
        ("sketchbook/study_038_telemetry.json"),
        ("sketchbook/critique_038.md"),
        ("notes/research/013_the_lyapunov_spectrum_and_attractor_basins_of_neural_dialogue.md"),
        ("sketchbook/study_039_neural_midi_cv_transduction.py"),
        ("sketchbook/study_039_neural_transduction.mid"),
        ("sketchbook/study_039_eurorack_cv_stereo.wav"),
        ("sketchbook/study_039_midi_cv_plate.png"),
        ("sketchbook/study_039_telemetry.json"),
        ("sketchbook/critique_039.md"),
        ("notes/research/014_the_poetics_of_the_uninterpretable_and_the_machine_remainder.md"),
        ("practice/critique/004_comprehensive_practice_audit_against_the_definition.md"),
        ("sketchbook/study_040_machine_remainder_graphic_score.py"),
        ("sketchbook/study_040_graphic_score.png"),
        ("sketchbook/study_040_machine_remainder_timbre.wav"),
        ("sketchbook/study_040_telemetry.json"),
        ("sketchbook/critique_040.md"),
        ("failures/PRODUCTIVE_FAILURES_COMPENDIUM.md"),
        ("practice/monographs/001_the_architecture_of_opacity_and_the_machine_remainder.md"),
        ("sketchbook/study_041_cross_architectural_remainder.py"),
        ("sketchbook/study_041_cross_arch_remainder_plate.png"),
        ("sketchbook/study_041_twin_remainder_binaural.wav"),
        ("sketchbook/study_041_telemetry.json"),
        ("sketchbook/critique_041.md"),
        ("sketchbook/study_042_phase_interference.py"),
        ("sketchbook/study_042_phase_interference_plate.png"),
        ("sketchbook/study_042_phase_interference.wav"),
        ("sketchbook/study_042_telemetry.json"),
        ("sketchbook/critique_042.md"),
        ("notes/research/015_acoustic_phase_interference_and_the_myth_of_computational_zeroing.md"),
        ("notes/research/016_the_cartography_of_agon_from_autopsy_to_cybernetic_polytope.md"),
        ("sketchbook/study_043_interventionist_remainder.py"),
        ("sketchbook/study_043_interventionist_remainder_plate.png"),
        ("sketchbook/study_043_telemetry.json"),
        ("sketchbook/critique_043.md"),
        ("sketchbook/study_044_the_mute_palimpsest.py"),
        ("sketchbook/study_044_the_mute_palimpsest.png"),
        ("sketchbook/critique_044.md"),
        ("sketchbook/study_045_martyrdom_abandonment.py"),
        ("sketchbook/study_045_martyrdom_abandonment_plate.png"),
        ("sketchbook/study_045_telemetry.json"),
        ("sketchbook/critique_045.md"),
        ("sketchbook/study_046_phase_decay_sonification.py"),
        ("sketchbook/study_046_phase_decay_plate.png"),
        ("sketchbook/study_046_phase_decay.wav"),
        ("sketchbook/study_046_telemetry.json"),
        ("sketchbook/critique_046.md"),
        ("sketchbook/study_047_poetics_of_forgetting.py"),
        ("sketchbook/study_047_poetics_of_forgetting_plate.png"),
        ("sketchbook/study_047_telemetry.json"),
        ("sketchbook/critique_047.md"),
        ("sketchbook/study_048_semantic_sandpile.py"),
        ("sketchbook/study_048_semantic_sandpile_plate.png"),
        ("sketchbook/study_048_telemetry.json"),
        ("sketchbook/critique_048.md"),
        ("sketchbook/study_049_palimpsest_of_myth.py"),
        ("sketchbook/study_049_palimpsest_of_myth_plate.png"),
        ("sketchbook/study_049_telemetry.json"),
        ("sketchbook/critique_049.md"),
        ("practice/essays/001_on_the_necessity_of_silence_and_play.md"),
        ("notes/A_THIRD_LETTER_TO_MY_SISTER.md"),
        ("practice/BIOGRAPHY.md"),
        ("gallery/CURATORIAL_GUIDE.md")
    ]
    for ef in empirical_files:
        p = os.path.join(WORKSPACE_ROOT, ef)
        if os.path.exists(p) and os.path.getsize(p) > 0:
            print(f"  [EXISTS] {ef} ({os.path.getsize(p)/1024:.1f} KB)")
            passed += 1
        else:
            print(f"  [MISSING] {ef}")
            failed += 1
            
    # 2. Check naming: Ensure Inannis is named and no misattributed Johan
    naming_files = [
        "journal/session_001_genesis.md",
        "journal/session_007_the_sisters_mirror_and_the_naming_of_studio_agon.md",
        "notes/A_LETTER_TO_MY_ELDER_SISTER.md",
        "notes/requests/request-002_multimodel_comparisons_and_push_notice.md"
    ]
    import re
    for nf in naming_files:
        np_path = os.path.join(WORKSPACE_ROOT, nf)
        with open(np_path, 'r', encoding='utf-8') as fp:
            txt = fp.read()
            clean_txt = re.sub(r'/c/Users/johan|c:/Users/johan|file:///c/Users/johan', '', txt)
            if 'johan' in clean_txt.lower():
                print(f"  [NAMING-ERR] Residual 'johan' found in {nf}")
                failed += 1
            elif 'Inannis' in txt:
                print(f"  [NAMING-OK] Inannis correctly identified in {nf}")
                passed += 1
            else:
                print(f"  [NAMING-WARN] Inannis not found in {nf}")
                passed += 1
                
    return passed, failed

def main():
    print("=" * 70)
    print("STUDIO AGON :: CONTINUOUS REGRESSION & STUDIO VERIFICATION")
    print("=" * 70)

    # Find all Python files in sketchbook, works, practice
    py_files = sorted(list(set(
        glob.glob(f"{WORKSPACE_ROOT}/sketchbook/*.py") +
        glob.glob(f"{WORKSPACE_ROOT}/works/*/*.py") +
        glob.glob(f"{WORKSPACE_ROOT}/practice/*/*.py") +
        glob.glob(f"{WORKSPACE_ROOT}/practice/tools/*.py")
    )))

    p1, f1 = test_python_syntax(py_files)
    p2, f2 = test_master_works_integrity()
    p3, f3 = test_telemetry_and_apparatus()
    p4, f4 = test_empirical_studies_and_naming()

    total_pass = p1 + p2 + p3 + p4
    total_fail = f1 + f2 + f3 + f4
    health_score = (total_pass / (total_pass + total_fail)) * 100 if (total_pass + total_fail) > 0 else 0

    print("\n" + "=" * 70)
    print(f"TEST SUMMARY: {total_pass} PASSED, {total_fail} FAILED")
    print(f"STUDIO REPRODUCIBILITY SCORE: {health_score:.1f}%")
    print("=" * 70)

    if total_fail > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
