#!/usr/bin/env python3
"""
Test CLAP similarity with negative samples using MusicCaps description.
Takes one MusicCaps description and tests against all LibriSpeech and DCASE audio.
Expected: Low similarity scores since music descriptions are unrelated to speech/audio events.
"""

import sys
from pathlib import Path
import numpy as np

# Add parent directory to path to import clap_similarity
sys.path.insert(0, str(Path(__file__).parent.parent))

from clap_similarity import calculate_similarity_msclap

# Dataset paths
SCRIPT_DIR = Path(__file__).parent
DCASE_DIR = SCRIPT_DIR.parent / "test_data" / "dcase"
LIBRISPEECH_DIR = SCRIPT_DIR.parent / "test_data" / "librispeech"
MUSICCAPS_DIR = SCRIPT_DIR.parent / "test_data" / "music_caps"

def test_negative_samples_musiccaps():
    """Test MusicCaps description against unrelated audio files."""

    # Get first MusicCaps description as our test description
    musiccaps_desc_file = MUSICCAPS_DIR / "-0Gj8-vB1q4_description.txt"

    if not musiccaps_desc_file.exists():
        print(f"Error: MusicCaps description file not found: {musiccaps_desc_file}")
        return

    with open(musiccaps_desc_file, 'r') as f:
        test_description = f.read().strip()

    print(f"Testing MusicCaps description as negative sample:")
    print(f"  Description: '{test_description}'")
    print("=" * 80)

    # Initialize CLAP model once
    import msclap
    model = msclap.CLAP(version='2023', use_cuda=False)

    all_scores = []
    results = []

    # Test against LibriSpeech audio files
    print("\nTesting against LibriSpeech audio files...")
    print("-" * 80)

    librispeech_files = sorted(LIBRISPEECH_DIR.glob("*.flac"))
    librispeech_scores = []

    for audio_file in librispeech_files:
        audio_embeddings = model.get_audio_embeddings([str(audio_file)], resample=True)
        text_embeddings = model.get_text_embeddings([test_description])

        # Normalize and calculate cosine similarity
        audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
        text_norm = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
        similarity = audio_norm @ text_norm.T
        similarity_score = float(similarity[0][0])

        librispeech_scores.append(similarity_score)
        all_scores.append(similarity_score)

        result_line = f"LibriSpeech/{audio_file.name}: {similarity_score:.4f}"
        results.append(result_line)
        print(f"  {audio_file.name}: {similarity_score:.4f}")

    # Test against DCASE audio files
    print("\nTesting against DCASE audio files...")
    print("-" * 80)

    dcase_files = sorted(DCASE_DIR.glob("*.wav"))
    dcase_scores = []

    for audio_file in dcase_files:
        audio_embeddings = model.get_audio_embeddings([str(audio_file)], resample=True)
        text_embeddings = model.get_text_embeddings([test_description])

        # Normalize and calculate cosine similarity
        audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
        text_norm = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
        similarity = audio_norm @ text_norm.T
        similarity_score = float(similarity[0][0])

        dcase_scores.append(similarity_score)
        all_scores.append(similarity_score)

        result_line = f"DCASE/{audio_file.name}: {similarity_score:.4f}"
        results.append(result_line)
        print(f"  {audio_file.name}: {similarity_score:.4f}")

    # Calculate statistics
    summary = []
    summary.append("=" * 80)
    summary.append("NEGATIVE SAMPLE TEST (MusicCaps) - SUMMARY STATISTICS")
    summary.append("=" * 80)
    summary.append(f"Test description: '{test_description}'")
    summary.append(f"Source: {musiccaps_desc_file.name}")
    summary.append("")
    summary.append(f"Total audio files tested: {len(all_scores)}")
    summary.append(f"  - LibriSpeech: {len(librispeech_scores)}")
    summary.append(f"  - DCASE: {len(dcase_scores)}")
    summary.append("")
    summary.append("Overall Statistics:")
    summary.append(f"  Mean similarity: {np.mean(all_scores):.4f}")
    summary.append(f"  Std deviation: {np.std(all_scores):.4f}")
    summary.append(f"  Min similarity: {np.min(all_scores):.4f}")
    summary.append(f"  Max similarity: {np.max(all_scores):.4f}")
    summary.append(f"  Median similarity: {np.median(all_scores):.4f}")
    summary.append("")
    summary.append("LibriSpeech Statistics:")
    summary.append(f"  Mean: {np.mean(librispeech_scores):.4f}")
    summary.append(f"  Min: {np.min(librispeech_scores):.4f}")
    summary.append(f"  Max: {np.max(librispeech_scores):.4f}")
    summary.append("")
    summary.append("DCASE Statistics:")
    summary.append(f"  Mean: {np.mean(dcase_scores):.4f}")
    summary.append(f"  Min: {np.min(dcase_scores):.4f}")
    summary.append(f"  Max: {np.max(dcase_scores):.4f}")
    summary.append("")
    summary.append("Expected: Low scores (< 0.1) since music descriptions")
    summary.append("          are unrelated to speech (LibriSpeech) and audio events (DCASE)")
    summary.append("=" * 80)

    print("\n" + "\n".join(summary))

    # Write results to file
    output_file = SCRIPT_DIR.parent / "results" / "negative_tests" / "negative_sample_test_results_musiccaps.txt"
    with open(output_file, 'w') as f:
        f.write("NEGATIVE SAMPLE TEST RESULTS (MusicCaps Description)\n")
        f.write("Testing MusicCaps description against unrelated audio\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            f.write(result + "\n")

        f.write("\n")
        for line in summary:
            f.write(line + "\n")

    print(f"\nResults saved to: {output_file}")

    return all_scores, summary

if __name__ == "__main__":
    test_negative_samples_musiccaps()
