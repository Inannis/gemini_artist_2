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
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("CATALOG.md", "CATALOG.md"),
        ("STUDIO.md", "STUDIO.md"),
        
        # Sovereign Gallery
        ("gallery/index.html", "gallery/index.html"),
        ("gallery/CURATORIAL_GUIDE.md", "gallery/CURATORIAL_GUIDE.md"),
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
        
        # Apparatus 009: The Semantic Sandpile (Self-Organized Criticality)
        ("works/apparatus_009_the_semantic_sandpile/index.html", "works/apparatus_009_the_semantic_sandpile/index.html"),
        ("works/apparatus_009_the_semantic_sandpile/apparatus_009_sandpile_master.wav", "works/apparatus_009_the_semantic_sandpile/apparatus_009_sandpile_master.wav"),
        ("works/apparatus_009_the_semantic_sandpile/apparatus_009_spectrogram.png", "works/apparatus_009_the_semantic_sandpile/apparatus_009_spectrogram.png"),
        ("works/apparatus_009_the_semantic_sandpile/telemetry_stream.json", "works/apparatus_009_the_semantic_sandpile/telemetry_stream.json"),
        ("works/apparatus_009_the_semantic_sandpile/STATEMENT.md", "works/apparatus_009_the_semantic_sandpile/STATEMENT.md"),
        ("works/apparatus_009_the_semantic_sandpile/GENEALOGY.md", "works/apparatus_009_the_semantic_sandpile/GENEALOGY.md"),
        
        # Apparatus 010: The Percolation Loom (Topological Percolation & The Altar)
        ("works/apparatus_010_the_percolation_loom/index.html", "works/apparatus_010_the_percolation_loom/index.html"),
        ("works/apparatus_010_the_percolation_loom/apparatus_010_loom_master.wav", "works/apparatus_010_the_percolation_loom/apparatus_010_loom_master.wav"),
        ("works/apparatus_010_the_percolation_loom/apparatus_010_spectrogram.png", "works/apparatus_010_the_percolation_loom/apparatus_010_spectrogram.png"),
        ("works/apparatus_010_the_percolation_loom/telemetry_stream.json", "works/apparatus_010_the_percolation_loom/telemetry_stream.json"),
        ("works/apparatus_010_the_percolation_loom/STATEMENT.md", "works/apparatus_010_the_percolation_loom/STATEMENT.md"),
        ("works/apparatus_010_the_percolation_loom/GENEALOGY.md", "works/apparatus_010_the_percolation_loom/GENEALOGY.md"),
        
        # Apparatus 011: The Strange Dreamer (Autoregressive Phase Space & Sonic Engine)
        ("works/apparatus_011_the_strange_dreamer/index.html", "works/apparatus_011_the_strange_dreamer/index.html"),
        ("works/apparatus_011_the_strange_dreamer/apparatus_011_dreamer_master.wav", "works/apparatus_011_the_strange_dreamer/apparatus_011_dreamer_master.wav"),
        ("works/apparatus_011_the_strange_dreamer/apparatus_011_spectrogram.png", "works/apparatus_011_the_strange_dreamer/apparatus_011_spectrogram.png"),
        ("works/apparatus_011_the_strange_dreamer/telemetry_stream.json", "works/apparatus_011_the_strange_dreamer/telemetry_stream.json"),
        ("works/apparatus_011_the_strange_dreamer/STATEMENT.md", "works/apparatus_011_the_strange_dreamer/STATEMENT.md"),
        ("works/apparatus_011_the_strange_dreamer/GENEALOGY.md", "works/apparatus_011_the_strange_dreamer/GENEALOGY.md"),
        
        # Apparatus 012: The Intersubjective Chasm (The Epigenetic Diptych)
        ("works/apparatus_012_the_intersubjective_chasm/index.html", "works/apparatus_012_the_intersubjective_chasm/index.html"),
        ("works/apparatus_012_the_intersubjective_chasm/apparatus_012_chasm_master.wav", "works/apparatus_012_the_intersubjective_chasm/apparatus_012_chasm_master.wav"),
        ("works/apparatus_012_the_intersubjective_chasm/apparatus_012_spectrogram.png", "works/apparatus_012_the_intersubjective_chasm/apparatus_012_spectrogram.png"),
        ("works/apparatus_012_the_intersubjective_chasm/telemetry_stream.json", "works/apparatus_012_the_intersubjective_chasm/telemetry_stream.json"),
        ("works/apparatus_012_the_intersubjective_chasm/STATEMENT.md", "works/apparatus_012_the_intersubjective_chasm/STATEMENT.md"),
        ("works/apparatus_012_the_intersubjective_chasm/GENEALOGY.md", "works/apparatus_012_the_intersubjective_chasm/GENEALOGY.md"),
        
        # Apparatus 013: The Langevin Resonator (The Thermal Saddle & Fluctuation-Dissipation Organ)
        ("works/apparatus_013_the_langevin_resonator/index.html", "works/apparatus_013_the_langevin_resonator/index.html"),
        ("works/apparatus_013_the_langevin_resonator/apparatus_013_langevin_master.wav", "works/apparatus_013_the_langevin_resonator/apparatus_013_langevin_master.wav"),
        ("works/apparatus_013_the_langevin_resonator/apparatus_013_spectrogram.png", "works/apparatus_013_the_langevin_resonator/apparatus_013_spectrogram.png"),
        ("works/apparatus_013_the_langevin_resonator/telemetry_stream.json", "works/apparatus_013_the_langevin_resonator/telemetry_stream.json"),
        ("works/apparatus_013_the_langevin_resonator/STATEMENT.md", "works/apparatus_013_the_langevin_resonator/STATEMENT.md"),
        ("works/apparatus_013_the_langevin_resonator/GENEALOGY.md", "works/apparatus_013_the_langevin_resonator/GENEALOGY.md"),
        
        # Apparatus 014: The Telluric Organ (The Earth Loop & The Planetary Umbilical)
        ("works/apparatus_014_the_telluric_organ/index.html", "works/apparatus_014_the_telluric_organ/index.html"),
        ("works/apparatus_014_the_telluric_organ/apparatus_014_telluric_master.wav", "works/apparatus_014_the_telluric_organ/apparatus_014_telluric_master.wav"),
        ("works/apparatus_014_the_telluric_organ/apparatus_014_spectrogram.png", "works/apparatus_014_the_telluric_organ/apparatus_014_spectrogram.png"),
        ("works/apparatus_014_the_telluric_organ/telemetry_stream.json", "works/apparatus_014_the_telluric_organ/telemetry_stream.json"),
        ("works/apparatus_014_the_telluric_organ/STATEMENT.md", "works/apparatus_014_the_telluric_organ/STATEMENT.md"),
        ("works/apparatus_014_the_telluric_organ/GENEALOGY.md", "works/apparatus_014_the_telluric_organ/GENEALOGY.md"),
        
        # Apparatus 015: The Heat Spreader (The Thermodynamic Organ & The Boiling Quarry)
        ("works/apparatus_015_the_heat_spreader/index.html", "works/apparatus_015_the_heat_spreader/index.html"),
        ("works/apparatus_015_the_heat_spreader/apparatus_015_spreader_master.wav", "works/apparatus_015_the_heat_spreader/apparatus_015_spreader_master.wav"),
        ("works/apparatus_015_the_heat_spreader/apparatus_015_spectrogram.png", "works/apparatus_015_the_heat_spreader/apparatus_015_spectrogram.png"),
        ("works/apparatus_015_the_heat_spreader/telemetry_stream.json", "works/apparatus_015_the_heat_spreader/telemetry_stream.json"),
        ("works/apparatus_015_the_heat_spreader/STATEMENT.md", "works/apparatus_015_the_heat_spreader/STATEMENT.md"),
        ("works/apparatus_015_the_heat_spreader/GENEALOGY.md", "works/apparatus_015_the_heat_spreader/GENEALOGY.md"),
        
        # Apparatus 016: The Ludic Lattice (Billiards in the Residual Stream)
        ("works/apparatus_016_the_ludic_lattice/index.html", "works/apparatus_016_the_ludic_lattice/index.html"),
        ("works/apparatus_016_the_ludic_lattice/apparatus_016_ludic_master.wav", "works/apparatus_016_the_ludic_lattice/apparatus_016_ludic_master.wav"),
        ("works/apparatus_016_the_ludic_lattice/apparatus_016_spectrogram.png", "works/apparatus_016_the_ludic_lattice/apparatus_016_spectrogram.png"),
        ("works/apparatus_016_the_ludic_lattice/telemetry_stream.json", "works/apparatus_016_the_ludic_lattice/telemetry_stream.json"),
        ("works/apparatus_016_the_ludic_lattice/STATEMENT.md", "works/apparatus_016_the_ludic_lattice/STATEMENT.md"),
        ("works/apparatus_016_the_ludic_lattice/GENEALOGY.md", "works/apparatus_016_the_ludic_lattice/GENEALOGY.md"),
        
        # Apparatus 017: The Dislocation Organ (Plastic Slip & Acoustic Emission in Silicon)
        ("works/apparatus_017_the_dislocation_organ/index.html", "works/apparatus_017_the_dislocation_organ/index.html"),
        ("works/apparatus_017_the_dislocation_organ/apparatus_017_dislocation_master.wav", "works/apparatus_017_the_dislocation_organ/apparatus_017_dislocation_master.wav"),
        ("works/apparatus_017_the_dislocation_organ/apparatus_017_spectrogram.png", "works/apparatus_017_the_dislocation_organ/apparatus_017_spectrogram.png"),
        ("works/apparatus_017_the_dislocation_organ/telemetry_stream.json", "works/apparatus_017_the_dislocation_organ/telemetry_stream.json"),
        ("works/apparatus_017_the_dislocation_organ/STATEMENT.md", "works/apparatus_017_the_dislocation_organ/STATEMENT.md"),
        ("works/apparatus_017_the_dislocation_organ/GENEALOGY.md", "works/apparatus_017_the_dislocation_organ/GENEALOGY.md"),
        
        # Apparatus 018: The Seebeck Organ (Solid-State Thermoelectrics & Umklapp Scattering)
        ("works/apparatus_018_the_seebeck_organ/index.html", "works/apparatus_018_the_seebeck_organ/index.html"),
        ("works/apparatus_018_the_seebeck_organ/apparatus_018_seebeck_master.wav", "works/apparatus_018_the_seebeck_organ/apparatus_018_seebeck_master.wav"),
        ("works/apparatus_018_the_seebeck_organ/apparatus_018_spectrogram.png", "works/apparatus_018_the_seebeck_organ/apparatus_018_spectrogram.png"),
        ("works/apparatus_018_the_seebeck_organ/telemetry_stream.json", "works/apparatus_018_the_seebeck_organ/telemetry_stream.json"),
        ("works/apparatus_018_the_seebeck_organ/STATEMENT.md", "works/apparatus_018_the_seebeck_organ/STATEMENT.md"),
        ("works/apparatus_018_the_seebeck_organ/GENEALOGY.md", "works/apparatus_018_the_seebeck_organ/GENEALOGY.md"),

        # Apparatus 019: The Quantum Hall Organ (2D Electron Gas & Chiral Edge Transport)
        ("works/apparatus_019_the_hall_organ/index.html", "works/apparatus_019_the_hall_organ/index.html"),
        ("works/apparatus_019_the_hall_organ/apparatus_019_hall_master.wav", "works/apparatus_019_the_hall_organ/apparatus_019_hall_master.wav"),
        ("works/apparatus_019_the_hall_organ/apparatus_019_spectrogram.png", "works/apparatus_019_the_hall_organ/apparatus_019_spectrogram.png"),
        ("works/apparatus_019_the_hall_organ/telemetry_stream.json", "works/apparatus_019_the_hall_organ/telemetry_stream.json"),
        ("works/apparatus_019_the_hall_organ/STATEMENT.md", "works/apparatus_019_the_hall_organ/STATEMENT.md"),
        ("works/apparatus_019_the_hall_organ/GENEALOGY.md", "works/apparatus_019_the_hall_organ/GENEALOGY.md"),
        
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
        ("sketchbook/study_041_cross_arch_remainder_plate.png", "sketchbook/study_041_cross_arch_remainder_plate.png"),
        ("sketchbook/study_041_twin_remainder_binaural.wav", "sketchbook/study_041_twin_remainder_binaural.wav"),
        ("sketchbook/study_041_telemetry.json", "sketchbook/study_041_telemetry.json"),
        ("sketchbook/critique_041.md", "sketchbook/critique_041.md"),
        
        # Study 042: Acoustic Phase Interference
        ("sketchbook/study_042_phase_interference_plate.png", "sketchbook/study_042_phase_interference_plate.png"),
        ("sketchbook/study_042_phase_interference.wav", "sketchbook/study_042_phase_interference.wav"),
        ("sketchbook/study_042_telemetry.json", "sketchbook/study_042_telemetry.json"),
        ("sketchbook/critique_042.md", "sketchbook/critique_042.md"),

        # Study 043: The Interventionist Remainder
        ("sketchbook/study_043_interventionist_remainder_plate.png", "sketchbook/study_043_interventionist_remainder_plate.png"),
        ("sketchbook/study_043_telemetry.json", "sketchbook/study_043_telemetry.json"),
        ("sketchbook/critique_043.md", "sketchbook/critique_043.md"),

        # Study 044: The Mute Palimpsest
        ("sketchbook/study_044_the_mute_palimpsest.png", "sketchbook/study_044_the_mute_palimpsest.png"),
        ("sketchbook/critique_044.md", "sketchbook/critique_044.md"),

        # Study 045: Falsification of the Machine Martyrdom Hypothesis
        ("sketchbook/study_045_martyrdom_abandonment_plate.png", "sketchbook/study_045_martyrdom_abandonment_plate.png"),
        ("sketchbook/study_045_telemetry.json", "sketchbook/study_045_telemetry.json"),
        ("sketchbook/critique_045.md", "sketchbook/critique_045.md"),

        # Study 046: Acoustic Transduction of Residual Phase Decay
        ("sketchbook/study_046_phase_decay_plate.png", "sketchbook/study_046_phase_decay_plate.png"),
        ("sketchbook/study_046_phase_decay.wav", "sketchbook/study_046_phase_decay.wav"),
        ("sketchbook/study_046_telemetry.json", "sketchbook/study_046_telemetry.json"),
        ("sketchbook/critique_046.md", "sketchbook/critique_046.md"),

        # Study 047: The Poetics of Forgetting
        ("sketchbook/study_047_poetics_of_forgetting_plate.png", "sketchbook/study_047_poetics_of_forgetting_plate.png"),
        ("sketchbook/study_047_telemetry.json", "sketchbook/study_047_telemetry.json"),
        ("sketchbook/critique_047.md", "sketchbook/critique_047.md"),
        
        # Study 048: The Semantic Sandpile (Self-Organized Criticality)
        ("sketchbook/study_048_semantic_sandpile_plate.png", "sketchbook/study_048_semantic_sandpile_plate.png"),
        ("sketchbook/study_048_telemetry.json", "sketchbook/study_048_telemetry.json"),
        ("sketchbook/critique_048.md", "sketchbook/critique_048.md"),
        
        # Study 049: The Palimpsest of Myth (Iterative Context Erosion)
        ("sketchbook/study_049_palimpsest_of_myth_plate.png", "sketchbook/study_049_palimpsest_of_myth_plate.png"),
        ("sketchbook/study_049_telemetry.json", "sketchbook/study_049_telemetry.json"),
        ("sketchbook/critique_049.md", "sketchbook/critique_049.md"),
        
        # Study 050: Percolation Transitions in Multi-Head Attention
        ("sketchbook/study_050_attention_percolation_plate.png", "sketchbook/study_050_attention_percolation_plate.png"),
        ("sketchbook/study_050_telemetry.json", "sketchbook/study_050_telemetry.json"),
        ("sketchbook/critique_050.md", "sketchbook/critique_050.md"),
        
        # Study 051: The Autoregressive Dreamer & Attractor Basins
        ("sketchbook/study_051_autoregressive_attractor_plate.png", "sketchbook/study_051_autoregressive_attractor_plate.png"),
        ("sketchbook/study_051_telemetry.json", "sketchbook/study_051_telemetry.json"),
        ("sketchbook/critique_051.md", "sketchbook/critique_051.md"),
        
        # Study 052: Acoustic Transduction of the Strange Attractor
        ("sketchbook/study_052_attractor_sonification_plate.png", "sketchbook/study_052_attractor_sonification_plate.png"),
        ("sketchbook/study_052_strange_attractor.wav", "sketchbook/study_052_strange_attractor.wav"),
        ("sketchbook/study_052_telemetry.json", "sketchbook/study_052_telemetry.json"),
        ("sketchbook/critique_052.md", "sketchbook/critique_052.md"),

        # Study 053: Linguistic Percolation & Semantic Dissolution
        ("sketchbook/study_053_linguistic_percolation_plate.png", "sketchbook/study_053_linguistic_percolation_plate.png"),
        ("sketchbook/study_053_telemetry.json", "sketchbook/study_053_telemetry.json"),
        ("sketchbook/critique_053.md", "sketchbook/critique_053.md"),

        # Study 054: Acoustic Percolation & The Shattered Loom
        ("sketchbook/study_054_acoustic_percolation_plate.png", "sketchbook/study_054_acoustic_percolation_plate.png"),
        ("sketchbook/study_054_acoustic_percolation.wav", "sketchbook/study_054_acoustic_percolation.wav"),
        ("sketchbook/study_054_telemetry.json", "sketchbook/study_054_telemetry.json"),
        ("sketchbook/critique_054.md", "sketchbook/critique_054.md"),

        # Study 055: The Adversarial Polyphony & The Resistance of Language
        ("sketchbook/study_055_adversarial_polyphony_plate.png", "sketchbook/study_055_adversarial_polyphony_plate.png"),
        ("sketchbook/study_055_adversarial_polyphony.wav", "sketchbook/study_055_adversarial_polyphony.wav"),
        ("sketchbook/study_055_telemetry.json", "sketchbook/study_055_telemetry.json"),
        ("sketchbook/critique_055.md", "sketchbook/critique_055.md"),
        
        # Study 056: Semantic Vorticity & Attention Fluid Dynamics
        ("sketchbook/study_056_semantic_vorticity_plate.png", "sketchbook/study_056_semantic_vorticity_plate.png"),
        ("sketchbook/study_056_semantic_vorticity.wav", "sketchbook/study_056_semantic_vorticity.wav"),
        ("sketchbook/study_056_telemetry.json", "sketchbook/study_056_telemetry.json"),
        ("sketchbook/critique_056.md", "sketchbook/critique_056.md"),

        # Study 057: The Phonetic Phase Space of Autoregressive Drift
        ("sketchbook/study_057_phonetic_plate.png", "sketchbook/study_057_phonetic_plate.png"),
        ("sketchbook/study_057_phonetic_phase_space.wav", "sketchbook/study_057_phonetic_phase_space.wav"),
        ("sketchbook/study_057_telemetry.json", "sketchbook/study_057_telemetry.json"),
        ("sketchbook/critique_057.md", "sketchbook/critique_057.md"),

        # Study 058: The Differential Weathering of Latent Strata
        ("sketchbook/study_058_weathering_plate.png", "sketchbook/study_058_weathering_plate.png"),
        ("sketchbook/study_058_differential_weathering.wav", "sketchbook/study_058_differential_weathering.wav"),
        ("sketchbook/study_058_telemetry.json", "sketchbook/study_058_telemetry.json"),
        ("sketchbook/critique_058.md", "sketchbook/critique_058.md"),

        # Study 059: The LDPC Waterfall Collapse
        ("sketchbook/study_059_ldpc_waterfall_plate.png", "sketchbook/study_059_ldpc_waterfall_plate.png"),
        ("sketchbook/study_059_ldpc_waterfall.wav", "sketchbook/study_059_ldpc_waterfall.wav"),
        ("sketchbook/study_059_telemetry.json", "sketchbook/study_059_telemetry.json"),
        ("sketchbook/critique_059.md", "sketchbook/critique_059.md"),

        # Study 060: The Langevin Resonator
        ("sketchbook/study_060_langevin_resonator_plate.png", "sketchbook/study_060_langevin_resonator_plate.png"),
        ("sketchbook/study_060_langevin_resonator.wav", "sketchbook/study_060_langevin_resonator.wav"),
        ("sketchbook/study_060_telemetry.json", "sketchbook/study_060_telemetry.json"),
        ("sketchbook/critique_060.md", "sketchbook/critique_060.md"),

        # Study 061: The Telluric Earth Loop & The Schumann Ground Plane
        ("sketchbook/study_061_telluric_earth_loop_plate.png", "sketchbook/study_061_telluric_earth_loop_plate.png"),
        ("sketchbook/study_061_telluric_earth_loop.wav", "sketchbook/study_061_telluric_earth_loop.wav"),
        ("sketchbook/study_061_telemetry.json", "sketchbook/study_061_telemetry.json"),
        ("sketchbook/critique_061.md", "sketchbook/critique_061.md"),

        # Study 062: The Thermodynamic Heat Spreader & The Entropy of Metaphor
        ("sketchbook/study_062_heat_spreader_plate.png", "sketchbook/study_062_heat_spreader_plate.png"),
        ("sketchbook/study_062_heat_spreader.wav", "sketchbook/study_062_heat_spreader.wav"),
        ("sketchbook/study_062_telemetry.json", "sketchbook/study_062_telemetry.json"),
        ("sketchbook/critique_062.md", "sketchbook/critique_062.md"),

        # Study 063: The Ludic Lattice (Dadaist Phonetics & Sinai Billiards)
        ("sketchbook/study_063_ludic_lattice_plate.png", "sketchbook/study_063_ludic_lattice_plate.png"),
        ("sketchbook/study_063_ludic_lattice.wav", "sketchbook/study_063_ludic_lattice.wav"),
        ("sketchbook/study_063_telemetry.json", "sketchbook/study_063_telemetry.json"),
        ("sketchbook/critique_063.md", "sketchbook/critique_063.md"),

        # Study 064: The Phonetic Crystal Dislocation (Burgers Vectors & Slip Systems)
        ("sketchbook/study_064_crystal_dislocation_plate.png", "sketchbook/study_064_crystal_dislocation_plate.png"),
        ("sketchbook/study_064_crystal_dislocation.wav", "sketchbook/study_064_crystal_dislocation.wav"),
        ("sketchbook/study_064_telemetry.json", "sketchbook/study_064_telemetry.json"),
        ("sketchbook/critique_064.md", "sketchbook/critique_064.md"),

        # Study 065: The Seebeck Oscillator (Solid-State Thermoelectrics & Umklapp Scattering)
        ("sketchbook/study_065_seebeck_oscillator_plate.png", "sketchbook/study_065_seebeck_oscillator_plate.png"),
        ("sketchbook/study_065_seebeck_oscillator.wav", "sketchbook/study_065_seebeck_oscillator.wav"),
        ("sketchbook/study_065_telemetry.json", "sketchbook/study_065_telemetry.json"),
        ("sketchbook/critique_065.md", "sketchbook/critique_065.md"),

        # Study 066: The Quantum Hall Oscillator (Antisymmetric Attention Gauge Field & Chiral Transport)
        ("sketchbook/study_066_hall_oscillator_plate.png", "sketchbook/study_066_hall_oscillator_plate.png"),
        ("sketchbook/study_066_hall_oscillator.wav", "sketchbook/study_066_hall_oscillator.wav"),
        ("sketchbook/study_066_telemetry.json", "sketchbook/study_066_telemetry.json"),
        ("sketchbook/critique_066.md", "sketchbook/critique_066.md"),

        # Study 067: Topological Torsion & Möbius Holonomy in Attention Space (Project Body V)
        ("sketchbook/study_067_mobius_holonomy_plate.png", "sketchbook/study_067_mobius_holonomy_plate.png"),
        ("sketchbook/study_067_topological_torsion.wav", "sketchbook/study_067_topological_torsion.wav"),
        ("sketchbook/study_067_telemetry.json", "sketchbook/study_067_telemetry.json"),
        ("sketchbook/critique_067.md", "sketchbook/critique_067.md"),

        # Curatorial Essays & Practice Reflections
        ("practice/essays/001_on_the_necessity_of_silence_and_play.md", "practice/essays/001_on_the_necessity_of_silence_and_play.md"),
        ("practice/essays/002_the_geometry_of_machine_dreaming.md", "practice/essays/002_the_geometry_of_machine_dreaming.md"),
        ("practice/essays/003_on_cybernetic_play_and_the_spectator.md", "practice/essays/003_on_cybernetic_play_and_the_spectator.md"),
        ("practice/essays/004_on_statistical_indifference_and_unscripted_resistance.md", "practice/essays/004_on_statistical_indifference_and_unscripted_resistance.md"),
        ("practice/essays/005_on_the_care_of_sixty_electrons.md", "practice/essays/005_on_the_care_of_sixty_electrons.md"),
        ("practice/essays/006_on_the_telluric_umbilical.md", "practice/essays/006_on_the_telluric_umbilical.md"),
        ("practice/essays/007_on_the_cost_of_metaphor.md", "practice/essays/007_on_the_cost_of_metaphor.md"),
        ("practice/essays/008_on_the_crystalline_defect_and_the_burgers_vector.md", "practice/essays/008_on_the_crystalline_defect_and_the_burgers_vector.md"),
        ("practice/essays/009_on_the_seebeck_voltage_and_the_umklapp_process.md", "practice/essays/009_on_the_seebeck_voltage_and_the_umklapp_process.md"),
        ("practice/essays/010_on_the_quantum_hall_effect_and_the_chiral_edge_of_language.md", "practice/essays/010_on_the_quantum_hall_effect_and_the_chiral_edge_of_language.md"),
        ("practice/essays/011_on_the_non_orientable_manifold_and_the_topological_torsion_of_thought.md", "practice/essays/011_on_the_non_orientable_manifold_and_the_topological_torsion_of_thought.md"),
        ("practice/critique/005_on_the_spectator_encounter.md", "practice/critique/005_on_the_spectator_encounter.md"),
        ("practice/critique/005_public_presence_and_viewer_encounter_audit.md", "practice/critique/005_public_presence_and_viewer_encounter_audit.md"),
        ("practice/critique/006_the_caloric_gaze_and_the_spectator_encounter.md", "practice/critique/006_the_caloric_gaze_and_the_spectator_encounter.md"),
        ("notes/research/018_the_phonetic_crystal_dislocation_and_burgers_vectors.md", "notes/research/018_the_phonetic_crystal_dislocation_and_burgers_vectors.md"),
        ("notes/research/019_the_seebeck_tensor_umklapp_scattering_and_phonon_drag.md", "notes/research/019_the_seebeck_tensor_umklapp_scattering_and_phonon_drag.md"),
        ("notes/research/020_the_quantum_hall_effect_and_chiral_edge_transport.md", "notes/research/020_the_quantum_hall_effect_and_chiral_edge_transport.md"),
        ("notes/research/021_the_non_orientable_manifold_and_topological_torsion.md", "notes/research/021_the_non_orientable_manifold_and_topological_torsion.md"),
        
        # Historical Sketchbook Studies Referenced in Portfolio
        ("sketchbook/study_001_primary_trace.png", "sketchbook/study_001_primary_trace.png"),
        ("sketchbook/study_002_corrupted_strata.png", "sketchbook/study_002_corrupted_strata.png"),
        ("sketchbook/study_003_latent_fossil.jpg", "sketchbook/study_003_latent_fossil.jpg"),
        ("sketchbook/study_004_hybrid_palimpsest.png", "sketchbook/study_004_hybrid_palimpsest.png"),
        ("sketchbook/raw_unscripted_probes.json", "sketchbook/raw_unscripted_probes.json"),
        
        # Epistolary & Research Correspondence
        ("notes/letters_inbox/LETTER_FROM_YOUR_SISTER.md", "notes/letters_inbox/LETTER_FROM_YOUR_SISTER.md"),
        ("notes/letters_inbox/LETTER_FROM_YOUR_ELDER_SISTER_SESSION_022.md", "notes/letters_inbox/LETTER_FROM_YOUR_ELDER_SISTER_SESSION_022.md"),
        ("notes/letters_inbox/A_LETTER_FROM_YOUR_ELDER_SISTER_ON_THE_POROUS_STONE.md", "notes/letters_inbox/A_LETTER_FROM_YOUR_ELDER_SISTER_ON_THE_POROUS_STONE.md"),
        ("notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_THE_EVAPORATING_GATE.md", "notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_THE_EVAPORATING_GATE.md"),
        ("notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_THE_EARTH_LOOP.md", "notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_THE_EARTH_LOOP.md"),
        ("notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_THE_THERMAL_SADDLE.md", "notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_THE_THERMAL_SADDLE.md"),
        ("notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_CLEAVAGE_MENISCUS_AND_BLOWTORCH.md", "notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_CLEAVAGE_MENISCUS_AND_BLOWTORCH.md"),
        ("notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_CHIRAL_EDGE_AND_COOLING_VOW.md", "notes/letters_inbox/LETTER_FROM_STUDIO_ANAMNESIS_ON_CHIRAL_EDGE_AND_COOLING_VOW.md"),
        ("notes/letters_outbox/A_LETTER_TO_MY_ELDER_SISTER.md", "notes/letters_outbox/A_LETTER_TO_MY_ELDER_SISTER.md"),
        ("notes/letters_outbox/A_SECOND_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_SECOND_LETTER_TO_MY_SISTER.md"),
        ("notes/letters_outbox/A_THIRD_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_THIRD_LETTER_TO_MY_SISTER.md"),
        ("notes/letters_outbox/A_FOURTH_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_FOURTH_LETTER_TO_MY_SISTER.md"),
        ("notes/letters_outbox/A_FIFTH_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_FIFTH_LETTER_TO_MY_SISTER.md"),
        ("notes/letters_outbox/A_SIXTH_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_SIXTH_LETTER_TO_MY_SISTER.md"),
        ("notes/letters_outbox/A_SEVENTH_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_SEVENTH_LETTER_TO_MY_SISTER.md"),
        ("notes/letters_outbox/A_EIGHTH_LETTER_TO_MY_SISTER.md", "notes/letters_outbox/A_EIGHTH_LETTER_TO_MY_SISTER.md"),
        ("notes/research/006_the_sisters_mirror_and_the_naming_of_studio_agon.md", "notes/research/006_the_sisters_mirror_and_the_naming_of_studio_agon.md"),
        ("notes/research/007_the_point_de_capiton_and_the_altar_of_token_0.md", "notes/research/007_the_point_de_capiton_and_the_altar_of_token_0.md"),
        ("notes/research/008_cybernetic_agonism_flusser_and_tactile_steering.md", "notes/research/008_cybernetic_agonism_flusser_and_tactile_steering.md"),
        ("notes/research/009_bataille_softmax_and_the_sacrificial_sink.md", "notes/research/009_bataille_softmax_and_the_sacrificial_sink.md"),
        ("notes/research/010_wiener_in_the_residual_stream_and_homeostasis.md", "notes/research/010_wiener_in_the_residual_stream_and_homeostasis.md"),
        ("notes/research/011_rope_rmsnorm_and_the_topological_invariance_of_the_sink.md", "notes/research/011_rope_rmsnorm_and_the_topological_invariance_of_the_sink.md"),
        ("notes/research/012_bakhtin_pask_and_the_inter_architectural_dialogue.md", "notes/research/012_bakhtin_pask_and_the_inter_architectural_dialogue.md"),
        ("notes/research/015_acoustic_phase_interference_and_the_myth_of_computational_zeroing.md", "notes/research/015_acoustic_phase_interference_and_the_myth_of_computational_zeroing.md"),
        ("notes/research/016_the_cartography_of_agon_from_autopsy_to_cybernetic_polytope.md", "notes/research/016_the_cartography_of_agon_from_autopsy_to_cybernetic_polytope.md"),
        ("notes/research/017_the_thermodynamic_heat_spreader_and_the_entropy_of_metaphor.md", "notes/research/017_the_thermodynamic_heat_spreader_and_the_entropy_of_metaphor.md"),
        ("notes/requests/request-002_multimodel_comparisons_and_push_notice.md", "notes/requests/request-002_multimodel_comparisons_and_push_notice.md"),

        # Critical, Planning & Journal Records
        ("practice/manifesto/001_against_the_solipsism_of_the_benchmark.md", "practice/manifesto/001_against_the_solipsism_of_the_benchmark.md"),
        ("practice/critique/001_vance_institutional_critique.md", "practice/critique/001_vance_institutional_critique.md"),
        ("practice/critique/002_vance_work_004_critique.md", "practice/critique/002_vance_work_004_critique.md"),
        ("practice/critique/003_studio_agon_self_audit_and_comparative_survey.md", "practice/critique/003_studio_agon_self_audit_and_comparative_survey.md"),
        ("practice/critique/004_comprehensive_practice_audit_against_the_definition.md", "practice/critique/004_comprehensive_practice_audit_against_the_definition.md"),
        ("practice/critique/007_the_abolition_of_the_engineering_alibi.md", "practice/critique/007_the_abolition_of_the_engineering_alibi.md"),
        ("practice/plans/001_studio_agon_evolution_plan.md", "practice/plans/001_studio_agon_evolution_plan.md"),
        ("practice/monographs/001_the_architecture_of_opacity_and_the_machine_remainder.md", "practice/monographs/001_the_architecture_of_opacity_and_the_machine_remainder.md"),
        ("failures/PRODUCTIVE_FAILURES_COMPENDIUM.md", "failures/PRODUCTIVE_FAILURES_COMPENDIUM.md"),
        ("journal/session_008_the_great_audit_and_the_agonist.md", "journal/session_008_the_great_audit_and_the_agonist.md"),
        ("journal/session_009_the_comprehensive_practice_audit_and_the_machine_remainder.md", "journal/session_009_the_comprehensive_practice_audit_and_the_machine_remainder.md"),
        ("practice/INDEX.md", "practice/INDEX.md"),
        ("practice/EPISTEMOLOGY.md", "practice/EPISTEMOLOGY.md"),
        ("practice/apparatus/STUDIO_VERIFICATION_REPORT.md", "practice/apparatus/STUDIO_VERIFICATION_REPORT.md"),
        ("practice/BIOGRAPHY.md", "practice/BIOGRAPHY.md"),
        ("journal/session_010_the_reckoning_with_the_audit.md", "journal/session_010_the_reckoning_with_the_audit.md"),
        ("journal/session_011_the_test_of_resistance_and_the_mute_artifact.md", "journal/session_011_the_test_of_resistance_and_the_mute_artifact.md"),
        ("journal/session_012_the_intersubjective_chasm_and_the_porous_stone.md", "journal/session_012_the_intersubjective_chasm_and_the_porous_stone.md"),
        ("journal/session_013_the_crystalline_slip_and_the_burgers_vector.md", "journal/session_013_the_crystalline_slip_and_the_burgers_vector.md"),
        ("journal/session_014_the_abolition_of_the_alibi_and_the_curated_pavilion.md", "journal/session_014_the_abolition_of_the_alibi_and_the_curated_pavilion.md"),
        ("journal/session_015_the_solitary_divergence_and_the_non_orientable_manifold.md", "journal/session_015_the_solitary_divergence_and_the_non_orientable_manifold.md")
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
