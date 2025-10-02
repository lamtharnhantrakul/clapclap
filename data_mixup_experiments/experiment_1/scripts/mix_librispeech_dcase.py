#!/usr/bin/env python3
"""
Mix LibriSpeech and DCASE audio files.
Creates audio mixtures and combined text descriptions for CLAP evaluation.
"""

import sys
import argparse
import random
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

def combine_descriptions_natural(speech_desc, dcase_desc):
    """
    Combine speech and DCASE descriptions into natural English.

    Args:
        speech_desc: LibriSpeech description (e.g., "a man speaking...")
        dcase_desc: DCASE description (e.g., "a buzzer is ringing...")

    Returns:
        Naturally combined description
    """
    # Extract key components from descriptions
    # Speech descriptions usually start with "a [gender] speaking/person speaking"
    # DCASE descriptions describe ambient sounds

    # Clean up descriptions
    speech = speech_desc.strip()
    ambient = dcase_desc.strip()

    # Remove trailing periods for easier combination
    if speech.endswith('.'):
        speech = speech[:-1]
    if ambient.endswith('.'):
        ambient = ambient[:-1]

    # Create natural combination
    # Pattern: "[speech description] while [ambient sound]"
    combined = f"{speech} while {ambient}"

    return combined

def run_mixup_experiment(num_mixtures=5):
    """
    Run the LibriSpeech + DCASE mixup experiment.

    Args:
        num_mixtures: Number of random audio mixtures to create (default: 5)
    """

    print("=" * 80)
    print(f"LibriSpeech + DCASE Audio Mixup Experiment ({num_mixtures} mixtures)")
    print("=" * 80)

    # Get all available files
    librispeech_files = sorted(LIBRISPEECH_DIR.glob("*.flac"))
    dcase_files = sorted(DCASE_DIR.glob("*.wav"))

    print(f"\nAvailable files:")
    print(f"  LibriSpeech: {len(librispeech_files)} files")
    print(f"  DCASE: {len(dcase_files)} files")

    # Randomly sample pairs
    random.seed(42)  # For reproducibility

    # Create random pairs
    pairs = []
    for i in range(num_mixtures):
        librispeech_file = random.choice(librispeech_files)
        dcase_file = random.choice(dcase_files)
        pairs.append((librispeech_file, dcase_file, i + 1))

    print(f"\nGenerating {num_mixtures} random mixtures...")
    print("=" * 80)

    # Initialize CLAP model once
    import msclap
    model = msclap.CLAP(version='2023', use_cuda=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Store results for summary
    all_results = []

    for librispeech_path, dcase_path, mix_num in pairs:
        print(f"\n[Mixture {mix_num}/{num_mixtures}]")
        print(f"  LibriSpeech: {librispeech_path.name}")
        print(f"  DCASE: {dcase_path.name}")

        # Load audio files
        librispeech_audio, sr1 = load_and_resample(librispeech_path)
        dcase_audio, sr2 = load_and_resample(dcase_path)

        # Mix audio
        mixed_audio = mix_audio(librispeech_audio, dcase_audio, mix_ratio=0.5)

        # Create output filenames with mixture number
        mix_name = f"mix_{mix_num:02d}_{librispeech_path.stem}_{dcase_path.stem}"
        mixed_audio_path = OUTPUT_DIR / f"{mix_name}.wav"

        # Save mixed audio
        sf.write(mixed_audio_path, mixed_audio, sr1)

        # Load text descriptions
        librispeech_desc_path = LIBRISPEECH_DIR / f"{librispeech_path.stem}_description.txt"
        dcase_desc_path = DCASE_DIR / f"{dcase_path.stem}_description.txt"

        with open(librispeech_desc_path, 'r') as f:
            librispeech_desc = f.read().strip()
        with open(dcase_desc_path, 'r') as f:
            dcase_desc = f.read().strip()

        # Combine descriptions naturally
        combined_desc = combine_descriptions_natural(librispeech_desc, dcase_desc)

        # Save combined description
        combined_desc_path = OUTPUT_DIR / f"{mix_name}_description.txt"
        with open(combined_desc_path, 'w') as f:
            f.write(combined_desc)

        print(f"  Combined: '{combined_desc}'")

        # Calculate CLAP similarity
        audio_embeddings = model.get_audio_embeddings([str(mixed_audio_path)], resample=True)

        # Test against combined description
        text_embeddings_combined = model.get_text_embeddings([combined_desc])
        audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
        text_norm_combined = text_embeddings_combined / np.linalg.norm(text_embeddings_combined, axis=1, keepdims=True)
        similarity_combined = float((audio_norm @ text_norm_combined.T)[0][0])

        # Test against individual descriptions
        text_embeddings_speech = model.get_text_embeddings([librispeech_desc])
        text_norm_speech = text_embeddings_speech / np.linalg.norm(text_embeddings_speech, axis=1, keepdims=True)
        similarity_speech = float((audio_norm @ text_norm_speech.T)[0][0])

        text_embeddings_dcase = model.get_text_embeddings([dcase_desc])
        text_norm_dcase = text_embeddings_dcase / np.linalg.norm(text_embeddings_dcase, axis=1, keepdims=True)
        similarity_dcase = float((audio_norm @ text_norm_dcase.T)[0][0])

        print(f"  CLAP Scores - Combined: {similarity_combined:.4f} | Speech: {similarity_speech:.4f} | DCASE: {similarity_dcase:.4f}")

        # Store results
        result = {
            'mix_num': mix_num,
            'librispeech_file': librispeech_path.name,
            'dcase_file': dcase_path.name,
            'librispeech_desc': librispeech_desc,
            'dcase_desc': dcase_desc,
            'combined_desc': combined_desc,
            'similarity_combined': similarity_combined,
            'similarity_speech': similarity_speech,
            'similarity_dcase': similarity_dcase,
            'audio_path': mixed_audio_path,
            'desc_path': combined_desc_path
        }
        all_results.append(result)

    # Save comprehensive results
    print(f"\n{'=' * 80}")
    print("Saving comprehensive results...")
    results_path = OUTPUT_DIR / "experiment_summary.txt"

    with open(results_path, 'w') as f:
        f.write("LibriSpeech + DCASE Audio Mixup Experiment - Summary\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total mixtures created: {num_mixtures}\n\n")

        for result in all_results:
            f.write(f"Mixture {result['mix_num']}:\n")
            f.write(f"  LibriSpeech: {result['librispeech_file']}\n")
            f.write(f"  DCASE: {result['dcase_file']}\n\n")
            f.write(f"  Speech description: {result['librispeech_desc']}\n")
            f.write(f"  DCASE description: {result['dcase_desc']}\n")
            f.write(f"  Combined description: {result['combined_desc']}\n\n")
            f.write(f"  CLAP Similarity Scores:\n")
            f.write(f"    Combined: {result['similarity_combined']:.4f}\n")
            f.write(f"    Speech only: {result['similarity_speech']:.4f}\n")
            f.write(f"    DCASE only: {result['similarity_dcase']:.4f}\n")

            if result['similarity_combined'] > max(result['similarity_speech'], result['similarity_dcase']):
                f.write(f"    ✓ Combined description performs best\n")
            else:
                f.write(f"    ⚠ Individual description performs better\n")

            f.write(f"\n  Output files:\n")
            f.write(f"    Audio: {result['audio_path'].name}\n")
            f.write(f"    Description: {result['desc_path'].name}\n")
            f.write("\n" + "-" * 80 + "\n\n")

        # Calculate statistics
        combined_scores = [r['similarity_combined'] for r in all_results]
        speech_scores = [r['similarity_speech'] for r in all_results]
        dcase_scores = [r['similarity_dcase'] for r in all_results]

        f.write("Overall Statistics:\n")
        f.write(f"  Combined descriptions - Mean: {np.mean(combined_scores):.4f}, Std: {np.std(combined_scores):.4f}\n")
        f.write(f"  Speech only - Mean: {np.mean(speech_scores):.4f}, Std: {np.std(speech_scores):.4f}\n")
        f.write(f"  DCASE only - Mean: {np.mean(dcase_scores):.4f}, Std: {np.std(dcase_scores):.4f}\n\n")

        combined_wins = sum(1 for r in all_results if r['similarity_combined'] > max(r['similarity_speech'], r['similarity_dcase']))
        f.write(f"  Combined description wins: {combined_wins}/{num_mixtures} ({100*combined_wins/num_mixtures:.1f}%)\n")

    print(f"✓ Results saved to: {results_path}")
    print(f"✓ Created {num_mixtures} audio mixtures in: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mix LibriSpeech and DCASE audio files')
    parser.add_argument('--num-mixtures', type=int, default=5,
                        help='Number of random audio mixtures to create (default: 5)')

    args = parser.parse_args()
    run_mixup_experiment(args.num_mixtures)
