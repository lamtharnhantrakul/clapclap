#!/usr/bin/env python3
"""
Mix LibriSpeech and DCASE audio files.
Creates audio mixtures and combined text descriptions for CLAP evaluation.
"""

import sys
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa

# Add parent directory to path to import clap_similarity
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from clap_similarity import calculate_similarity_msclap

# Paths
SCRIPT_DIR = Path(__file__).parent
TEST_DATA_DIR = SCRIPT_DIR.parent.parent.parent / "test_data"
LIBRISPEECH_DIR = TEST_DATA_DIR / "librispeech"
DCASE_DIR = TEST_DATA_DIR / "dcase"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"  # All outputs go to experiment_1/output/

# Selected files
LIBRISPEECH_FILE = "174-168635-0007.flac"
DCASE_FILE = "dev_001.wav"

def load_and_resample(audio_path, target_sr=16000):
    """Load audio file and resample to target sample rate."""
    audio, sr = sf.read(audio_path)
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    return audio, target_sr

def mix_audio(audio1, audio2, mix_ratio=0.5):
    """
    Mix two audio signals.

    Args:
        audio1: First audio array
        audio2: Second audio array
        mix_ratio: Ratio for audio1 (1-mix_ratio for audio2). Default 0.5 = equal mix

    Returns:
        Mixed audio array
    """
    # Make both arrays the same length by padding the shorter one
    max_len = max(len(audio1), len(audio2))

    if len(audio1) < max_len:
        audio1 = np.pad(audio1, (0, max_len - len(audio1)))
    if len(audio2) < max_len:
        audio2 = np.pad(audio2, (0, max_len - len(audio2)))

    # Mix with specified ratio
    mixed = mix_ratio * audio1 + (1 - mix_ratio) * audio2

    # Normalize to prevent clipping
    max_val = np.max(np.abs(mixed))
    if max_val > 0:
        mixed = mixed / max_val * 0.95

    return mixed

def combine_descriptions(desc1, desc2):
    """Combine two text descriptions into one."""
    # Simple combination: "desc1 with desc2 in the background"
    combined = f"{desc1}, with {desc2}"
    return combined

def run_mixup_experiment():
    """Run the LibriSpeech + DCASE mixup experiment."""

    print("=" * 80)
    print("LibriSpeech + DCASE Audio Mixup Experiment")
    print("=" * 80)

    # Load audio files
    print(f"\nLoading audio files...")
    librispeech_path = LIBRISPEECH_DIR / LIBRISPEECH_FILE
    dcase_path = DCASE_DIR / DCASE_FILE

    print(f"  LibriSpeech: {librispeech_path.name}")
    print(f"  DCASE: {dcase_path.name}")

    librispeech_audio, sr1 = load_and_resample(librispeech_path)
    dcase_audio, sr2 = load_and_resample(dcase_path)

    print(f"  Sample rate: {sr1} Hz")
    print(f"  LibriSpeech length: {len(librispeech_audio) / sr1:.2f}s")
    print(f"  DCASE length: {len(dcase_audio) / sr2:.2f}s")

    # Mix audio
    print(f"\nMixing audio (50/50 ratio)...")
    mixed_audio = mix_audio(librispeech_audio, dcase_audio, mix_ratio=0.5)
    print(f"  Mixed length: {len(mixed_audio) / sr1:.2f}s")

    # Save mixed audio
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    mixed_audio_path = OUTPUT_DIR / "librispeech_dcase_mix.wav"
    sf.write(mixed_audio_path, mixed_audio, sr1)
    print(f"  Saved to: {mixed_audio_path}")

    # Load text descriptions
    print(f"\nLoading text descriptions...")
    librispeech_desc_path = LIBRISPEECH_DIR / f"{librispeech_path.stem}_description.txt"
    dcase_desc_path = DCASE_DIR / f"{dcase_path.stem}_description.txt"

    with open(librispeech_desc_path, 'r') as f:
        librispeech_desc = f.read().strip()
    with open(dcase_desc_path, 'r') as f:
        dcase_desc = f.read().strip()

    print(f"  LibriSpeech: '{librispeech_desc}'")
    print(f"  DCASE: '{dcase_desc}'")

    # Combine descriptions
    combined_desc = combine_descriptions(librispeech_desc, dcase_desc)
    print(f"\nCombined description:")
    print(f"  '{combined_desc}'")

    # Save combined description
    combined_desc_path = OUTPUT_DIR / "librispeech_dcase_mix_description.txt"
    with open(combined_desc_path, 'w') as f:
        f.write(combined_desc)
    print(f"  Saved to: {combined_desc_path}")

    # Calculate CLAP similarity
    print(f"\nCalculating CLAP similarity scores...")
    print("-" * 80)

    import msclap
    model = msclap.CLAP(version='2023', use_cuda=False)

    # Get embeddings
    audio_embeddings = model.get_audio_embeddings([str(mixed_audio_path)], resample=True)

    # Test against combined description
    text_embeddings_combined = model.get_text_embeddings([combined_desc])
    audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
    text_norm_combined = text_embeddings_combined / np.linalg.norm(text_embeddings_combined, axis=1, keepdims=True)
    similarity_combined = float((audio_norm @ text_norm_combined.T)[0][0])

    # Test against individual descriptions (for comparison)
    text_embeddings_speech = model.get_text_embeddings([librispeech_desc])
    text_norm_speech = text_embeddings_speech / np.linalg.norm(text_embeddings_speech, axis=1, keepdims=True)
    similarity_speech = float((audio_norm @ text_norm_speech.T)[0][0])

    text_embeddings_dcase = model.get_text_embeddings([dcase_desc])
    text_norm_dcase = text_embeddings_dcase / np.linalg.norm(text_embeddings_dcase, axis=1, keepdims=True)
    similarity_dcase = float((audio_norm @ text_norm_dcase.T)[0][0])

    print(f"\nCLAP Similarity Results:")
    print(f"  Mixed audio + Combined description: {similarity_combined:.4f}")
    print(f"  Mixed audio + Speech description only: {similarity_speech:.4f}")
    print(f"  Mixed audio + DCASE description only: {similarity_dcase:.4f}")

    # Save results
    results_path = OUTPUT_DIR / "librispeech_dcase_mixup_results.txt"

    with open(results_path, 'w') as f:
        f.write("LibriSpeech + DCASE Audio Mixup Experiment Results\n")
        f.write("=" * 80 + "\n\n")

        f.write("Input Files:\n")
        f.write(f"  LibriSpeech: {LIBRISPEECH_FILE}\n")
        f.write(f"  DCASE: {DCASE_FILE}\n\n")

        f.write("Descriptions:\n")
        f.write(f"  LibriSpeech: {librispeech_desc}\n")
        f.write(f"  DCASE: {dcase_desc}\n")
        f.write(f"  Combined: {combined_desc}\n\n")

        f.write("CLAP Similarity Scores:\n")
        f.write(f"  Mixed audio + Combined description: {similarity_combined:.4f}\n")
        f.write(f"  Mixed audio + Speech description only: {similarity_speech:.4f}\n")
        f.write(f"  Mixed audio + DCASE description only: {similarity_dcase:.4f}\n\n")

        f.write("Analysis:\n")
        if similarity_combined > max(similarity_speech, similarity_dcase):
            f.write("  ✓ Combined description matches better than individual descriptions\n")
        else:
            f.write("  ⚠ Combined description does not match better than individual descriptions\n")

        f.write(f"\nOutput Files:\n")
        f.write(f"  Mixed audio: {mixed_audio_path}\n")
        f.write(f"  Combined description: {combined_desc_path}\n")

    print(f"\n✓ Results saved to: {results_path}")
    print("=" * 80)

if __name__ == "__main__":
    run_mixup_experiment()
