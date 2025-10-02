#!/usr/bin/env python3
"""
Mix LibriSpeech, DCASE, and MusicCaps audio files (3-way mixing).
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
MUSICCAPS_DIR = TEST_DATA_DIR / "music_caps"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"

def load_and_resample(audio_path, target_sr=16000):
    """Load audio file and resample to target sample rate."""
    audio, sr = sf.read(audio_path)
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    return audio, target_sr

def mix_three_audio(audio1, audio2, audio3, ratio1=0.33, ratio2=0.33, ratio3=0.34):
    """
    Mix three audio signals.

    Args:
        audio1, audio2, audio3: Audio arrays
        ratio1, ratio2, ratio3: Mixing ratios (should sum to ~1.0)

    Returns:
        Mixed audio array
    """
    # Make all arrays the same length by padding
    max_len = max(len(audio1), len(audio2), len(audio3))

    if len(audio1) < max_len:
        audio1 = np.pad(audio1, (0, max_len - len(audio1)))
    if len(audio2) < max_len:
        audio2 = np.pad(audio2, (0, max_len - len(audio2)))
    if len(audio3) < max_len:
        audio3 = np.pad(audio3, (0, max_len - len(audio3)))

    # Mix with specified ratios
    mixed = ratio1 * audio1 + ratio2 * audio2 + ratio3 * audio3

    # Normalize to prevent clipping
    max_val = np.max(np.abs(mixed))
    if max_val > 0:
        mixed = mixed / max_val * 0.95

    return mixed

def combine_three_descriptions(speech_desc, dcase_desc, music_desc):
    """
    Combine speech, DCASE, and music descriptions into natural English.

    Args:
        speech_desc: LibriSpeech description
        dcase_desc: DCASE description
        music_desc: MusicCaps description

    Returns:
        Naturally combined description
    """
    # Clean up descriptions
    speech = speech_desc.strip()
    ambient = dcase_desc.strip()
    music = music_desc.strip()

    # Remove trailing periods
    if speech.endswith('.'):
        speech = speech[:-1]
    if ambient.endswith('.'):
        ambient = ambient[:-1]
    if music.endswith('.'):
        music = music[:-1]

    # For music descriptions that are very long, take only the first sentence
    if len(music) > 150:
        # Split by period and take first sentence
        sentences = music.split('.')
        if len(sentences) > 1:
            music = sentences[0].strip()

    # Create natural three-way combination
    # Pattern: "[speech] with [ambient] and [music] playing in the background"
    combined = f"{speech} with {ambient} and {music} playing in the background"

    return combined

def run_mixup_experiment(num_mixtures=5):
    """
    Run the 3-way mixup experiment.

    Args:
        num_mixtures: Number of random audio mixtures to create (default: 5)
    """

    print("=" * 80)
    print(f"3-Way Audio Mixup: LibriSpeech + DCASE + MusicCaps ({num_mixtures} mixtures)")
    print("=" * 80)

    # Get all available files
    librispeech_files = sorted(LIBRISPEECH_DIR.glob("*.flac"))
    dcase_files = sorted(DCASE_DIR.glob("*.wav"))
    musiccaps_files = sorted(MUSICCAPS_DIR.glob("*.wav"))

    print(f"\nAvailable files:")
    print(f"  LibriSpeech: {len(librispeech_files)} files")
    print(f"  DCASE: {len(dcase_files)} files")
    print(f"  MusicCaps: {len(musiccaps_files)} files")

    # Randomly sample triplets
    random.seed(42)  # For reproducibility

    # Create random triplets
    triplets = []
    for i in range(num_mixtures):
        librispeech_file = random.choice(librispeech_files)
        dcase_file = random.choice(dcase_files)
        musiccaps_file = random.choice(musiccaps_files)
        triplets.append((librispeech_file, dcase_file, musiccaps_file, i + 1))

    print(f"\nGenerating {num_mixtures} random 3-way mixtures...")
    print("=" * 80)

    # Initialize CLAP model once
    import msclap
    model = msclap.CLAP(version='2023', use_cuda=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Store results for summary
    all_results = []

    for librispeech_path, dcase_path, musiccaps_path, mix_num in triplets:
        print(f"\n[Mixture {mix_num}/{num_mixtures}]")
        print(f"  LibriSpeech: {librispeech_path.name}")
        print(f"  DCASE: {dcase_path.name}")
        print(f"  MusicCaps: {musiccaps_path.name}")

        # Load audio files
        librispeech_audio, sr1 = load_and_resample(librispeech_path)
        dcase_audio, sr2 = load_and_resample(dcase_path)
        musiccaps_audio, sr3 = load_and_resample(musiccaps_path)

        # Mix audio (equal ratios)
        mixed_audio = mix_three_audio(librispeech_audio, dcase_audio, musiccaps_audio)

        # Create output filenames
        mix_name = f"mix_{mix_num:02d}_{librispeech_path.stem}_{dcase_path.stem}_{musiccaps_path.stem}"
        mixed_audio_path = OUTPUT_DIR / f"{mix_name}.wav"

        # Save mixed audio
        sf.write(mixed_audio_path, mixed_audio, sr1)

        # Load text descriptions
        librispeech_desc_path = LIBRISPEECH_DIR / f"{librispeech_path.stem}_description.txt"
        dcase_desc_path = DCASE_DIR / f"{dcase_path.stem}_description.txt"
        musiccaps_desc_path = MUSICCAPS_DIR / f"{musiccaps_path.stem}_description.txt"

        with open(librispeech_desc_path, 'r') as f:
            librispeech_desc = f.read().strip()
        with open(dcase_desc_path, 'r') as f:
            dcase_desc = f.read().strip()
        with open(musiccaps_desc_path, 'r') as f:
            musiccaps_desc = f.read().strip()

        # Combine descriptions naturally
        combined_desc = combine_three_descriptions(librispeech_desc, dcase_desc, musiccaps_desc)

        # Save combined description
        combined_desc_path = OUTPUT_DIR / f"{mix_name}_description.txt"
        with open(combined_desc_path, 'w') as f:
            f.write(combined_desc)

        print(f"  Combined: '{combined_desc[:120]}...'")

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

        text_embeddings_music = model.get_text_embeddings([musiccaps_desc])
        text_norm_music = text_embeddings_music / np.linalg.norm(text_embeddings_music, axis=1, keepdims=True)
        similarity_music = float((audio_norm @ text_norm_music.T)[0][0])

        print(f"  CLAP Scores:")
        print(f"    Combined: {similarity_combined:.4f}")
        print(f"    Speech: {similarity_speech:.4f} | DCASE: {similarity_dcase:.4f} | Music: {similarity_music:.4f}")

        # Store results
        result = {
            'mix_num': mix_num,
            'librispeech_file': librispeech_path.name,
            'dcase_file': dcase_path.name,
            'musiccaps_file': musiccaps_path.name,
            'librispeech_desc': librispeech_desc,
            'dcase_desc': dcase_desc,
            'musiccaps_desc': musiccaps_desc,
            'combined_desc': combined_desc,
            'similarity_combined': similarity_combined,
            'similarity_speech': similarity_speech,
            'similarity_dcase': similarity_dcase,
            'similarity_music': similarity_music,
            'audio_path': mixed_audio_path,
            'desc_path': combined_desc_path
        }
        all_results.append(result)

    # Save comprehensive results
    print(f"\n{'=' * 80}")
    print("Saving comprehensive results...")
    results_path = OUTPUT_DIR / "experiment_summary.txt"

    with open(results_path, 'w') as f:
        f.write("3-Way Audio Mixup Experiment - Summary\n")
        f.write("LibriSpeech + DCASE + MusicCaps\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total mixtures created: {num_mixtures}\n\n")

        for result in all_results:
            f.write(f"Mixture {result['mix_num']}:\n")
            f.write(f"  LibriSpeech: {result['librispeech_file']}\n")
            f.write(f"  DCASE: {result['dcase_file']}\n")
            f.write(f"  MusicCaps: {result['musiccaps_file']}\n\n")
            f.write(f"  Speech description: {result['librispeech_desc']}\n")
            f.write(f"  DCASE description: {result['dcase_desc']}\n")
            f.write(f"  MusicCaps description: {result['musiccaps_desc']}\n")
            f.write(f"  Combined description: {result['combined_desc']}\n\n")
            f.write(f"  CLAP Similarity Scores:\n")
            f.write(f"    Combined: {result['similarity_combined']:.4f}\n")
            f.write(f"    Speech only: {result['similarity_speech']:.4f}\n")
            f.write(f"    DCASE only: {result['similarity_dcase']:.4f}\n")
            f.write(f"    Music only: {result['similarity_music']:.4f}\n")

            max_individual = max(result['similarity_speech'],
                                result['similarity_dcase'],
                                result['similarity_music'])

            if result['similarity_combined'] > max_individual:
                f.write(f"    ✓ Combined description performs best\n")
            else:
                f.write(f"    ⚠ Individual description performs better (max: {max_individual:.4f})\n")

            f.write(f"\n  Output files:\n")
            f.write(f"    Audio: {result['audio_path'].name}\n")
            f.write(f"    Description: {result['desc_path'].name}\n")
            f.write("\n" + "-" * 80 + "\n\n")

        # Calculate statistics
        combined_scores = [r['similarity_combined'] for r in all_results]
        speech_scores = [r['similarity_speech'] for r in all_results]
        dcase_scores = [r['similarity_dcase'] for r in all_results]
        music_scores = [r['similarity_music'] for r in all_results]

        f.write("Overall Statistics:\n")
        f.write(f"  Combined descriptions - Mean: {np.mean(combined_scores):.4f}, Std: {np.std(combined_scores):.4f}\n")
        f.write(f"  Speech only - Mean: {np.mean(speech_scores):.4f}, Std: {np.std(speech_scores):.4f}\n")
        f.write(f"  DCASE only - Mean: {np.mean(dcase_scores):.4f}, Std: {np.std(dcase_scores):.4f}\n")
        f.write(f"  Music only - Mean: {np.mean(music_scores):.4f}, Std: {np.std(music_scores):.4f}\n\n")

        combined_wins = sum(1 for r in all_results
                           if r['similarity_combined'] > max(r['similarity_speech'],
                                                             r['similarity_dcase'],
                                                             r['similarity_music']))
        f.write(f"  Combined description wins: {combined_wins}/{num_mixtures} ({100*combined_wins/num_mixtures:.1f}%)\n")

    print(f"✓ Results saved to: {results_path}")
    print(f"✓ Created {num_mixtures} audio mixtures in: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mix LibriSpeech, DCASE, and MusicCaps audio files (3-way)')
    parser.add_argument('--num-mixtures', type=int, default=5,
                        help='Number of random audio mixtures to create (default: 5)')

    args = parser.parse_args()
    run_mixup_experiment(args.num_mixtures)
